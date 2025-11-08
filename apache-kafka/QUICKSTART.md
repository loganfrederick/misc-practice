# Quick Start Guide

Get up and running with Kafka in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ installed
- Basic understanding of terminal/command line

## Step-by-Step Instructions

### 1. Start Kafka (30 seconds)

```bash
cd /Users/loganfrederick/Projects/misc-practice/apache-kafka
docker-compose up -d
```

Wait about 30 seconds for Kafka to fully start. Check status:
```bash
docker-compose ps
```

You should see both `zookeeper` and `kafka` running.

### 2. Install Python Dependencies (10 seconds)

```bash
pip install -r requirements.txt
```

### 3. Run the Consumer (Terminal 1)

Open a terminal and run:
```bash
python consumer.py
```

You should see:
```
KAFKA CONSUMER DEMO
==================================================
Connecting to Kafka broker at localhost:9092...
✓ Connected successfully!
Waiting for messages...
```

**Leave this running!** The consumer waits for messages.

### 4. Run the Producer (Terminal 2)

Open a **second terminal** and run:
```bash
python producer.py
```

### 5. Watch the Magic! ✨

Switch back to **Terminal 1** (consumer). You should see messages appearing in real-time as the producer sends them!

## What Just Happened?

1. **Producer** created messages and sent them to Kafka topic `demo-topic`
2. **Kafka** stored these messages durably
3. **Consumer** read messages from the topic and processed them
4. They never directly communicated - Kafka acted as the middleman!

## Try This

### Experiment 1: Order Doesn't Matter
- Stop the consumer (Ctrl+C)
- Run the producer again (messages get stored in Kafka)
- Start the consumer - it will receive all messages!

### Experiment 2: Multiple Runs
- Run the producer multiple times
- Consumer receives all messages in order

### Experiment 3: Restart Consumer
- Consumer remembers its position (offset)
- Stop and restart consumer - it continues from where it left off

## Clean Up

When done experimenting:

```bash
# Stop Kafka
docker-compose down

# Remove all data (optional)
docker-compose down -v
```

## What's Next?

- Read the full `README.md` for detailed explanations
- Check out `consumer_group.py` to see multiple consumers working together
- Modify the code to send your own custom messages!

## Troubleshooting

**"Connection refused" error?**
- Make sure Docker containers are running: `docker-compose ps`
- Wait 30-60 seconds after starting for Kafka to be ready

**Consumer not receiving messages?**
- Make sure both scripts use the same topic name
- Check that consumer is running when you send messages

**Port already in use?**
- Something else is using port 9092
- Stop other Kafka instances or change the port in `docker-compose.yml`

