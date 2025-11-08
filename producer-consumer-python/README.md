# Producer-Consumer Pattern in Python

## What is the Producer-Consumer Pattern?

The **producer-consumer pattern** is a classic concurrency design pattern where:

- **Producers** create data/work items and add them to a shared buffer
- **Consumers** take data/work items from the buffer and process them
- A **Queue** (buffer) sits between them to decouple production from consumption

## Why Use This Pattern?

1. **Decoupling**: Producers and consumers work independently at their own pace
2. **Thread Safety**: Queues handle synchronization automatically
3. **Load Balancing**: Multiple consumers can process items in parallel
4. **Buffering**: Handles speed differences between production and consumption

## Key Components

### Queue
- Acts as a thread-safe buffer between producers and consumers
- Python's `queue.Queue` is designed for this pattern
- Main methods:
  - `put(item)` - Add item to queue (blocks if full)
  - `get()` - Remove and return item (blocks if empty)
  - `task_done()` - Signal that processing is complete
  - `join()` - Block until all items are processed

### Producer Thread
- Generates data/work items
- Puts items into the queue
- Can signal completion (e.g., with a sentinel value)

### Consumer Thread
- Takes items from the queue
- Processes each item
- Calls `task_done()` when finished

## Examples in This Folder

1. **basic_example.py** - Simple single producer, single consumer
2. **multiple_consumers.py** - One producer, multiple consumers working in parallel
3. **multiple_producers.py** - Multiple producers, multiple consumers
4. **real_world_example.py** - Practical example: web scraper with URL processing

## Running the Examples

```bash
# Basic example
python basic_example.py

# Multiple consumers
python multiple_consumers.py

# Multiple producers and consumers
python multiple_producers.py

# Real-world example
python real_world_example.py
```

## Common Patterns

### Signaling Completion
Use a sentinel value (like `None`) to tell consumers to stop:
```python
# Producer signals done
queue.put(None)

# Consumer checks for sentinel
while True:
    item = queue.get()
    if item is None:
        break
    process(item)
```

### Multiple Consumers
Send one sentinel per consumer:
```python
# Signal all consumers to stop
for _ in range(num_consumers):
    queue.put(None)
```

## Best Practices

1. **Always call `task_done()`** after processing each item
2. **Use sentinel values** to signal completion
3. **Handle exceptions** in both producers and consumers
4. **Set queue size** (`maxsize`) to prevent memory issues
5. **Use timeouts** when appropriate to prevent deadlocks


