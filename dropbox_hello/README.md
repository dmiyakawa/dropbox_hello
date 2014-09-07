# What is this?

Django's Dropbox Hello World, or something like that.

# How to use this?

* Prepare an auth key and secret in Dropbox dev site.
* Put it in dropbox_hello/secrets.py, which is absent.
    * DROPBOX\_API\_KEY and DROPBOX\_API\_SECRET
* Prepare data/ directory and set appropriate permissions.
* All done.

# A Note (what I got stack).

We see "csrf token" in its API document.
Please be aware that the token is not relevant to
django's own csrf\_token things, but will be prepared
by the API itself.
We don't need to use csrf\_token handling
for this example,
because return\_uri is called with GET request, not POST.
@csrf\_exempt is meaningless there.

The Dropbox's own csrf token will be set
on DropboxOAuth2Flow.start()
and be checked on DropboxOAuth2Flow.finish().
Preparation and verification for the token
will be done by the API but
we need to remember the token on our side
via "session" stuff.
For this example I used a simple cookie
for remembering it.
You may want to use some model object
bound to a user instead.

If you haven't seen the demo in Python SDK,
I recommend to check it out.
Though it is not for django but for flask
(another Web application framework for Python),
it is still informative enough for django users too.

https://www.dropbox.com/developers/core/sdks/python

Enjoy.
