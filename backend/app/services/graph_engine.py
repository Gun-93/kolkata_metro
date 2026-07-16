'''
import heapq
from app.db.sqlite_client import get_sqlite_conn

def get_metro_route(source_name: str, destination_name: str):
    """
    Computes the shortest route (based on travel time) between the source and 
    destination metro stations using Dijkstra's algorithm.
    Reads station, connection, and interchange graphs dynamically from SQLite.
    """
    pass

'''
import heapq
from collections import defaultdict
from app.db.sqlite_client import get_sqlite_conn


def get_metro_route(source_name: str, destination_name: str):
    with get_sqlite_conn() as conn:

        conn.row_factory = None
        cur = conn.cursor()

        # -----------------------------
        # Load Stations
        # -----------------------------
        cur.execute("""
            SELECT id, name, line
            FROM stations
        """)

        stations = {}
        name_to_ids = defaultdict(list)

        for station_id, name, line in cur.fetchall():
            stations[station_id] = {
                "name": name,
                "line": line
            }
            name_to_ids[name.strip().lower()].append(station_id)

        source_candidates = name_to_ids.get(source_name.strip().lower(), [])
        destination_candidates = name_to_ids.get(destination_name.strip().lower(), [])

        if not source_candidates:
            raise ValueError(f"Source station '{source_name}' not found.")

        if not destination_candidates:
            raise ValueError(f"Destination station '{destination_name}' not found.")

        # -----------------------------
        # Build Graph
        # -----------------------------
        graph = defaultdict(list)

        # Normal Connections
        cur.execute("""
            SELECT
                station_a_id,
                station_b_id,
                travel_time_minutes,
                fare_inr
            FROM connections
        """)

        for a, b, travel_time, fare in cur.fetchall():
            graph[a].append((b, travel_time, fare, False))
            

        # Interchanges
        cur.execute("""
            SELECT
                station_from_id,
                station_to_id,
                transfer_time_minutes
            FROM interchanges
        """)

        for a, b, transfer_time in cur.fetchall():
            graph[a].append((b, transfer_time, 0, True))
            

        # ---------------------------------------------------
        # Run Dijkstra for every source/destination variant
        # ---------------------------------------------------
        best_result = None

        for source in source_candidates:
            for destination in destination_candidates:

                pq = []
                heapq.heappush(pq, (0, source))

                dist = {source: 0}
                fare_cost = {source: 0}
                parent = {}

                while pq:
                    current_time, node = heapq.heappop(pq)

                    if current_time > dist[node]:
                        continue

                    if node == destination:
                        break

                    for neighbour, edge_time, edge_fare, _ in graph[node]:

                        new_time = current_time + edge_time
                        new_fare = fare_cost[node] + edge_fare

                        if (
                            neighbour not in dist
                            or new_time < dist[neighbour]
                            or (
                                new_time == dist[neighbour]
                                and new_fare < fare_cost[neighbour]
                            )
                        ):
                            dist[neighbour] = new_time
                            fare_cost[neighbour] = new_fare
                            parent[neighbour] = node
                            heapq.heappush(pq, (new_time, neighbour))

                if destination not in dist:
                    continue

                if best_result is None or dist[destination] < best_result["time"]:
                    best_result = {
                        "source": source,
                        "destination": destination,
                        "time": dist[destination],
                        "fare": fare_cost[destination],
                        "parent": parent,
                    }

        if best_result is None:
            raise ValueError("No route found.")

        # -----------------------------
        # Reconstruct Path
        # -----------------------------
        path = []

        node = best_result["destination"]

        while True:
            path.append(node)

            if node == best_result["source"]:
                break

            node = best_result["parent"][node]

        path.reverse()

        # -----------------------------
        # Build Itinerary
        # -----------------------------
        ordered_itinerary = []
        interchange_count = 0

        for i, station_id in enumerate(path):

            station = stations[station_id]

            is_interchange = False
            transfer_to = None

            if i < len(path) - 1:
                next_station = path[i + 1]

                current_line = station["line"]
                next_line = stations[next_station]["line"]

                if current_line != next_line:
                    is_interchange = True
                    transfer_to = next_line
                    interchange_count += 1

            ordered_itinerary.append({
                "station_name": station["name"],
                "line": station["line"],
                "is_interchange": is_interchange,
                "transfer_to": transfer_to
            })

        # -----------------------------
        # Response
        # -----------------------------
        return {
            "route_summary": {
                "source": stations[best_result["source"]]["name"],
                "destination": stations[best_result["destination"]]["name"],
                "total_fare_inr": best_result["fare"],
                "total_travel_time_minutes": best_result["time"],
                "interchanges_count": interchange_count
            },
            "ordered_itinerary": ordered_itinerary
        }