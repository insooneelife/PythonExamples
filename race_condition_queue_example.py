import threading
from queue import Queue
import time

# Shared variables
try_count = 1000
thread_num = 8

def increment_counter(q):
    for _ in range(try_count):
        # Complex operation to increase chance of GIL switching to another thread
        temp = q.get()  # Get current value from queue
        # I/O operation to increase chance of GIL release
        with open('temp.txt', 'a') as f:
            f.write('1')
        q.put(temp + 1)  # Put incremented value back to queue

def main():
    # Initialize queue with starting value 0
    q = Queue()
    q.put(0)
    
    # Create threads
    threads = []
    for _ in range(thread_num):
        thread = threading.Thread(target=increment_counter, args=(q,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Get final value from queue
    final_value = q.get()
    
    # Print the final counter value
    print(f"Final counter value: {final_value}")
    print(f"Expected value: {try_count * thread_num}")

if __name__ == "__main__":
    main() 