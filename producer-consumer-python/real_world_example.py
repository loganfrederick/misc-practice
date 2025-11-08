"""
Real-World Example: Download Simulator

This simulates a practical use case where:
- Producers discover URLs/tasks from different sources
- Consumers download and process the content
- Error handling and statistics are included

This pattern is commonly used for:
- Web scraping
- File processing pipelines
- API data collection
- Image/video processing
"""

import queue
import threading
import time
import random
from dataclasses import dataclass
from typing import List


@dataclass
class DownloadTask:
    """Represents a download task."""
    url: str
    source: str
    priority: int = 5  # 1-10, lower is higher priority
    
    def __lt__(self, other):
        """Enable priority comparison for PriorityQueue."""
        return self.priority < other.priority


class Statistics:
    """Thread-safe statistics collector."""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.total_discovered = 0
        self.total_processed = 0
        self.total_failed = 0
        self.processing_times = []
    
    def increment_discovered(self):
        with self.lock:
            self.total_discovered += 1
    
    def record_success(self, processing_time):
        with self.lock:
            self.total_processed += 1
            self.processing_times.append(processing_time)
    
    def increment_failed(self):
        with self.lock:
            self.total_failed += 1
    
    def get_summary(self):
        with self.lock:
            avg_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
            return {
                'discovered': self.total_discovered,
                'processed': self.total_processed,
                'failed': self.total_failed,
                'avg_time': avg_time
            }


def url_discoverer(q, stats, source, urls):
    """
    Simulates discovering URLs from a source (e.g., RSS feed, sitemap, API).
    
    Args:
        q: Queue to put tasks into
        stats: Statistics object
        source: Name of this source
        urls: List of URLs to discover
    """
    print(f"[Discoverer-{source}] Starting to discover URLs...")
    
    for url in urls:
        # Simulate discovery time
        time.sleep(random.uniform(0.1, 0.3))
        
        # Create task with random priority
        task = DownloadTask(
            url=url,
            source=source,
            priority=random.randint(1, 10)
        )
        
        q.put(task)
        stats.increment_discovered()
        print(f"[Discoverer-{source}] Found: {url} (priority: {task.priority})")
    
    print(f"[Discoverer-{source}] Finished discovering {len(urls)} URLs")


def downloader(q, stats, worker_id):
    """
    Simulates downloading and processing content.
    
    Args:
        q: Queue to get tasks from
        stats: Statistics object
        worker_id: Unique identifier for this worker
    """
    print(f"[Worker-{worker_id}] Ready to download...")
    
    while True:
        try:
            # Get task with timeout
            task = q.get(timeout=0.5)
            
            # Check for stop signal
            if task is None:
                q.task_done()
                break
            
            # Process the task
            print(f"[Worker-{worker_id}] Downloading: {task.url} (from {task.source})")
            
            start_time = time.time()
            
            # Simulate download time
            time.sleep(random.uniform(0.3, 1.0))
            
            # Simulate occasional failures (10% failure rate)
            if random.random() < 0.1:
                print(f"[Worker-{worker_id}] FAILED: {task.url}")
                stats.increment_failed()
            else:
                processing_time = time.time() - start_time
                print(f"[Worker-{worker_id}] SUCCESS: {task.url} ({processing_time:.2f}s)")
                stats.record_success(processing_time)
            
            q.task_done()
            
        except queue.Empty:
            # Queue is empty, continue waiting
            continue
    
    print(f"[Worker-{worker_id}] Shutting down")


def main():
    """Run the real-world example."""
    print("=" * 70)
    print("REAL-WORLD EXAMPLE: Multi-Source Download Simulator")
    print("=" * 70)
    print()
    
    # Simulate different sources of URLs
    sources = {
        "RSS-Feed": [
            "https://example.com/article1",
            "https://example.com/article2",
            "https://example.com/article3",
        ],
        "Sitemap": [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
            "https://example.com/page4",
        ],
        "API": [
            "https://api.example.com/data1",
            "https://api.example.com/data2",
            "https://api.example.com/data3",
        ]
    }
    
    # Configuration
    num_workers = 3
    
    # Create queue and statistics
    work_queue = queue.Queue()
    stats = Statistics()
    
    # Create and start discoverer threads (producers)
    discoverer_threads = []
    for source, urls in sources.items():
        thread = threading.Thread(
            target=url_discoverer,
            args=(work_queue, stats, source, urls),
            name=f"Discoverer-{source}"
        )
        thread.start()
        discoverer_threads.append(thread)
    
    # Create and start worker threads (consumers)
    worker_threads = []
    for i in range(num_workers):
        thread = threading.Thread(
            target=downloader,
            args=(work_queue, stats, i+1),
            name=f"Worker-{i+1}"
        )
        thread.start()
        worker_threads.append(thread)
    
    # Wait for all discoverers to finish
    for thread in discoverer_threads:
        thread.join()
    
    print("\n[Main] All sources discovered. Waiting for downloads to complete...")
    
    # Wait for all items to be processed
    work_queue.join()
    
    print("[Main] All downloads complete. Shutting down workers...")
    
    # Send stop signals to workers
    for _ in range(num_workers):
        work_queue.put(None)
    
    # Wait for all workers to finish
    for thread in worker_threads:
        thread.join()
    
    # Print statistics
    summary = stats.get_summary()
    print()
    print("=" * 70)
    print("FINAL STATISTICS")
    print("=" * 70)
    print(f"URLs Discovered:        {summary['discovered']}")
    print(f"Successfully Processed: {summary['processed']}")
    print(f"Failed:                 {summary['failed']}")
    print(f"Average Processing:     {summary['avg_time']:.2f} seconds")
    print(f"Success Rate:           {summary['processed'] / summary['discovered'] * 100:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()



