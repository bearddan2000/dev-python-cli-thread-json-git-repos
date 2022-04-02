import requests, json
from queue import Queue
from data.threadcall import ThreadedCall

class CallApi(object):
    """docstring for callApi."""

    def __init__(self):
        from pprint import pprint
        results: Queue = Queue()
        th_lst: list = []
        repos = self.num_repos()
        for i in range(repos):
            th = ThreadedCall(i, results)
            th.start()
            th_lst.append(th)

        for t in th_lst:
            t.join()

        pprint(list(results.queue))

    def num_repos(self):
        from math import ceil
        response = requests.get('https://api.github.com/users/bearddan2000').text
        y = json.loads(response)
        return 30 # int(ceil(y[0]['public_repos']) / 100)
