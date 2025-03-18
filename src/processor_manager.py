import os
import psutil
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("TezosPasswordFinder")

class ProcessorManager:
    def __init__(self):
        self.cpu_count = psutil.cpu_count(logical=True)
        self.usable_cpus = max(1, self.cpu_count - 1)  # Leave one CPU free
        self.process = psutil.Process()
        self.thread_pool = None
        logger.info(f"Initialized ProcessorManager with {self.usable_cpus} usable CPUs")

    def set_affinity(self):
        """Set CPU affinity for the current process"""
        try:
            # Get all available CPU IDs
            all_cpus = list(range(self.cpu_count))
            # Remove the last CPU from the list
            working_cpus = all_cpus[:-1]
            # Set affinity
            self.process.cpu_affinity(working_cpus)
            logger.info(f"Set CPU affinity to CPUs {working_cpus}")
        except Exception as e:
            logger.error(f"Failed to set CPU affinity: {str(e)}")

    def create_thread_pool(self) -> ThreadPoolExecutor:
        """Create thread pool for password recovery"""
        self.thread_pool = ThreadPoolExecutor(
            max_workers=self.usable_cpus,
            thread_name_prefix="PasswordRecovery"
        )
        logger.info(f"Created thread pool with {self.usable_cpus} workers")
        return self.thread_pool

    def cleanup(self):
        """Cleanup resources"""
        if self.thread_pool:
            self.thread_pool.shutdown(wait=True)
            logger.info("Thread pool shut down")
