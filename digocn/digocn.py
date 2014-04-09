#########################################################################
# Copyright 2014 Cloud Sidekick
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################

import urllib2
import httplib
import base64
import re
import time
import json

class DigOcnConn():
    """Example:
    conn = digocn.DigOcnConn(user, password, timeout, debug=True)
    """

    def __init__(self, client_id, api_key, timeout=5, debug=False):
        """Initiallizes the DigOcnConn class.

        Will automatically use parameters and establish connection to Digital Ocean
        
        Arguments:
        client_id -- Digital Ocean Client Id
        api_key -- Digital Ocean API key
        timeout -- optional, timeout in seconds for all http connections with, default 5
        debug -- optional, prints html responses from the api endpoint, True or False (default)
        """
        
        self.timeout = timeout
        self.debug = debug
        self.base_url = "https://api.digitalocean.com"
        self.client_id = client_id
        self.api_key = api_key


    def call(self, noun, action=None, subject=None, params={}):
        """Constructs the Digital Ocean api request to send"""

        url = "%s/%s" % (self.base_url, noun)
        if subject:
            url = "%s/%s" % (url, subject)
        if action:
            url = "%s/%s" % (url, action)
        params["client_id"] = self.client_id
        params["api_key"] = self.api_key
        query_string = '&'.join(['%s=%s' % (k,urllib2.quote(str(v))) for (k,v) in params.items()])
        url = "%s?%s" % (url, query_string)
        url = url.replace(" ", "+")
        if self.debug:
            print url
        req = urllib2.Request(url)
        response = self._send_request(req, timeout=self.timeout)
        return json.loads(response)

    def _send_request(self, req, timeout=None):
        """Sends the request and handles errors"""

        reattempt = True
        attempt = 1
        reattempt_http_codes = []
        delay = 1
        attempts_allowed = 10
        if not timeout:
            timeout = self.timeout 
        while reattempt is True and attempt <= attempts_allowed:
            try:
                response = urllib2.urlopen(req, timeout=timeout)
            except urllib2.HTTPError, e:
                if e.code in reattempt_http_codes and attempt < attempts_allowed:
                    print("HTTPError, will reattempt = %s, %s, %s\n%s" % (str(e.code), e.msg, e.read(), req.get_full_url()))
                    attempt += 1
                    time.sleep(delay)
                    continue
                else:
                    raise Exception("HTTPError = %s, %s, %s\n%s" % (str(e.code), e.msg, e.read(), req.get_full_url()))
            except urllib2.URLError, e:
                raise Exception("URLError = %s\n%s" % (str(e.reason), req.get_full_url()))
            except httplib.HTTPException, e:
                raise Exception("HTTPException")
            except Exception:
                import traceback
                raise Exception("generic exception: " + traceback.format_exc())
            else:
                # got here, request was successful, break out
                reattempt = False

        r = response.read()
        if self.debug:
            print(response.info())
            print(r)

        return r
