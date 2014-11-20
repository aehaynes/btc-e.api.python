
import httplib
import urllib
import json
import hashlib
import hmac
import time
import sys

class api:
  __api_key = '';
  __api_secret  = '';
  __nonce_v = 1;
  __wait_for_nonce = False
  inf = sys.maxsize
  btce_domain = "btc-e.com"

  def __init__(self,api_key,api_secret,wait_for_nonce=False):
    self.__api_key = api_key
    self.__api_secret = api_secret
    self.__wait_for_nonce = wait_for_nonce

  def __nonce(self):
    if self.__wait_for_nonce: time.sleep(1)
    self.__nonce_v = str(time.time()).split('.')[0]

  def __signature(self, params):
    return hmac.new(self.__api_secret, params, digestmod=hashlib.sha512).hexdigest()

  def __api_call(self,method,params):
    self.__nonce()
    params['method'] = method
    params['nonce'] = str(self.__nonce_v)
    params = urllib.urlencode(params)
    headers = {"Content-type" : "application/x-www-form-urlencoded",
                      "Key" : self.__api_key,
         "Sign" : self.__signature(params)}
    conn = httplib.HTTPSConnection(self.btce_domain)
    conn.request("POST", "/tapi", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = json.load(response)
    conn.close()
    return data

  def get_param(self, couple, param):
    conn = httplib.HTTPSConnection(self.btce_domain)
    conn.request("GET", "/api/2/"+couple+"/"+param)
    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data

  def getInfo(self):
    return self.__api_call('getInfo', {})

  def TransHistory(self, **params):
    return self.__api_call('TransHistory', params)

  def TradeHistory(self, **params):
    return self.__api_call('TradeHistory', params)

  def ActiveOrders(self, **params):
    return self.__api_call('ActiveOrders', params)

  def Trade(self, tpair, ttype, trate, tamount):
    params = {
      "pair"  : tpair,
      "type"  : ttype,
      "rate"  : trate,
      "amount"  : tamount}
    return self.__api_call('Trade', params)

  def CancelOrder(self, torder_id):
    params = { "order_id" : torder_id }
    return self.__api_call('CancelOrder', params)
