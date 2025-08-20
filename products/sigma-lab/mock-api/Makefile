.PHONY: run dev smoke

run:
	uvicorn mock_api.app:app --host 0.0.0.0 --port 8010

dev:
	uvicorn mock_api.app:app --reload --port 8010

smoke:
	@echo "Running mock API smoke tests against $${MOCK_API_URL:-http://localhost:8010}"
	python smoke.py

