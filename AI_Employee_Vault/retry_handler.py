#!/usr/bin/env python3
"""
Retry Handler Module

Provides retry logic with exponential backoff for transient errors.
Use as a decorator for functions that may fail temporarily.

Features:
- Exponential backoff
- Max retry limit
- Jitter to prevent thundering herd
- Custom retry conditions

Usage:
    @with_retry(max_attempts=3, base_delay=1)
    def send_email(...):
        # May fail transiently
        pass
"""

import time
import random
import logging
from functools import wraps
from typing import Callable, Any, Optional, Tuple


logger = logging.getLogger(__name__)


class TransientError(Exception):
    """Exception indicating a transient/retryable error."""
    pass


class PermanentError(Exception):
    """Exception indicating a permanent/non-retryable error."""
    pass


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Optional[Tuple] = None,
):
    """
    Decorator for retry logic with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff
        jitter: Whether to add random jitter to delay
        retryable_exceptions: Tuple of exception types to retry (default: Exception)
    
    Returns:
        Decorated function with retry logic
    
    Example:
        @with_retry(max_attempts=5, base_delay=2)
        def call_api():
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
    """
    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                    
                except retryable_exceptions as e:
                    last_exception = e
                    
                    # Don't retry on last attempt
                    if attempt == max_attempts:
                        logger.error(f"{func.__name__}: Max attempts ({max_attempts}) reached")
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)
                    
                    # Add jitter (±25%)
                    if jitter:
                        jitter_factor = random.uniform(0.75, 1.25)
                        delay *= jitter_factor
                    
                    logger.warning(
                        f"{func.__name__}: Attempt {attempt}/{max_attempts} failed: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    # Non-retryable exception
                    logger.error(f"{func.__name__}: Non-retryable error: {e}")
                    raise
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def retry_with_timeout(
    func: Callable,
    *args,
    timeout: float = 30.0,
    max_attempts: int = 3,
    **kwargs
) -> Any:
    """
    Retry a function with timeout per attempt.
    
    Args:
        func: Function to retry
        timeout: Timeout per attempt in seconds
        max_attempts: Maximum retry attempts
        *args: Arguments to pass to function
        **kwargs: Keyword arguments to pass to function
    
    Returns:
        Function result
    
    Raises:
        TimeoutError: If all attempts timeout
        Exception: If all attempts fail
    """
    import signal
    
    last_exception = None
    
    for attempt in range(1, max_attempts + 1):
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Function timed out after {timeout}s")
        
        # Set timeout (Unix only)
        if os.name != 'nt':
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout))
        
        try:
            result = func(*args, **kwargs)
            
            # Cancel alarm
            if os.name != 'nt':
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            
            return result
            
        except TimeoutError as e:
            last_exception = e
            logger.warning(f"Attempt {attempt}/{max_attempts} timed out")
            
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}")
            
        finally:
            # Cancel alarm if still set
            if os.name != 'nt':
                signal.alarm(0)
        
        # Delay between attempts
        if attempt < max_attempts:
            delay = min(2 ** (attempt - 1), 30)
            time.sleep(delay)
    
    if last_exception:
        raise last_exception
    
    raise RuntimeError("Unexpected state in retry_with_timeout")


class RetryManager:
    """
    Class-based retry manager for complex retry scenarios.
    
    Features:
    - Track retry statistics
    - Circuit breaker pattern
    - Custom retry strategies
    
    Usage:
        manager = RetryManager(max_attempts=5)
        
        @manager.retry
        def flaky_function():
            ...
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        
        # Statistics
        self.total_attempts = 0
        self.successful_attempts = 0
        self.failed_attempts = 0
    
    def retry(self, func: Callable) -> Callable:
        """Decorator for retry logic."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.total_attempts += 1
            
            for attempt in range(1, self.max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    self.successful_attempts += 1
                    return result
                    
                except Exception as e:
                    if attempt == self.max_attempts:
                        self.failed_attempts += 1
                        raise
                    
                    delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
                    logger.warning(f"Retry {attempt}/{self.max_attempts}: {e}")
                    time.sleep(delay)
            
            raise RuntimeError("Unexpected retry state")
        
        return wrapper
    
    def get_stats(self) -> dict:
        """Get retry statistics."""
        return {
            'total_attempts': self.total_attempts,
            'successful': self.successful_attempts,
            'failed': self.failed_attempts,
            'success_rate': (
                self.successful_attempts / self.total_attempts
                if self.total_attempts > 0 else 0
            )
        }


# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    @with_retry(max_attempts=3, base_delay=1)
    def example_function():
        import random
        if random.random() < 0.7:
            raise TransientError("Random failure")
        return "Success!"
    
    print("Testing retry logic...")
    for i in range(5):
        try:
            result = example_function()
            print(f"Call {i+1}: {result}")
        except Exception as e:
            print(f"Call {i+1}: Failed - {e}")
    
    print("\nRetry statistics complete!")
