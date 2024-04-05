coverage run -m --source=. pytest --ignore=tests/e2e
coverage report
coverage html
docker-compose up -d
pytest tests/e2e