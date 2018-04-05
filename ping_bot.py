from threading import Thread
import subprocess
from queue import Queue
import time
import telebot
token = 'your_telegram_token'

queue = Queue()
hosts = {'ESXi_VM1': '10.10.0.1', 'ESXi_VM2': '192.168.0.10',
         'TRN': '10.10.0.4', 'FreeNAS': '192.168.0.6',
         'ASKtele': '10.10.0.7', 'AppServer': '10.10.0.9',
         'Serv1: '192.168.0.5', 'googledns': '8.8.8.8'
        }

bot = telebot.TeleBot(token)
def pinger(i, q, phosts):
    time.sleep(i)
    host = q.get()
    print ("%s: ping %s..." % (i, phosts[i-1]))
    ret = subprocess.call("ping -n 1 %s" % host,
                        shell=True,
                        stdout=open('C:\ping_bot\log.txt', 'w'),
                        stderr=subprocess.STDOUT)
    if ret == 0:
        print('Host ' + phosts[i-1] +': ' + host + ' is up')
    else:
        print('Host ' + phosts[i-1] +': ' + host + ' is down')
        bot.send_message('your_id', 'Host ' + phosts[i-1] +': ' + host + ' is down')
    print('______________________________________________________')
    q.task_done()
while True:
    for i in range(1, len(hosts)+1):
        worker = Thread(target=pinger, args=(i, queue, list(hosts.keys())))
        worker.setDaemon(True)
        worker.start()
    
    for host in hosts.values():
        queue.put(host)
    time.sleep(180)
queue.join()