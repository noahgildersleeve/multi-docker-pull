import docker
client = docker.from_env()
import argparse
import asyncio
import time
import tarfile
import gzip
from threading import Thread
import subprocess

def tar_docker(docker_list, tarName):
    started_at = time.monotonic()  
    images = []
    new_list=""
    for i in docker_list:
        new_list+=i.strip()+" "
    print(new_list)
    # This part is if you need to do this with gzip for any reason
    # process = subprocess.run("docker save " + new_list +" | gzip --stdout > "+ tarName, shell=True,
    #                      stdout=subprocess.PIPE, 
    #                      universal_newlines=True)
    # Creates the tar.gz file with pigz
    process = subprocess.run("docker save " + new_list +" | pigz -c -4 > "+ tarName, shell=True,
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    process
    print(process.stdout)
    total_time = time.monotonic() - started_at
    print('====')
    print(f' tar.gz process took {total_time:.2f} seconds')


def worker_job(docker_list):
    # This prints the images being pulled then pulls them
    print(docker_list)
    image = client.images.pull(docker_list)

def docker_prune():
    client.images.prune()

async def main():
    # Adds in the parameters and help for the script
    parser = argparse.ArgumentParser(description='Download Rancher images locally.')
    parser.add_argument('filename', help='Filename of image list')
    parser.add_argument('--workers', type=int, default=30, help='Number of Threads')
    parser.add_argument('--save', type=bool, default=False, help='bool for saving images to tar.gz')
    parser.add_argument('--tarName', default='rancher-images.tar.gz', help="Filename of output Tar")
    args = parser.parse_args()
    # parser.print_help()

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
    # Checks if save is true and tars the docker images
    if args.save:
        tar_docker(Lines, args.tarName)

    # Get the amount of time and number of total threads.
    total_slept_for = time.monotonic() - started_at
    total_workers = iteration * args.workers
    print('====')
    print(f'{total_workers} workers processed in parallel for {total_slept_for:.2f} seconds')

asyncio.run(main())
# main()