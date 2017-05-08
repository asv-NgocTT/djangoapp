from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import webapp2
COUNTER_KEY = 'default counter'


class Counter(ndb.Model):
    count = ndb.IntegerProperty(indexed=False)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        counter = Counter.get_by_id(COUNTER_KEY)
        count = counter.count if counter else 0

        self.response.write("""
            Count: {count}<br>
            <form method="post" action="/enqueue">
                <label>Increment amount</label>
                <input name="amount" value="1">
                <button>Enqueue task</button>
            </form>
        """.format(count=count))


class EnqueueTaskHandler(webapp2.RequestHandler):
    def post(self):
        amount = int(self.request.get('amount'))

        task = taskqueue.add(
            url='/update_counter',
            target='worker',
            params={'amount': amount})

        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


# AsyncEnqueueTaskHandler behaves the same as EnqueueTaskHandler, but shows
# how to queue the task using the asyncronous API. This is not wired up by
# default. To use this, change the MainPageHandler's form action to
# /enqueue_async
class AsyncEnqueueTaskHandler(webapp2.RequestHandler):
    def post(self):
        amount = int(self.request.get('amount'))

        queue = taskqueue.Queue(name='default')
        task = taskqueue.Task(
            url='/update_counter',
            target='worker',
            params={'amount': amount})

        rpc = queue.add_async(task)

        # Wait for the rpc to complete and return the queued task.
        task = rpc.get_result()

        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/enqueue', EnqueueTaskHandler),
    ('/enqueue_async', AsyncEnqueueTaskHandler)
], debug=True)
