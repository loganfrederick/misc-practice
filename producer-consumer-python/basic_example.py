"""
Basic Producer-Consumer Example

This demonstrates the fundamental producer-consumer pattern with:
- One producer thread that generates numbers
- One consumer thread that processes numbers
- A queue to connect them safely
"""

import queue
import threading
import time
import random


def producer(q, num_items):
    """
    Producer function that generates work items.
    
    Args:
        q: The queue to put items into
        num_items: Number of items to produce
    """
    print("Producer: Starting...")
    
    for i in range(num_items):
        # Simulate some work to produce an item
        time.sleep(random.uniform(0.1, 0.5))
        
        item = f"Item-{i}"
        q.put(item)
        print(f"Producer: Created {item} (Queue size: {q.qsize()})")
    
    # Send sentinel value to signal completion
    q.put(None)
    print("Producer: Done! Sent stop signal.")


def consumer(q):
    """
    Consumer function that processes work items.
    
    Args:
        q: The queue to get items from
    """
    print("Consumer: Starting...")
    
    while True:
        # Get item from queue (blocks if empty)
        item = q.get()
        
        # Check for stop signal
        if item is None:
            print("Consumer: Received stop signal.")
            q.task_done()
            break
        
        # Process the item (simulate work)
        print(f"Consumer: Processing {item}...")
        time.sleep(random.uniform(0.2, 0.8))
        print(f"Consumer: Finished {item}")
        
        # Mark task as done
        q.task_done()
    
    print("Consumer: Shutting down.")


def main():
    """Run the basic producer-consumer example."""
    print("=" * 60)
    print("BASIC PRODUCER-CONSUMER EXAMPLE")
    print("=" * 60)
    print()
    
    # Create a queue with unlimited size
    work_queue = queue.Queue()
    
    # Number of items to produce
    num_items = 5
    
    # Create and start producer thread
    producer_thread = threading.Thread(
        target=producer,
        args=(work_queue, num_items),
        name="Producer"
    )
    
    # Create and start consumer thread
    consumer_thread = threading.Thread(
        target=consumer,
        args=(work_queue,),
        name="Consumer"
    )
    
    # Start both threads
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for producer to finish
    producer_thread.join()
    
    # Wait for all items to be processed
    work_queue.join()
    
    # Wait for consumer to finish
    consumer_thread.join()
    
    print()
    print("=" * 60)
    print("All work completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()


