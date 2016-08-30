import os
import bottle
from bottle import route, run, post, Response
from twilio import twiml
from twilio.rest import TwilioRestClient


app = bottle.default_app()
# plug in account SID and auth token here if they are not already exposed as
# environment variables
twilio_client = TwilioRestClient()

TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '+12025551234')
NGROK_BASE_URL = os.environ.get('NGROK_BASE_URL', 'https://c6c6d4e8.ngrok.io')


@route('/')
def index():
    """Returns standard text response to show app is up and running."""
    return Response("Bottle app running!")


@post('/twiml')
def twiml_response():
    """Provides TwiML instructions in response to a Twilio POST webhook
    event so that Twilio knows how to handle the outbound phone call
    when someone picks up the phone.
    """
    response = twiml.Response()
    response.say("Sweet, this phone call is answered by your Bottle app!")
    response.play("https://api.twilio.com/cowbell.mp3", loop=10)
    return Response(str(response))


@route('/dial-phone/<outbound_phone_number>')
def outbound_call(outbound_phone_number):
    """Uses the Twilio Python helper library to send a POST request to
    Twilio telling it to dial an outbound phone call from our
    specific Twilio phone number (that phone number must be owned by our
    Twilio account).
    """
    # the url must match the Ngrok Forwarding URL plus the route defined in
    # the previous function that responds with TwiML instructions
    twilio_client.calls.create(to=outbound_phone_number,
                               from_=BLOG_POST_NUMBER,
                               url=NGROK_BASE_URL + '/twiml')
    return Response('phone call placed to ' + outbound_phone_number + '!')


if __name__ == '__main__':
    run(host='127.0.0.1', port=8000, debug=False, reloader=True)
