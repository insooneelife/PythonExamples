import asyncio
import aiofiles

# Shared variables
counter = 0
try_count = 1000
thread_num = 8

async def increment_counter():
    global counter
    for _ in range(try_count):
        # I/O operation is naturally non-blocking with async/await
        async with aiofiles.open('temp.txt', 'a') as f:
            await f.write('1')
        counter += 1  # This operation is atomic in Python

async def main():
    # Create tasks
    tasks = []
    for _ in range(thread_num):
        task = asyncio.create_task(increment_counter())
        tasks.append(task)
    
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)
    
    # Print the final counter value
    print(f"Final counter value: {counter}")
    print(f"Expected value: {try_count * thread_num}")

if __name__ == "__main__":
    asyncio.run(main()) 