import urllib
from google.appengine.api import urlfetch

API_SSL_SERVER = "https://www.google.com/recaptcha/api"
API_SERVER = "http://www.google.com/recaptcha/api"
VERIFY_SERVER = "www.google.com"


class RecaptchaResponse(object):
    def __init__(self, is_valid):
                    self.is_valid = is_valid


def displayhtml(public_key,
                use_ssl=False,
                error=None):
    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return """<script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>
        <noscript>
        <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
        <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
        <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
        </noscript>
        """ % {'ApiServer': server, 'PublicKey': public_key, 'ErrorParam': error_param}


def submit(recaptcha_challenge_field,
           recaptcha_response_field,
           private_key,
           remoteip):

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len(recaptcha_response_field) and len(recaptcha_challenge_field)):
        return RecaptchaResponse(is_valid=False, error_code='incorrect-captcha-sol')

    headers = {
        'Content-type':  'application/x-www-form-urlencoded',
        "User-agent":  "reCAPTCHA GAE Python"
    }

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
        'privatekey': encode_if_necessary(private_key),
        'remoteip': encode_if_necessary(remoteip),
        'challenge': encode_if_necessary(recaptcha_challenge_field),
        'response': encode_if_necessary(recaptcha_response_field),
    })

    httpresp = urlfetch.fetch(
        url="https://%s/recaptcha/api/verify" % VERIFY_SERVER,
        payload=params,
        method=urlfetch.POST,
        headers=headers)

    if httpresp.status_code == 200:
        return_values = httpresp.content.splitlines()
        return_code = return_values[0]
        if return_code == "true":
            return RecaptchaResponse(is_valid=True)
        else:
            return RecaptchaResponse(is_valid=False)
