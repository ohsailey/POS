from flask import Flask, render_template, request
from flask.ext.classy import FlaskView, route
import requests

app = Flask(__name__)



class PubSubView(FlaskView):

	@route('/send_subscription/', methods=['GET','POST'], endpoint='transmit')
	def transmit(self):
		error = None
		if request.method == 'POST':

			if len(request.form['pub_url']) == 0 or len(request.form['topic_url']) == 0 or \
					len(request.form['callback_url']) == 0 :
				error = 'please fill in your subscription form'
			else :
				headers = {'content-type': 'application/x-www-form-urlencoded'}
    			payload = {
        			'mode': 'subscribe',
        			'topic': request.form['topic_url'],
        			'callback': request.form['callback_url']}

        		pub_url = request.form['pub_url']

        		r = requests.post(pub_url, data=payload, headers=headers)
        		error = 'Subscription request sent to the hub'
		return render_template('login.html', error=error)

	@route('/callback/', methods=['POST'])
	def process_subscription_challenge(self):
		print 'callback'
		args = urlparse.parse_qs(self._env.get('QUERY_STRING', None))
		challenge = args.get('hub.challenge', [None])[0]
		if not challenge:
			return self.respond(code=400, msg="Bad Request.")
		return self.respond(code=200, msg=challenge)

	'''def update_subscriber(self, topic, subscriber_url, lease,
                          mode="subscribe"):
        """
        Given the topic, subscriber url and lease time, this method
        adds a new subscriber and saves it.
        """

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

        filename = self.config['subscribers_file']

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

    def read_subscriptions(self):
        "Read subscriber's list from file"

        filename = self.config['subscribers_file']

        data = {}
        sub_file = None
        try:
            # using 'r+b' file permissions here so that the
            # file gets created if there is none.
            sub_file = open(filename, "r+b")
            data = cPickle.load(sub_file)
        except (IOError, EOFError) as err:
            print(err)
            return None
        finally:
            if sub_file:
                sub_file.close()
        return self.verify_lease(data)

    def verify_lease(self, subscriptions):
        """
        Loop through the dict of subscribers and del all the subscriptions
        that are past their lease time.
        """

        current_time = time.time()
        subs = copy.deepcopy(subscriptions)
        for topic in list(subscriptions):
            for subscriber in subscriptions[topic]:
                if subscriptions[topic][subscriber] <= current_time:
                    del subs[topic][subscriber]
        return subs

    def base_n(self, num, bits,
               numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        """
        Creates a unique hash for subscription verification.
        Taken from: https://github.com/progrium/wolverine/blob/master/\
            miyamoto/pubsub.py
        """

        return ((num == 0) and "0") or \
            (self.base_n(num // bits, bits).lstrip("0") + numerals[num % bits])'''


	'''def subscribe(subscription):
		cha'''

PubSubView.register(app,  route_base="/")

if __name__ == '__main__':
    app.run(debug=True, port=8010)