
{
  "order_id": "ORD123",
  "user_id": 1001,
  "items": [
    {
      "product_id": "P101",
      "quantity": 2
    }
  ],
  "payment_method": "CARD",
  "amount": 1200
}

#Validation Service Access

DB Data Needed
1. OrderId, orderAmount -> orders (Check Product exists, Price Validation)
2. user_id, isActive -> Users (Check User exists)
3. At least one item to order
4. Quantity > 0
5. Quantity !> 10
6. Amount > 0
7. Valid payment method
8. Valid currency code

Too many orders (More than 10 order place)

Client
  |
  v
FastAPI Order API
  |
  | Produce Event (Create a DB Entry)
  v
Kafka: orders.created
  |
  v
Python Validation Service (Asyncio) (Update a DB Entry)
  |
  +-------------------------+
  |                         |
  | Valid                   | Invalid
  v                         v
Kafka: orders.valid     Kafka: orders.failed
  |
  v
Go Order Processor (Update a DB Entry)
  |
  | Redis Idempotency Check
  | (SETNX lock / idempotency key)
  |
  | DB Transaction
  v
PostgreSQL
  |
  | Publish Event
  v
Kafka: orders.processed
  |
  +---------------------+
  |                     |
  v                     v
Audit Service        Notification/Other Services



# Order Service
Python + FastAPI

POST /orders
{
   "user_id":123,
   "items":[...],
   "amount":1000
}

Request
   ↓
FastAPI
   ↓
Publish to Kafka
   ↓
Return 202 Accepted

# Validation Engine
Python

Amount > 0
User Exists
Duplicate Order
Business Rules

# Order Processor
Go Gin
Consumes -> Creates( Order, Payment ) - order-created

#Audit Service
orders
valid-orders
order-created

CREATE TABLE orders(
   id UUID PRIMARY KEY,
   user_id BIGINT,
   amount NUMERIC,
   status VARCHAR(50),
   created_at TIMESTAMP
);

CREATE TABLE payments(
   id UUID PRIMARY KEY,
   order_id UUID,
   status VARCHAR(50)
);

CREATE TABLE audit_logs(
   id SERIAL PRIMARY KEY,
   event_type VARCHAR(100),
   payload JSONB,
   created_at TIMESTAMP
);

Kafka Topics

valid-orders
invalid-orders
order-created
payment-created

Exactly Once Delivery
SETNX order:123 processing
if exists -> process saveDb


Monitoring
orders_received_total
orders_processed_total
validation_failed_total
kafka_consumer_lag

CICD

Lint
Test
Build Docker
Push Image
Deploy
