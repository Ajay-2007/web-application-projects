uvicorn run:app --reload --port 3002

# docker run --name=bookstore-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:10

# docker run --name my-redis -d -p 6379:6379 redis


# docker build -t bookstore-api-build .
# docker run --name=bookstore-api -idt -e MODULE_NAME="run" -e PORT="3001" -e PRODUCTION="true" -p 3001:3001 bookstore-api-build
# docker logs -f bookstore-api