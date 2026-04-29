# Local runbook

1. Copy `.env.example` to `.env` if you want to override paths or ports.
2. Run `make bootstrap` once.
3. Run `make seed` to load the synthetic scenarios into SQLite.
4. Run `make dev` to start the backend and frontend together.
5. Open the Voice Workspace and start a demo call.
6. Use the Supervisor Board and Call Review screens to inspect the seeded history.

The backend is local by default. No paid model keys are needed for the deterministic demo mode.
