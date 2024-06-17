run:
	@fastapi run portaled/main.py

run dev:
	@fastapi dev portaled/main.py

lint:
	@black portaled/*.py . --exclude .venv

test:
	@pytest portaled/tests