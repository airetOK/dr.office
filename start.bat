coverage run -m --source=. pytest --ignore=tests/e2e
coverage report
coverage html
docker-compose up -d
playwright install
pytest tests/e2e