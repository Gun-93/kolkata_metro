# TESTIMONIAL

## Overall Approach

I first understood the project structure and how the frontend, backend, SQLite, and PostgreSQL work together. I completed the assessment feature by feature and verified each API before moving to the next task.

## Understanding the Project

The project uses React and Vite for the frontend, FastAPI for the backend, SQLite for metro route data, and PostgreSQL for ticket management. Route planning is implemented using Dijkstra's shortest path algorithm.

## Bugs Encountered During Setup

- SQLite database path issue.
- SQLite connection context manager issue.
- PostgreSQL authentication issue.
- Missing PostgreSQL tables.
- API integration issues during setup.

## How I Resolved Them

- Corrected the SQLite database path.
- Updated the graph routing implementation.
- Configured the correct PostgreSQL credentials.
- Initialized the PostgreSQL database using the provided SQL script.
- Tested all APIs before verifying the frontend.

## Challenges Faced

The biggest challenge was understanding an unfamiliar codebase, configuring both SQLite and PostgreSQL correctly, and debugging backend issues during setup.

## Assumptions Made

- Existing station metadata is correct.
- Metro connections are already available in the SQLite database.
- Existing API contracts should not be modified.

## Improvements

If given more time, I would:

- Improve the UI and responsiveness.
- Add better error handling.
- Add route visualization on a metro map.
- Write unit and integration tests.
- Improve application performance by caching frequently requested routes.