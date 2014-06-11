# -*- coding:utf-8 -*-

import os
if os.path.exists('oauth2.db')== 'False':
    import get_token.py

import sqlite3
conn = sqlite3.connect('oauth2.db')
c = conn.cursor()
c.execute('''select * from token''')
oauth_token,oauth_token_secret = c.fetchone()
conn.close()


''' read the data '''
import time
import linecache
no = int(time.strftime("%j"))
message =  linecache.getline('data',no)


''' send message to fanfou.com '''
import urlparse,sys,urllib,re
import oauth2 as oauth
from urllib2 import Request,urlopen
consumer_key = 'api key'
consumer_secret = 'api key'

params={}
params['status']=message
url = 'http://api.fanfou.com/statuses/update.xml'
consumer = oauth.Consumer(consumer_key, consumer_secret)
token = oauth.Token(oauth_token,oauth_token_secret)
request = oauth.Request.from_consumer_and_token(consumer,
                                                token,                      
                                                http_url=url,              
                                                http_method='POST',
                                                parameters=params    
                                                )
signature_method = oauth.SignatureMethod_HMAC_SHA1()
request.sign_request(signature_method, consumer, token)
def request_to_header(request, realm=''):
    """Serialize as a header for an HTTPAuth request."""
    auth_header = 'OAuth realm="%s"' % realm
    for k, v in request.iteritems():
        if k.startswith('oauth_') or k.startswith('x_auth_'):
            auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    return {'Authorization': auth_header}

headers=request_to_header(request)
data = {'status':message}
data = urllib.urlencode(data)
resp = urlopen(Request(url,data=data,headers=headers))
resp = resp.read()
print resp


''' well done, I do it :) '''
