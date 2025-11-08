#!/usr/bin/env python3
"""
Kafka Consumer Example

This script demonstrates how to consume messages from a Kafka topic.
A consumer is responsible for:
1. Subscribing to one or more topics
2. Reading messages in order (within a partition)
3. Processing the messages
4. Tracking progress (offsets)
"""

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import signal
import sys


# Global flag for graceful shutdown
running = True


def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shutdown the consumer."""
    global running
    print('\n\nShutting down gracefully...')
    running = False


def create_consumer():
    """
    Create and configure a Kafka consumer.
    
    The consumer deserializes JSON messages and handles automatic offset commits.
    """
    consumer = KafkaConsumer(
        'demo-topic',  # Topic to subscribe to
        bootstrap_servers=['localhost:9092'],  # Kafka broker address
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # Parse JSON
        auto_offset_reset='earliest',  # Start from beginning if no offset exists
        enable_auto_commit=True,  # Automatically commit offsets
        auto_commit_interval_ms=1000,  # Commit every second
        group_id='demo-consumer-group',  # Consumer group ID
        consumer_timeout_ms=1000  # Return if no message received in 1 second
    )
    return consumer


def process_message(message):
    """
    Process a single message from Kafka.
    
    In a real application, this might:
    - Save data to a database
    - Call an external API
    - Update a cache
    - Trigger business logic
    
    Args:
        message: The Kafka message object
    """
    # Extract message metadata
    topic = message.topic
    partition = message.partition
    offset = message.offset
    key = message.key
    value = message.value
    timestamp = message.timestamp
    
    # Print header
    print("=" * 70)
    print(f"📨 NEW MESSAGE RECEIVED")
    print("=" * 70)
    
    # Print metadata
    print(f"Topic:      {topic}")
    print(f"Partition:  {partition}")
    print(f"Offset:     {offset}")
    print(f"Key:        {key}")
    print(f"Timestamp:  {timestamp}")
    print()
    
    # Print message content
    print("Message Content:")
    print("-" * 70)
    print(json.dumps(value, indent=2))
    print("-" * 70)
    
    # Simulate processing based on message type
    message_type = value.get('type', 'unknown')
    
    if message_type == 'greeting':
        print("💬 Processing greeting message...")
        print(f"   Content: {value.get('content')}")
        
    elif message_type == 'user_action':
        print("👤 Processing user action...")
        print(f"   User {value.get('user_id')} performed action: {value.get('action')}")
        
    elif message_type == 'order':
        print("🛒 Processing order...")
        order_id = value.get('order_id')
        total = value.get('total')
        item_count = len(value.get('items', []))
        print(f"   Order {order_id} with {item_count} items, total: ${total}")
        
    elif message_type == 'batch_message':
        print("📦 Processing batch message...")
        print(f"   Sequence: {value.get('sequence')}")
        
    elif message_type == 'high_throughput':
        print("⚡ Processing high-throughput message...")
        print(f"   Message ID: {value.get('message_id')}")
        
    else:
        print("❓ Processing unknown message type...")
    
    print("\n✓ Message processed successfully!\n")


def consume_messages():
    """
    Main function that continuously consumes and processes messages.
    """
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 70)
    print("KAFKA CONSUMER DEMO")
    print("=" * 70)
    print()
    print("Connecting to Kafka broker at localhost:9092...")
    
    # Create the consumer
    consumer = create_consumer()
    
    print("✓ Connected successfully!")
    print(f"✓ Subscribed to topic: demo-topic")
    print(f"✓ Consumer group: demo-consumer-group")
    print()
    print("Waiting for messages... (Press Ctrl+C to stop)")
    print("=" * 70)
    print()
    
    message_count = 0
    
    try:
        # Main consumption loop
        while running:
            # Poll for messages (with timeout)
            # This returns a batch of messages, but we iterate one by one
            for message in consumer:
                if not running:
                    break
                    
                message_count += 1
                
                try:
                    # Process the message
                    process_message(message)
                    
                except Exception as e:
                    print(f"Error processing message: {e}")
                    print("Continuing to next message...\n")
        
        print()
        print("=" * 70)
        print(f"Consumer stopped. Processed {message_count} messages.")
        print("=" * 70)
                    
    except KafkaError as e:
        print(f"Kafka error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Always close the consumer to clean up resources
        print("\nClosing consumer...")
        consumer.close()
        print("Consumer closed. Goodbye!")


if __name__ == '__main__':
    consume_messages()

