import docker
client = docker.from_env()
import argparse
import asyncio
import time
from threading import Thread

# SLEEP_FOR = random.uniform(0.05, 1.0)
# WORKER_NUMBER = 30
# FILE = 'rancher-images.txt'
def worker_job(docker_list):
    # This prints the images being pulled then pulls them
    print(docker_list)
    image = client.images.pull(docker_list)

async def main():
    # Adds in the parameters and help for the script
    parser = argparse.ArgumentParser(description='Download Rancher images locally.')
    parser.add_argument('filename', help='Filename of image list')           # positional argument
    parser.add_argument('--workers', type=int, default=30, help='Number of Threads')
    args = parser.parse_args()
    parser.print_help()

    # Generate random timings and put them into the queue.
    file1 = open(args.filename, 'r')
    Lines = file1.readlines()
    total_sleep_time = 0
    started_at = time.monotonic()
    iteration = 1
    # Create three worker tasks to process the queue concurrently.
    length = len(Lines)
    while length > 0:
        threads = []
        for i in range(args.workers):
            worker = Thread(target=worker_job, args=(Lines[length-1].strip(),))
            # task = loop.create_task(worker(line.strip))
            worker.setDaemon(True)
            worker.start()
            threads.append(worker)
            length = length -1
        for thread in threads:
            thread.join()
        iteration = iteration +1
    # Wait until the queue is fully processed.
    total_slept_for = time.monotonic() - started_at
    total_workers = iteration * args.workers
    print('====')
    print(f'{total_workers} workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')

asyncio.run(main())
# main()