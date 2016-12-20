import threading
import time
import random
import urllib2
import unittest
from bs4 import BeautifulSoup
from threading import Thread, Condition


queue = []
MAX_NUM = 10
condition = Condition()


class ProducerThread(Thread):
    
    def run(self):
        with open('links.txt') as f:
            urls = f.readlines()
        nums = range(0,len(urls))
        global queue
        while True:
            condition.acquire()
            if len(queue) == MAX_NUM:
                print "Queue full, producer is waiting"
                condition.wait()
                print "Space in queue, Consumer notified the producer"
            num = random.choice(nums)
            queue.append(num)
            url = urls[num]
            print "Produced", url
            condition.notify()
            condition.release()
            time.sleep(random.random())


class ConsumerThread(Thread):
    def run(self):
        with open('links.txt') as f:
            urls = f.readlines()
        global queue
        while True:
            condition.acquire()
            if not queue:
                print "Nothing in queue, consumer is waiting"
                condition.wait()
                print "Producer added something to queue and notified the consumer"
            num = queue.pop(0)
            try:
                url = urllib2.urlopen(urls[num])
                chunk = url.read()
                soup = BeautifulSoup(chunk, "lxml")
                print soup.findAll(['title'])
                print "Consumed", num
                condition.notify()
                condition.release()
                time.sleep(random.random())

            except:
                print "failed to load url"
                print "Consumed", num
                condition.notify()
                condition.release()
                time.sleep(random.random())
                continue
                
            
ProducerThread().start()
ConsumerThread().start()
