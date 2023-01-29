# FastAPI and Redis in Microservices Architecture

In this example, I've used FastAPI and Redis database in microservices architecture context.
I've used FastAPI as a web framework in a two services: Inventory and Payment.

Also, I've used RedisJSON (NoSQL Database) as a database for each service (each service with a different instance), and Redis Streams as a message broker.

## System Design

<p align="center">
<img src="System Diagram - FastAPI Microservices.jpg" width=60% height=60%>
</p>

## API Endpoints
To reach the API endpoints, run the service and you can see and try the endpoints using this path formula:

```
localhost:port/redoc
```

For example:

```
http://127.0.0.1:8000/redoc
```

*Note*: Run each service on a different port
