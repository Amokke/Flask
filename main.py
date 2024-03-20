import argparse
import os
import time
import requests
import threading
from multiprocessing import Process


def download_image(url_synchronous):
    """Функция, которая скачивает изображения с заданного URL-адреса(и выводит время работы в консоль)"""
    if not os.path.exists('images'):
        os.mkdir('images')
    start_time = time.time()
    name = url_synchronous.split('/')[-1]
    resp = requests.get(url_synchronous)
    if resp.status_code == 200:
        with open(f'images\\{name}', 'wb') as file:
            file.write(resp.content)
    print(f'время скачивания изображения({name}): {time.time() - start_time:.2f} сек.')


start_time_all = time.time()

parser = argparse.ArgumentParser(description='Parser to start download_image')
parser.add_argument('-list', metavar='url', action='append', type=str, nargs='*', help='download_image sending URL')

args = parser.parse_args()

threads = []
for url in args.list[0]:
    thread = threading.Thread(target=download_image, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
print(f'(Итог)время работы программы(многопоточный): {round(time.time() - start_time_all, 2)} сек.\n')

if __name__ == '__main__':
    processes = []
    for url_processes in args.list[0]:
        process = Process(target=download_image, args=(url_processes,))
        processes.append(process)
    process.start()

    for process in processes:
        process.join()

    print(f'(Итог)время работы программы(многопроцессорный): {round(time.time() - start_time_all, 2)} сек.\n')

print(f'Общее времени выполнения программы: {time.time() - start_time_all:.2f}')
