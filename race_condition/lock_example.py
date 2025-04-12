import threading
import time

# Shared variables
counter = 0
try_count = 1000
thread_num = 8
lock = threading.Lock()

def increment_counter():
    global counter
    for _ in range(try_count):
        # Complex operation to increase chance of GIL switching to another thread
        with lock:  # Acquire lock before accessing shared resource
            temp = counter
            # I/O operation to increase chance of GIL release
            with open('temp.txt', 'a') as f:
                f.write('1')
            counter = temp + 1

def main():
    # Create threads
    threads = []
    for _ in range(thread_num):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Print the final counter value
    print(f"Final counter value: {counter}")
    print(f"Expected value: {try_count * thread_num}")

if __name__ == "__main__":
    main() 