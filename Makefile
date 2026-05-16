.PHONY: setup run-app run-attacker reset-db clean

setup:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && python -m pip install -r requirements.txt

run-app:
	. .venv/bin/activate && python app/main.py

run-attacker:
	. .venv/bin/activate && python tools/attacker_server.py

reset-db:
	. .venv/bin/activate && python app/main.py --reset-db --init-only

clean:
	rm -f app/data.db app/mail_outbox.txt stolen_cookies.log badscript_ran.txt downloaded_badscript.py command_injection_result.txt
