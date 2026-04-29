SHELL := /bin/zsh

.PHONY: bootstrap seed dev demo-call previews test audit backend-test frontend-check frontend-test

bootstrap:
	python3 -m venv signal-server/.venv
	. signal-server/.venv/bin/activate && pip install -U pip
	. signal-server/.venv/bin/activate && pip install -e ./signal-server
	. signal-server/.venv/bin/activate && pip install pytest
	cd call-room && npm install

seed:
	. signal-server/.venv/bin/activate && python -m callsignal.tools.seed_demo_state

dev:
	bash tools/dev.sh

demo-call:
	. signal-server/.venv/bin/activate && python -m callsignal.tools.run_demo_call

previews:
	. signal-server/.venv/bin/activate && python -m callsignal.tools.capture_previews

backend-test:
	. signal-server/.venv/bin/activate && pytest signal-server/tests -q

frontend-check:
	cd call-room && npm run check

frontend-test:
	cd call-room && npm test

test: backend-test frontend-check frontend-test

audit:
	bash tools/verify_no_ai_traces.sh
	bash tools/check_empty_folders.sh
