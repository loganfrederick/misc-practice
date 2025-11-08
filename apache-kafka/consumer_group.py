#!/usr/bin/env python3
"""
Kafka Consumer Group Example

This demonstrates how multiple consumers can work together in a consumer group
to process messages in parallel. This is useful for:

1. Load Balancing: Distribute work across multiple consumers
2. Scalability: Add more consumers to handle more messages
3. Fault Tolerance: If one consumer fails, others continue working

HOW TO USE:
1. Open 3 terminals
2. Run this script in each: python consumer_group.py
3. In a 4th terminal, run: python producer.py
4. Watch how messages are distributed across the 3 consumers!

Each consumer in the same group will receive different messages.
"""

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import signal
import sys
import random
import time


# Global flag for graceful shutdown
running = True
# Assign a random color for this consumer instance
COLORS = [
    '\033[91m',  # Red
    '\033[92m',  # Green
    '\033[93m',  # Yellow
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
]
COLOR = random.choice(COLORS)
RESET = '\033[0m'


def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shutdown the consumer."""
    global running
    print(f'\n\n{COLOR}Shutting down gracefully...{RESET}')
    running = False


def create_consumer(consumer_id):
    """
    Create and configure a Kafka consumer as part of a consumer group.
    
    Key configuration:
    - All consumers with the same group_id form a consumer group
    - Kafka automatically distributes partitions among group members
    - If a consumer joins/leaves, Kafka rebalances partitions
    """
    consumer = KafkaConsumer(
        'demo-topic',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        auto_commit_interval_ms=1000,
        group_id='load-balanced-consumer-group',  # Same group ID = same group
        client_id=f'consumer-{consumer_id}',  # Unique ID for this consumer
        consumer_timeout_ms=1000
    )
    return consumer


def process_message(message, consumer_id):
    """
    Process a single message.
    Each consumer in the group processes different messages.
    """
    value = message.value
    partition = message.partition
    offset = message.offset
    
    print(f"{COLOR}╔{'═' * 68}╗{RESET}")
    print(f"{COLOR}║ CONSUMER {consumer_id} - Message Received{' ' * 38}║{RESET}")
    print(f"{COLOR}╠{'═' * 68}╣{RESET}")
    print(f"{COLOR}║{RESET} Partition: {partition:<55} {COLOR}║{RESET}")
    print(f"{COLOR}║{RESET} Offset: {offset:<58} {COLOR}║{RESET}")
    print(f"{COLOR}║{RESET} Type: {value.get('type', 'unknown'):<60} {COLOR}║{RESET}")
    print(f"{COLOR}║{RESET} Data: {str(value.get('data', value.get('content', 'N/A')))[:60]:<60} {COLOR}║{RESET}")
    print(f"{COLOR}╚{'═' * 68}╝{RESET}")
    print()
    
    # Simulate some processing time
    time.sleep(0.1)


def consume_messages():
    """
    Main function that continuously consumes and processes messages
    as part of a consumer group.
    """
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate a random consumer ID
    consumer_id = random.randint(1000, 9999)
    
    print(f"{COLOR}{'=' * 70}{RESET}")
    print(f"{COLOR}KAFKA CONSUMER GROUP DEMO - Consumer {consumer_id}{RESET}")
    print(f"{COLOR}{'=' * 70}{RESET}")
    print()
    print(f"{COLOR}Connecting to Kafka...{RESET}")
    
    # Create the consumer
    consumer = create_consumer(consumer_id)
    
    print(f"{COLOR}✓ Connected!{RESET}")
    print(f"{COLOR}✓ Consumer ID: {consumer_id}{RESET}")
    print(f"{COLOR}✓ Group: load-balanced-consumer-group{RESET}")
    print(f"{COLOR}✓ Topic: demo-topic{RESET}")
    print()
    print(f"{COLOR}{'=' * 70}{RESET}")
    print(f"{COLOR}TIP: Run multiple instances of this script to see load balancing!{RESET}")
    print(f"{COLOR}     Each consumer will process different messages.{RESET}")
    print(f"{COLOR}{'=' * 70}{RESET}")
    print()
    print(f"{COLOR}Waiting for messages... (Press Ctrl+C to stop){RESET}")
    print()
    
    message_count = 0
    
    try:
        # Main consumption loop
        while running:
            for message in consumer:
                if not running:
                    break
                    
                message_count += 1
                
                try:
                    process_message(message, consumer_id)
                except Exception as e:
                    print(f"{COLOR}Error processing message: {e}{RESET}")
                    print(f"{COLOR}Continuing...{RESET}\n")
        
        print()
        print(f"{COLOR}{'=' * 70}{RESET}")
        print(f"{COLOR}Consumer {consumer_id} stopped. Processed {message_count} messages.{RESET}")
        print(f"{COLOR}{'=' * 70}{RESET}")
                    
    except KafkaError as e:
        print(f"{COLOR}Kafka error: {e}{RESET}")
    except Exception as e:
        print(f"{COLOR}Unexpected error: {e}{RESET}")
    finally:
        print(f"\n{COLOR}Closing consumer {consumer_id}...{RESET}")
        consumer.close()
        print(f"{COLOR}Goodbye!{RESET}")


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                   CONSUMER GROUP DEMONSTRATION                     ║
    ╠════════════════════════════════════════════════════════════════════╣
    ║                                                                    ║
    ║  This script demonstrates Kafka's consumer group feature.          ║
    ║                                                                    ║
    ║  TO SEE IT IN ACTION:                                              ║
    ║  1. Open 3 terminal windows                                        ║
    ║  2. Run this script in each: python consumer_group.py              ║
    ║  3. Open a 4th terminal and run: python producer.py                ║
    ║  4. Watch messages get distributed across the 3 consumers!         ║
    ║                                                                    ║
    ║  Each consumer gets DIFFERENT messages (load balancing).           ║
    ║  Try stopping one consumer - others take over its partitions!      ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to start this consumer...")
    print()
    
    consume_messages()

