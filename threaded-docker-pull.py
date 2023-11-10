import docker
client = docker.from_env()
import argparse
import asyncio
import time
from threading import Thread

def worker_job(docker_list):
    # This prints the images being pulled then pulls them
    print(docker_list)
    image = client.images.pull(docker_list)

async def main():
    # Adds in the parameters and help for the script
    parser = argparse.ArgumentParser(description='Download Rancher images locally.')
    parser.add_argument('filename', help='Filename of image list')
    parser.add_argument('--workers', type=int, default=30, help='Number of Threads')
    args = parser.parse_args()
    parser.print_help()

    # Open the file from the parameter and read in every line
    file1 = open(args.filename, 'r')
    Lines = file1.readlines()
    total_sleep_time = 0
    started_at = time.monotonic()
    iteration = 1
    # Check the length of the file then iterate through it
    length = len(Lines)
    while length > 0:
        threads = []
        # Creates the pool of threads and then loops them until the total file has been parsed
        for i in range(args.workers):
            worker = Thread(target=worker_job, args=(Lines[length-1].strip(),))
            worker.setDaemon(True)
            worker.start()
            threads.append(worker)
            length = length -1
        for thread in threads:
            thread.join()
        iteration = iteration +1
    # Get the amount of time and number of total threads.
    total_slept_for = time.monotonic() - started_at
    total_workers = iteration * args.workers
    print('====')
    print(f'{total_workers} workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')

asyncio.run(main())
# main()