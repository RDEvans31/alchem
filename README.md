# Alchem Prototype event driven architecture
A minimal management console - single page on next.js that polls the apij every 5 seconds.

A Python FastAPI API that handles events and communicates with the database.

The database is a SQLite database that is generated on startup

The e2e test runs on selenium and simulates events and then checks the front end to see that it updates.
