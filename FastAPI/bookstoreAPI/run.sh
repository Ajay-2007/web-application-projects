uvicorn run:app --reload --port 3000

# docker run --name=bookstore-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:10

# docker run --name my-redis -d -p 6379:6379 redis