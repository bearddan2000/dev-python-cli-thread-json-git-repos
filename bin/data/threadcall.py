import requests, json
from queue import Queue
from threading import Thread

class ThreadedCall(Thread):
    results_q: Queue
    url = "https://api.github.com/users/bearddan2000/repos?per_page=100&page="

    def __init__(self, index: int, q: Queue):
        Thread.__init__(self)
        self.url += str(index)
        self.results_q = q

    def filter_api(self, data: str, filter: list):
        if data in filter:
            return True
        return False

    def filter_field(self, data: str, filter: list):
        if self.filter_api(data, filter):
            return data
        return '-'

    def check_field_exits(self, data: str, index: int=0, filter: list=None):
        try:
            col: list = data.split("-")
            if len(col) > index:
                return self.filter_field(col[index], filter)
        except:
            return '-'

    def callGitApi(self):
        return requests.get(self.url).text

    def run(self):
        response = self.callGitApi()
        x = json.loads(response)
        for i in range(99):
            try:
                name = x[i]['name']
                # js = f'"name": {name}'
                self.results_q.put(name)
            except:
                self.results_q.put(i)
            '''
            if name:
                if self.filter_api(name, ['bearddan2000']) == False:
                    d: dict = {}
                    language = name.split('-')[0]
                    d['name'] = name
                    d['lang'] = language
                    d['platform'] = self.check_field_exits(name, 1, ['cli', 'desktop', 'web'])
                    d['build'] = self.check_field_exits(name, 2, ['ant', 'bazel', 'buckbuild', 'gradle'])
                    d['desc'] = self.check_field_exits(x[i]['description'])
                    d['url'] = x[i]['clone_url']
                    self.results_q.put(d)
            else:
                break
            '''
