import argparse
import os
import time
import requests
import threading
from multiprocessing import Process
import asyncio


def download_image(url):
    if not os.path.exists('images'):
        os.mkdir('images')
    start_time = time.time()
    name = url.split('/')[-1]
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f'images\\{name}', 'wb') as file:
            file.write(resp.content)
    print(f'время скачивания изображения({name}): {time.time() - start_time:.2f} сек.')


async def download_image_async(url):
    if not os.path.exists('images'):
        os.mkdir('images')
    start_time = time.time()
    name = url.split('/')[-1]
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f'images\\{name}', 'wb') as file:
            file.write(resp.content)
    print(f'время скачивания изображения({name}): {time.time() - start_time:.2f} сек.')


parser = argparse.ArgumentParser(description='Parser to start download_image')
parser.add_argument('-list', metavar='url', action='append', type=str, nargs='*', help='download_image sending URL')

args = parser.parse_args()

if __name__ == '__main__':

    start_time_all = time.time()

    threads = []
    for url in args.list[0]:
        thread = threading.Thread(target=download_image, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f'(Итог)время работы программы(многопоточный): {round(time.time() - start_time_all, 2)} сек.\n')

    full_time = time.time() - start_time_all

    start_time_all = time.time()
    processes = []
    for url_processes in args.list[0]:
        process = Process(target=download_image, args=(url_processes,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'(Итог)время работы программы(многопроцессорный): {round(time.time() - start_time_all, 2)} сек.\n')

    full_time += time.time() - start_time_all

    start_time_all = time.time()


    async def main():

        tasks = []
        for url_tasks in args.list[0]:
            tasks.append(asyncio.ensure_future(download_image_async(url_tasks)))
        await asyncio.gather(*tasks)


    asyncio.run(main())
    print(f'(Итог)время работы программы(с async): {round(time.time() - start_time_all, 2)} сек.\n')

    full_time += time.time() - start_time_all

    print(f'(Итог)Общее время работы программы: {round(full_time, 2)} сек.\n')
