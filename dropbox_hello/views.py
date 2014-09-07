# -*- coding=utf-8 -*-

# DropboxClient
from dropbox.client import DropboxOAuth2Flow

from dropbox_hello.settings import SERVER_FQDN
from dropbox_hello.secrets import DROPBOX_API_KEY, DROPBOX_API_SECRET

from django.middleware.csrf import get_token
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from logging import getLogger
import traceback

logger = getLogger('dropbox_hello.debug')

# Key for CSRF key *FROM DROPBOX*.
# This is irrelevant to csrf_token provided by django.
DROPBOX_CSRF_KEY = 'dropbox-auth-csrf-token'

def get_auth_flow(request, session):
    redirect_uri = "https://{}{}".format(SERVER_FQDN, reverse('end_auth'))
    logger.debug('redirect_uri: {}'.format(redirect_uri))
    return DropboxOAuth2Flow(DROPBOX_API_KEY,
                             DROPBOX_API_SECRET,
                             redirect_uri,
                             session,
                             DROPBOX_CSRF_KEY)


def home(request):
    remote_addr = request.META.get('REMOTE_ADDR')
    logger.debug('home(IP: {})'.format(remote_addr))
    context = {'dropbox-auth-csrf-token': None,
               'mock-value': 'Hello!'}
    return render_to_response("home.djhtml", context)


def start_auth(request):
    remote_addr = request.META.get('REMOTE_ADDR')
    logger.debug('start_auth(IP: {})'.format(remote_addr))
    session = {}
    authorize_url = (get_auth_flow(request, session)
                     .start('hogehoge'))
    logger.debug('{}: {}'.format(DROPBOX_CSRF_KEY,
                                 session[DROPBOX_CSRF_KEY]))
    response = HttpResponseRedirect(authorize_url)
    response.set_cookie(DROPBOX_CSRF_KEY,
                        session[DROPBOX_CSRF_KEY])
    return response

    
# TODO: remove this
def end_auth(request):
    remote_addr = request.META.get('REMOTE_ADDR')
    logger.debug('end_auth(IP: {}, method: {})'
                 .format(remote_addr, request.method))
    try:
        query_args = request.GET
        #query_args = {u'state': get_token(request),
        #              u'code': request.GET.get(u'code')}
        dropbox_csrf_token = request.COOKIES.get(DROPBOX_CSRF_KEY)
        logger.debug('csrf: {}, query: {}'
                     .format(dropbox_csrf_token, query_args))
        session = {DROPBOX_CSRF_KEY: dropbox_csrf_token}
        result = (get_auth_flow(request, session).finish(query_args))
        access_token, user_id, url_state = result
        logger.debug('token: {}, id: {}, state: {}'
                     .format(access_token, user_id, url_state))
        context = {"token": None}
        return render_to_response("end_auth.djhtml", context)
    except DropboxOAuth2Flow.BadRequestException, e:
        logger.error('Exception raised: {}'.format(e))
        logger.error(traceback.format_exc())
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.BadStateException, e:
        logger.error('Exception raised: {}'.format(e))
        logger.error(traceback.format_exc())
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.CsrfException, e:
        logger.error('Exception raised: {}'.format(e))
        logger.error(traceback.format_exc())
        logger.debug('Bye')
        return HttpResponseForbidden()
    except DropboxOAuth2Flow.NotApprovedException, e:
        logger.error('Exception raised: {}'.format(e))
        logger.error(traceback.format_exc())
        return HttpResponseRedirect(reverse('home'))
    except DropboxOAuth2Flow.ProviderException, e:
        logger.info("Auth error: {}".format(e))
        return HttpResponseForbidden()

