# Order Creation Workflow

## Purpose

Accept customer orders asynchronously and process them using Kafka.

---

## Actors

- Client
- Order API
- Kafka
- Validation Service
- Order Processor
- PostgreSQL

---

## Flow

Client
  |
  v
POST /orders
  |
  v
Order API
  |
  v
Kafka: orders.created
  |
  v
Validation Service
  |
  +----------------+
  |                |
  v                v
Valid            Invalid
  |                |
  v                v
orders.valid   orders.failed
  |
  v
Order Processor
  |
  +--> PostgreSQL
  |
  +--> Kafka: orders.processed


---

## Kafka Topics

Input:
- orders.created

Output:
- orders.valid
- orders.failed
- orders.processed


---

## Failure Handling

- Kafka retry on consumer failure
- Invalid orders are routed to `orders.failed`
- Duplicate requests handled using Redis idempotency key


---

## Metrics

- orders_received_total
- orders_valid_total
- orders_failed_total
- orders_processed_total
