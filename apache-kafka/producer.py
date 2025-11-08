#!/usr/bin/env python3
"""
Kafka Producer Example

This script demonstrates how to send messages to a Kafka topic.
A producer is responsible for:
1. Creating messages
2. Sending them to a specific topic
3. Handling delivery confirmations
"""

from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
from datetime import datetime


def create_producer():
    """
    Create and configure a Kafka producer.
    
    The producer serializes messages to JSON format before sending.
    """
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],  # Kafka broker address
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Convert dict to JSON
        acks='all',  # Wait for all replicas to acknowledge (most reliable)
        retries=3,   # Retry failed sends up to 3 times
        max_in_flight_requests_per_connection=1  # Ensure ordering
    )
    return producer


def on_send_success(record_metadata):
    """
    Callback function called when a message is successfully sent.
    
    Args:
        record_metadata: Information about where the message was stored
    """
    print(f"✓ Message sent successfully!")
    print(f"  Topic: {record_metadata.topic}")
    print(f"  Partition: {record_metadata.partition}")
    print(f"  Offset: {record_metadata.offset}")
    print(f"  Timestamp: {record_metadata.timestamp}")
    print()


def on_send_error(exc):
    """
    Callback function called when sending a message fails.
    
    Args:
        exc: The exception that occurred
    """
    print(f"✗ Error sending message: {exc}")
    print()


def send_messages():
    """
    Main function that sends various types of messages to demonstrate
    different producer patterns.
    """
    print("=" * 60)
    print("KAFKA PRODUCER DEMO")
    print("=" * 60)
    print()
    
    # Create the producer
    print("Connecting to Kafka broker at localhost:9092...")
    producer = create_producer()
    print("Connected!\n")
    
    topic = 'demo-topic'
    
    try:
        # Example 1: Simple message
        print("Example 1: Sending a simple text message")
        print("-" * 60)
        message1 = {
            'type': 'greeting',
            'content': 'Hello, Kafka!',
            'timestamp': datetime.now().isoformat()
        }
        future = producer.send(topic, value=message1)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)
        time.sleep(1)  # Give time for callback to execute
        
        # Example 2: User event
        print("Example 2: Sending a user event")
        print("-" * 60)
        message2 = {
            'type': 'user_action',
            'user_id': 12345,
            'action': 'button_click',
            'button': 'submit',
            'timestamp': datetime.now().isoformat()
        }
        future = producer.send(topic, value=message2)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)
        time.sleep(1)
        
        # Example 3: Order event
        print("Example 3: Sending an order event")
        print("-" * 60)
        message3 = {
            'type': 'order',
            'order_id': 'ORD-98765',
            'customer_id': 54321,
            'items': [
                {'product': 'Laptop', 'quantity': 1, 'price': 999.99},
                {'product': 'Mouse', 'quantity': 2, 'price': 29.99}
            ],
            'total': 1059.97,
            'timestamp': datetime.now().isoformat()
        }
        future = producer.send(topic, value=message3)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)
        time.sleep(1)
        
        # Example 4: Batch of messages
        print("Example 4: Sending a batch of messages")
        print("-" * 60)
        for i in range(5):
            message = {
                'type': 'batch_message',
                'sequence': i + 1,
                'data': f'Batch message number {i + 1}',
                'timestamp': datetime.now().isoformat()
            }
            producer.send(topic, value=message)
            print(f"  Queued message {i + 1}/5")
        
        # Flush ensures all queued messages are sent
        print("\nFlushing producer queue...")
        producer.flush()
        print("All messages sent!")
        print()
        
        # Example 5: High-throughput simulation
        print("Example 5: Sending 10 messages rapidly")
        print("-" * 60)
        start_time = time.time()
        for i in range(10):
            message = {
                'type': 'high_throughput',
                'message_id': i + 1,
                'data': f'High-speed message {i + 1}',
                'timestamp': datetime.now().isoformat()
            }
            producer.send(topic, value=message)
        
        producer.flush()
        elapsed = time.time() - start_time
        print(f"✓ Sent 10 messages in {elapsed:.3f} seconds")
        print(f"  Throughput: {10/elapsed:.1f} messages/second")
        print()
        
    except KafkaError as e:
        print(f"Kafka error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Always close the producer to release resources
        print("Closing producer...")
        producer.close()
        print("Producer closed. Goodbye!")


if __name__ == '__main__':
    send_messages()

