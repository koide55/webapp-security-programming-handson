PYTHON ?= python3

.PHONY: setup run-app run-attacker reset-db clean

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && python -m pip install -r requirements.txt

run-app:
	. .venv/bin/activate && python app/main.py

run-attacker:
	. .venv/bin/activate && python tools/attacker_server.py

reset-db:
	. .venv/bin/activate && python app/main.py --reset-db --init-only

clean:
	$(PYTHON) tools/clean.py
