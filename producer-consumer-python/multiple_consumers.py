"""
Multiple Consumers Example

This shows how multiple consumer threads can process items in parallel,
which is useful for:
- Improving throughput
- Load balancing
- Utilizing multiple CPU cores for I/O-bound tasks
"""

import queue
import threading
import time
import random


def producer(q, num_items):
    """
    Producer that generates work items for multiple consumers.
    
    Args:
        q: The queue to put items into
        num_items: Number of items to produce
    """
    print("[Producer] Starting...")
    
    for i in range(num_items):
        # Simulate work
        time.sleep(random.uniform(0.05, 0.2))
        
        item = f"Task-{i}"
        q.put(item)
        print(f"[Producer] Created {item}")
    
    print(f"[Producer] Finished producing {num_items} items")


def consumer(q, consumer_id):
    """
    Consumer that processes work items.
    
    Args:
        q: The queue to get items from
        consumer_id: Unique identifier for this consumer
    """
    print(f"[Consumer-{consumer_id}] Starting...")
    items_processed = 0
    
    while True:
        try:
            # Try to get item with timeout to check for completion
            item = q.get(timeout=1)
            
            # Check for stop signal
            if item is None:
                print(f"[Consumer-{consumer_id}] Received stop signal")
                q.task_done()
                break
            
            # Process the item
            items_processed += 1
            print(f"[Consumer-{consumer_id}] Processing {item}...")
            
            # Simulate variable processing time
            time.sleep(random.uniform(0.3, 0.9))
            
            print(f"[Consumer-{consumer_id}] Completed {item}")
            q.task_done()
            
        except queue.Empty:
            # Queue is empty, check if we should continue waiting
            continue
    
    print(f"[Consumer-{consumer_id}] Shutting down. Processed {items_processed} items.")


def main():
    """Run the multiple consumers example."""
    print("=" * 60)
    print("MULTIPLE CONSUMERS EXAMPLE")
    print("=" * 60)
    print()
    
    # Configuration
    num_items = 10
    num_consumers = 3
    
    # Create a queue
    work_queue = queue.Queue()
    
    # Create and start multiple consumer threads
    consumer_threads = []
    for i in range(num_consumers):
        thread = threading.Thread(
            target=consumer,
            args=(work_queue, i+1),
            name=f"Consumer-{i+1}"
        )
        thread.start()
        consumer_threads.append(thread)
    
    # Create and start producer thread
    producer_thread = threading.Thread(
        target=producer,
        args=(work_queue, num_items),
        name="Producer"
    )
    producer_thread.start()
    
    # Wait for producer to finish
    producer_thread.join()
    print("\n[Main] Producer finished. Waiting for consumers to finish work...")
    
    # Wait for all items to be processed
    work_queue.join()
    print("[Main] All items processed. Sending stop signals...")
    
    # Send stop signal to each consumer
    for _ in range(num_consumers):
        work_queue.put(None)
    
    # Wait for all consumers to finish
    for thread in consumer_threads:
        thread.join()
    
    print()
    print("=" * 60)
    print(f"All work completed! {num_items} items processed by {num_consumers} consumers.")
    print("=" * 60)


if __name__ == "__main__":
    main()


