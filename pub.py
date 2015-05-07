from flask import Flask, render_template, request
from flask.ext.classy import FlaskView, route
import time
import cPickle
import copy
import urlparse
import urllib
import os
import requests

app = Flask(__name__)
app.config['subscribers_file']=os.path.join(
            os.path.dirname(__file__),
            "../db/subscriptions.pk"
)
class PubView(FlaskView):

    @route('/subscribe/', methods=['POST'])
    def receive_subscription(self):
        subscription = request.form
        lease_time = 2678400
        if request.method == 'POST':
            if not subscription['mode'] and not subscription['topic'] and \
                  not subscription['callback'] :
                return "Bad request: Expected 'hub.mode', 'hub.callback', and 'hub.topic'"
        to_verify = {'mode': subscription['mode'],
                     'topic': subscription['topic'],
                     'callback': subscription['callback'],
                     'lease': lease_time}
        return self.subscribe(to_verify)

    def subscribe(self, to_verify):
		challenge = self.base_n(abs(hash(time.time())),36)
		payload = {
			'hub.mode': to_verify['mode'],
			'hub.topic': to_verify['topic'],
			'hub.challenge': challenge
		}

		url = '?'.join([to_verify['callback'], urllib.urlencode(payload)])
		subscriber_saved = False
		try:
			response = requests.get(url).result()
			payload = response.content
			if challenge in payload:
				if to_verify['mode'] == 'subscribe':
					subscriber_saved == self.update_subscriber(to_verify['topic'],
                                           to_verify['callback'],
                                           to_verify['lease'],
                                           mode="subscribe")
				else:
					subscriber_saved = self.update_subscriber(to_verify['topic'],
                                           to_verify['callback'],
                                           to_verify['lease'],
                                           mode="unsubscribe")
			else:
				return 'what the.......'
		except Exception:
			return 'wowhahawowhaha'

		if subscriber_saved:
			return 'subscription verification successful'
		else:
			return 'Error saving subscriber to file'

    def update_subscriber(self, topic, subscriber_url, lease, mode="subscribe"):

		subscriptions = {}
		subscriptions = self.read_subscriptions()

		if not subscriptions:
			subscriptions = {}
		try:
			subscriptions[topic]
		except Exception:
			subscriptions[topic] = {}

		if mode == "subscribe":
			subscriptions[topic][subscriber_url] = time.time() + lease
		elif mode == "unsubscribe":
			if subscriber_url in subscriptions[topic]:
				del subscriptions[topic][subscriber_url]

		return self.save_subscriptions(subscriptions)

    def save_subscriptions(self, subscriptions):
        'Save subscribers to disk as a dict'

        filename = app.config['subscribers_file']

        subscriptions = self.verify_lease(subscriptions)
        sub_file = None
        try:
            sub_file = open(filename, 'wb')
            cPickle.dump(subscriptions, sub_file)
        except IOError as err:
            print(err)
            return None
        finally:
            if sub_file:
                sub_file.close()
        return True

    def varify_lease(self, subscriptions):
        current_time = time.time()
        subs = copy.deepcopy(subscriptions)
        for topic in list(subscriptions):
            for subscriber in subscriptions[topic]:
                if subscriptions[topic][subscriber] <= current_time:
                    del subs[topic][subscriber]
        return subs

    def base_n(self, num, bits, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        return ((num == 0) and "0") or \
            (self.base_n(num // bits, bits).lstrip("0") + numerals[num % bits])

PubView.register(app,  route_base="/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
