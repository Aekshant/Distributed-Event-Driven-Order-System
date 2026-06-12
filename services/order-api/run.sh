uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload


alembic revision --autogenerate -m "add status to orders table"
alembic upgrade head