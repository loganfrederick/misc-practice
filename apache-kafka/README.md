# Apache Kafka Producer-Consumer Model Tutorial

## What is the Producer-Consumer Model?

The **producer-consumer model** is a classic software design pattern where:
- **Producers** create and send data/messages
- **Consumers** receive and process those messages
- A **message broker** (like Kafka) sits in the middle to decouple producers from consumers

### Key Benefits:
1. **Decoupling**: Producers and consumers don't need to know about each other
2. **Scalability**: Add more producers or consumers independently
3. **Reliability**: Messages are persisted and can be replayed
4. **Asynchronous**: Producers don't wait for consumers to process messages

---

## Apache Kafka Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Producer   │────────▶│    Kafka     │────────▶│  Consumer   │
│  (Sender)   │         │   (Broker)   │         │ (Receiver)  │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ▼
                         ┌─────────┐
                         │  Topic  │ (Category/Channel)
                         └─────────┘
                              │
                         ┌────┴────┐
                    Partition 0  Partition 1  ...
```

### Core Concepts:

1. **Topic**: A category or feed name to which messages are published
   - Like a channel or queue name
   - Example: "orders", "user-events", "logs"

2. **Partition**: Topics are split into partitions for scalability
   - Messages within a partition are ordered
   - Different partitions can be on different servers

3. **Producer**: Application that publishes messages to topics
   - Decides which partition to send to (or Kafka chooses)
   - Can send messages synchronously or asynchronously

4. **Consumer**: Application that subscribes to topics and processes messages
   - Can be part of a consumer group for load balancing
   - Tracks its position (offset) in the message stream

5. **Broker**: A Kafka server that stores data and serves clients
   - Multiple brokers form a Kafka cluster

6. **Offset**: Unique ID for each message within a partition
   - Consumers track which messages they've processed

---

## How It Works

### Message Flow:

1. **Producer sends message** to a topic
   ```python
   producer.send('my-topic', value='Hello Kafka!')
   ```

2. **Kafka stores** the message in a partition
   - Messages are written to disk (durable)
   - Retained for a configured time (e.g., 7 days)

3. **Consumer reads** messages from the topic
   ```python
   for message in consumer:
       process(message.value)
   ```

4. **Consumer commits offset** to track progress
   - If consumer crashes, it can resume from last committed offset

---

## Setup Instructions

### 1. Start Kafka with Docker

```bash
docker-compose up -d
```

This starts:
- **Zookeeper** (coordinates Kafka brokers)
- **Kafka broker** (the message broker)

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Examples

**Terminal 1 - Start Consumer:**
```bash
python consumer.py
```

**Terminal 2 - Send Messages with Producer:**
```bash
python producer.py
```

Watch the consumer receive and process messages in real-time!

---

## Example Use Cases

1. **Event Streaming**: User clicks, page views, transactions
2. **Log Aggregation**: Collecting logs from multiple services
3. **Message Queue**: Asynchronous task processing
4. **Data Pipeline**: ETL processes, data integration
5. **Microservices Communication**: Decoupled service-to-service messaging

---

## Advanced Features (Not in This Tutorial)

- **Consumer Groups**: Multiple consumers share the workload
- **Message Keys**: Control which partition messages go to
- **Exactly-Once Semantics**: Guaranteed message processing
- **Kafka Streams**: Real-time stream processing
- **Schema Registry**: Manage message schemas
- **Transactions**: Atomic multi-message operations


## Try These Experiments

Now that you have Kafka running, try these hands-on experiments to understand key concepts:

### Experiment 1: Message Durability
**Concept**: Kafka persists messages to disk - they don't disappear!

1. **Stop the consumer** (Ctrl+C in Terminal 1)
2. **Run the producer** several times (`python producer.py` in Terminal 2)
3. **Restart the consumer** (`python consumer.py` in Terminal 1)
4. **Observe**: The consumer receives all the messages that were sent while it was offline!

**Why?** Kafka stores messages durably. Consumers can read at their own pace.

### Experiment 2: Message Ordering
**Concept**: Messages within a partition are always processed in order.

1. Run the consumer
2. Run the producer and observe the sequence numbers in batch messages
3. **Observe**: Messages always arrive in the exact order they were sent

**Why?** Kafka guarantees ordering within each partition (though not across partitions).

### Experiment 3: Load Balancing with Consumer Groups
**Concept**: Multiple consumers can share the workload.

1. Open **3 terminal windows**
2. In each, run: `python consumer_group.py`
3. Wait for all 3 to connect (you'll see different colored output)
4. In a **4th terminal**, run: `python producer.py`
5. **Observe**: Messages are distributed across the 3 consumers - each processes different messages!

**Why?** Kafka automatically distributes partitions among consumers in the same group.

### Experiment 4: Fault Tolerance
**Concept**: If a consumer fails, others take over its work.

1. Keep the 3 consumers from Experiment 3 running
2. **Kill one consumer** (Ctrl+C)
3. Run the producer again
4. **Observe**: The remaining 2 consumers now handle all the messages

**Why?** Kafka rebalances partitions when consumers join or leave a group.

### Experiment 5: Multiple Runs & Offset Management
**Concept**: Consumers remember where they left off.

1. Start a consumer and let it process some messages
2. **Stop it** (Ctrl+C)
3. **Start it again**
4. Run the producer with new messages
5. **Observe**: The consumer only processes NEW messages, not old ones

**Why?** Kafka tracks each consumer's offset (position) in the message stream.


---

## Common Patterns

### 1. Fan-Out Pattern
One producer, multiple consumers (each gets all messages)
```
Producer ──▶ Topic ──▶ Consumer Group A
                   └──▶ Consumer Group B
```

### 2. Load Balancing Pattern
One producer, consumer group with multiple consumers (messages distributed)
```
Producer ──▶ Topic ──▶ Consumer Group {
                         Consumer 1,
                         Consumer 2,
                         Consumer 3
                       }
```

### 3. Message Priority
Use different topics for different priorities
```
Producer ──▶ high-priority-topic
         └──▶ low-priority-topic
```

---

## Troubleshooting

**Consumer not receiving messages?**
- Check that topic names match
- Ensure Kafka is running: `docker-compose ps`
- Check consumer group is configured correctly

**Producer timing out?**
- Verify Kafka is accessible at localhost:9092
- Check Docker logs: `docker-compose logs kafka`

**Messages processed multiple times?**
- Consumer crashed before committing offset
- This is expected behavior! Design consumers to be idempotent

---

## Cleanup

```bash
# Stop Kafka and Zookeeper
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v
```

---

## Learn More

- [Official Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [Confluent Kafka Tutorials](https://kafka-tutorials.confluent.io/)

