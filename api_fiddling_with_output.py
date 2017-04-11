In [1]: from temba_client.v2 import TembaClient

In [2]: client = TembaClient('rapidpro.io', open('token').read())

In [3]: client.get_flows()
Out[3]: <temba_client.clients.CursorQuery at 0x7fcf081b9e10>

In [4]: list(client.get_flows())
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-3adda10cf3a5> in <module>()
----> 1 list(client.get_flows())

TypeError: 'CursorQuery' object is not iterable

In [5]: a = client.get_flows().iterfetches()

In [6]: a
Out[6]: <temba_client.clients.CursorIterator at 0x7fcf08107350>

In [7]: list(a)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-7-61edcfee5862> in <module>()
----> 1 list(a)

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/six.pyc in next(self)
    556 
    557         def next(self):
--> 558             return type(self).__next__(self)
    559 
    560     callable = callable

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/clients.pyc in __next__(self)
    273 
    274         response = self.client._request('get', self.url, params=self.params,
--> 275                                         retry_on_rate_exceed=self.retry_on_rate_exceed)
    276 
    277         self.url = response['next']

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/clients.pyc in _request(self, method, url, params, body, retry_on_rate_exceed)
    350             return self._request_wth_rate_limit_retry(method, url, params=params, body=body)
    351         else:
--> 352             return super(BaseCursorClient, self)._request(method, url, params=params, body=body)
    353 
    354     def _request_wth_rate_limit_retry(self, method, url, params=None, body=None):

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/clients.pyc in _request(self, method, url, params, body)
     86             kwargs['verify'] = self.verify_ssl
     87 
---> 88             response = request(method, url, **kwargs)
     89 
     90             if response.status_code == 400:

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/utils.pyc in request(method, url, **kwargs)
     52         kwargs['data'] = json.dumps(kwargs['data'])
     53 
---> 54     return requests.request(method, url, **kwargs)

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/requests/api.pyc in request(method, url, **kwargs)
     54     # cases, and look like a memory leak in others.
     55     with sessions.Session() as session:
---> 56         return session.request(method=method, url=url, **kwargs)
     57 
     58 

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/requests/sessions.pyc in request(self, method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
    486         }
    487         send_kwargs.update(settings)
--> 488         resp = self.send(prep, **send_kwargs)
    489 
    490         return resp

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/requests/sessions.pyc in send(self, request, **kwargs)
    607 
    608         # Send the request
--> 609         r = adapter.send(request, **kwargs)
    610 
    611         # Total elapsed time of the request (approximately)

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/requests/adapters.pyc in send(self, request, stream, timeout, verify, cert, proxies)
    421                     decode_content=False,
    422                     retries=self.max_retries,
--> 423                     timeout=timeout
    424                 )
    425 

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/requests/packages/urllib3/connectionpool.pyc in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
    598                                                   timeout=timeout_obj,
    599                                                   body=body, headers=headers,
--> 600                                                   chunked=chunked)
    601 
    602             # If we're going to release the connection in ``finally:``, then

/home/robert/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/requests/packages/urllib3/connectionpool.pyc in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
    354             conn.request_chunked(method, url, **httplib_request_kw)
    355         else:
--> 356             conn.request(method, url, **httplib_request_kw)
    357 
    358         # Reset the timeout for the recv() on the socket

/usr/lib/python2.7/httplib.pyc in request(self, method, url, body, headers)
   1055     def request(self, method, url, body=None, headers={}):
   1056         """Send a complete request to the server."""
-> 1057         self._send_request(method, url, body, headers)
   1058 
   1059     def _set_content_length(self, body, method):

/usr/lib/python2.7/httplib.pyc in _send_request(self, method, url, body, headers)
   1094             self._set_content_length(body, method)
   1095         for hdr, value in headers.iteritems():
-> 1096             self.putheader(hdr, value)
   1097         self.endheaders(body)
   1098 

/usr/lib/python2.7/httplib.pyc in putheader(self, header, *values)
   1033         for one_value in values:
   1034             if _is_illegal_header_value(one_value):
-> 1035                 raise ValueError('Invalid header value %r' % (one_value,))
   1036 
   1037         hdr = '%s: %s' % (header, '\r\n\t'.join(values))

ValueError: Invalid header value 'Token 7367778c1befefbe75ebb99484839f30e18c8fba\n'

In [8]: client = TembaClient('rapidpro.io', open('token').read().strip())

In [9]: a = client.get_flows().iterfetches()

In [10]: list(a)
Out[10]: 
[[<temba_client.v2.types.Flow at 0x7fcf08071dd0>,
  <temba_client.v2.types.Flow at 0x7fcf08071c90>,
  <temba_client.v2.types.Flow at 0x7fcefb482050>,
  <temba_client.v2.types.Flow at 0x7fcefb482110>,
  <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482290>,
  <temba_client.v2.types.Flow at 0x7fcefb482390>,
  <temba_client.v2.types.Flow at 0x7fcefb482490>,
  <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482690>,
  <temba_client.v2.types.Flow at 0x7fcefb482750>,
  <temba_client.v2.types.Flow at 0x7fcefb482810>,
  <temba_client.v2.types.Flow at 0x7fcefb4828d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482990>,
  <temba_client.v2.types.Flow at 0x7fcefb482a50>,
  <temba_client.v2.types.Flow at 0x7fcefb482b10>,
  <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
  <temba_client.v2.types.Flow at 0x7fcefb482c90>,
  <temba_client.v2.types.Flow at 0x7fcefb482d90>,
  <temba_client.v2.types.Flow at 0x7fcefb482e50>,
  <temba_client.v2.types.Flow at 0x7fcefb482f10>,
  <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
  <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483190>,
  <temba_client.v2.types.Flow at 0x7fcefb483250>,
  <temba_client.v2.types.Flow at 0x7fcefb483310>,
  <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483490>,
  <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483690>,
  <temba_client.v2.types.Flow at 0x7fcefb483750>,
  <temba_client.v2.types.Flow at 0x7fcefb483810>,
  <temba_client.v2.types.Flow at 0x7fcefb483950>,
  <temba_client.v2.types.Flow at 0x7fcefb483a50>,
  <temba_client.v2.types.Flow at 0x7fcefb483b50>,
  <temba_client.v2.types.Flow at 0x7fcefb483c90>,
  <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
  <temba_client.v2.types.Flow at 0x7fcefb483f10>,
  <temba_client.v2.types.Flow at 0x7fcefb484090>,
  <temba_client.v2.types.Flow at 0x7fcefb484150>,
  <temba_client.v2.types.Flow at 0x7fcefb484210>,
  <temba_client.v2.types.Flow at 0x7fcefb4842d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484390>,
  <temba_client.v2.types.Flow at 0x7fcefb484450>,
  <temba_client.v2.types.Flow at 0x7fcefb484510>,
  <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484690>,
  <temba_client.v2.types.Flow at 0x7fcefb484750>,
  <temba_client.v2.types.Flow at 0x7fcefb484810>,
  <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484990>,
  <temba_client.v2.types.Flow at 0x7fcefb484a50>,
  <temba_client.v2.types.Flow at 0x7fcefb484b10>,
  <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
  <temba_client.v2.types.Flow at 0x7fcefb484c90>,
  <temba_client.v2.types.Flow at 0x7fcefb484d50>,
  <temba_client.v2.types.Flow at 0x7fcefb484e10>,
  <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
  <temba_client.v2.types.Flow at 0x7fcefb484f90>,
  <temba_client.v2.types.Flow at 0x7fcf0808f090>,
  <temba_client.v2.types.Flow at 0x7fcf0808f150>,
  <temba_client.v2.types.Flow at 0x7fcf0808f210>,
  <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f390>,
  <temba_client.v2.types.Flow at 0x7fcf0808f450>,
  <temba_client.v2.types.Flow at 0x7fcf0808f510>,
  <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f690>,
  <temba_client.v2.types.Flow at 0x7fcf0808f750>,
  <temba_client.v2.types.Flow at 0x7fcf0808f810>,
  <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f990>,
  <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
  <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
  <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
  <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
  <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
  <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
  <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
  <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
  <temba_client.v2.types.Flow at 0x7fcf08093090>,
  <temba_client.v2.types.Flow at 0x7fcf08093150>,
  <temba_client.v2.types.Flow at 0x7fcf08093210>,
  <temba_client.v2.types.Flow at 0x7fcf080932d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093390>,
  <temba_client.v2.types.Flow at 0x7fcf08093450>,
  <temba_client.v2.types.Flow at 0x7fcf08093510>,
  <temba_client.v2.types.Flow at 0x7fcf080935d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093690>,
  <temba_client.v2.types.Flow at 0x7fcf08093750>,
  <temba_client.v2.types.Flow at 0x7fcf08093810>,
  <temba_client.v2.types.Flow at 0x7fcf080938d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093990>,
  <temba_client.v2.types.Flow at 0x7fcf08093a50>,
  <temba_client.v2.types.Flow at 0x7fcf08093b10>,
  <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
  <temba_client.v2.types.Flow at 0x7fcf08093c90>,
  <temba_client.v2.types.Flow at 0x7fcf08093d50>,
  <temba_client.v2.types.Flow at 0x7fcf08093e10>,
  <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
  <temba_client.v2.types.Flow at 0x7fcf08093f90>,
  <temba_client.v2.types.Flow at 0x7fcf08098090>,
  <temba_client.v2.types.Flow at 0x7fcf08098150>,
  <temba_client.v2.types.Flow at 0x7fcf08098210>,
  <temba_client.v2.types.Flow at 0x7fcf080982d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098390>,
  <temba_client.v2.types.Flow at 0x7fcf08098450>,
  <temba_client.v2.types.Flow at 0x7fcf08098510>,
  <temba_client.v2.types.Flow at 0x7fcf080985d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098690>,
  <temba_client.v2.types.Flow at 0x7fcf08098750>,
  <temba_client.v2.types.Flow at 0x7fcf08098810>,
  <temba_client.v2.types.Flow at 0x7fcf080988d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098990>,
  <temba_client.v2.types.Flow at 0x7fcf08098a50>,
  <temba_client.v2.types.Flow at 0x7fcf08098b10>,
  <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
  <temba_client.v2.types.Flow at 0x7fcf08098c90>,
  <temba_client.v2.types.Flow at 0x7fcf08098d50>,
  <temba_client.v2.types.Flow at 0x7fcf08098e10>,
  <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
  <temba_client.v2.types.Flow at 0x7fcf08098f90>,
  <temba_client.v2.types.Flow at 0x7fcf0809c090>,
  <temba_client.v2.types.Flow at 0x7fcf0809c150>,
  <temba_client.v2.types.Flow at 0x7fcf0809c210>,
  <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c390>,
  <temba_client.v2.types.Flow at 0x7fcf0809c450>,
  <temba_client.v2.types.Flow at 0x7fcf0809c510>,
  <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c690>,
  <temba_client.v2.types.Flow at 0x7fcf0809c750>,
  <temba_client.v2.types.Flow at 0x7fcf0809c810>,
  <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c990>,
  <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
  <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
  <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
  <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
  <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
  <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
  <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
  <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
  <temba_client.v2.types.Flow at 0x7fcf080a0090>,
  <temba_client.v2.types.Flow at 0x7fcf080a0150>,
  <temba_client.v2.types.Flow at 0x7fcf080a0210>,
  <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0390>,
  <temba_client.v2.types.Flow at 0x7fcf080a0450>,
  <temba_client.v2.types.Flow at 0x7fcf080a0510>,
  <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0690>,
  <temba_client.v2.types.Flow at 0x7fcf080a0750>,
  <temba_client.v2.types.Flow at 0x7fcf080a0810>,
  <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0990>,
  <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
  <temba_client.v2.types.Flow at 0x7fcf080a4090>,
  <temba_client.v2.types.Flow at 0x7fcf080a4150>,
  <temba_client.v2.types.Flow at 0x7fcf080a4210>,
  <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4390>,
  <temba_client.v2.types.Flow at 0x7fcf080a4450>,
  <temba_client.v2.types.Flow at 0x7fcf080a4510>,
  <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4690>,
  <temba_client.v2.types.Flow at 0x7fcf080a4750>,
  <temba_client.v2.types.Flow at 0x7fcf080a4810>,
  <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4990>,
  <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
  <temba_client.v2.types.Flow at 0x7fcf080a9090>,
  <temba_client.v2.types.Flow at 0x7fcf080a9150>,
  <temba_client.v2.types.Flow at 0x7fcf080a9210>,
  <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9390>,
  <temba_client.v2.types.Flow at 0x7fcf080a9450>,
  <temba_client.v2.types.Flow at 0x7fcf080a9510>,
  <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9690>,
  <temba_client.v2.types.Flow at 0x7fcf080a9750>,
  <temba_client.v2.types.Flow at 0x7fcf080a9810>,
  <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9990>,
  <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
  <temba_client.v2.types.Flow at 0x7fcf080ad090>,
  <temba_client.v2.types.Flow at 0x7fcf080ad150>,
  <temba_client.v2.types.Flow at 0x7fcf080ad210>,
  <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
  <temba_client.v2.types.Flow at 0x7fcf080ad390>,
  <temba_client.v2.types.Flow at 0x7fcf080ad450>,
  <temba_client.v2.types.Flow at 0x7fcf080ad550>,
  <temba_client.v2.types.Flow at 0x7fcf080ad650>,
  <temba_client.v2.types.Flow at 0x7fcf080ad750>,
  <temba_client.v2.types.Flow at 0x7fcf080ad850>,
  <temba_client.v2.types.Flow at 0x7fcf080ad950>,
  <temba_client.v2.types.Flow at 0x7fcf080ada50>,
  <temba_client.v2.types.Flow at 0x7fcf080adb50>,
  <temba_client.v2.types.Flow at 0x7fcf080adc50>,
  <temba_client.v2.types.Flow at 0x7fcf080add10>,
  <temba_client.v2.types.Flow at 0x7fcf080addd0>,
  <temba_client.v2.types.Flow at 0x7fcf080ade90>,
  <temba_client.v2.types.Flow at 0x7fcf080adf50>,
  <temba_client.v2.types.Flow at 0x7fcf080b1050>,
  <temba_client.v2.types.Flow at 0x7fcf080b1110>,
  <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
  <temba_client.v2.types.Flow at 0x7fcf080b1290>,
  <temba_client.v2.types.Flow at 0x7fcf080b1350>,
  <temba_client.v2.types.Flow at 0x7fcf080b1410>]]

In [11]: flows = _

In [12]: flows
Out[12]: 
[[<temba_client.v2.types.Flow at 0x7fcf08071dd0>,
  <temba_client.v2.types.Flow at 0x7fcf08071c90>,
  <temba_client.v2.types.Flow at 0x7fcefb482050>,
  <temba_client.v2.types.Flow at 0x7fcefb482110>,
  <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482290>,
  <temba_client.v2.types.Flow at 0x7fcefb482390>,
  <temba_client.v2.types.Flow at 0x7fcefb482490>,
  <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482690>,
  <temba_client.v2.types.Flow at 0x7fcefb482750>,
  <temba_client.v2.types.Flow at 0x7fcefb482810>,
  <temba_client.v2.types.Flow at 0x7fcefb4828d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482990>,
  <temba_client.v2.types.Flow at 0x7fcefb482a50>,
  <temba_client.v2.types.Flow at 0x7fcefb482b10>,
  <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
  <temba_client.v2.types.Flow at 0x7fcefb482c90>,
  <temba_client.v2.types.Flow at 0x7fcefb482d90>,
  <temba_client.v2.types.Flow at 0x7fcefb482e50>,
  <temba_client.v2.types.Flow at 0x7fcefb482f10>,
  <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
  <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483190>,
  <temba_client.v2.types.Flow at 0x7fcefb483250>,
  <temba_client.v2.types.Flow at 0x7fcefb483310>,
  <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483490>,
  <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483690>,
  <temba_client.v2.types.Flow at 0x7fcefb483750>,
  <temba_client.v2.types.Flow at 0x7fcefb483810>,
  <temba_client.v2.types.Flow at 0x7fcefb483950>,
  <temba_client.v2.types.Flow at 0x7fcefb483a50>,
  <temba_client.v2.types.Flow at 0x7fcefb483b50>,
  <temba_client.v2.types.Flow at 0x7fcefb483c90>,
  <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
  <temba_client.v2.types.Flow at 0x7fcefb483f10>,
  <temba_client.v2.types.Flow at 0x7fcefb484090>,
  <temba_client.v2.types.Flow at 0x7fcefb484150>,
  <temba_client.v2.types.Flow at 0x7fcefb484210>,
  <temba_client.v2.types.Flow at 0x7fcefb4842d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484390>,
  <temba_client.v2.types.Flow at 0x7fcefb484450>,
  <temba_client.v2.types.Flow at 0x7fcefb484510>,
  <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484690>,
  <temba_client.v2.types.Flow at 0x7fcefb484750>,
  <temba_client.v2.types.Flow at 0x7fcefb484810>,
  <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484990>,
  <temba_client.v2.types.Flow at 0x7fcefb484a50>,
  <temba_client.v2.types.Flow at 0x7fcefb484b10>,
  <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
  <temba_client.v2.types.Flow at 0x7fcefb484c90>,
  <temba_client.v2.types.Flow at 0x7fcefb484d50>,
  <temba_client.v2.types.Flow at 0x7fcefb484e10>,
  <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
  <temba_client.v2.types.Flow at 0x7fcefb484f90>,
  <temba_client.v2.types.Flow at 0x7fcf0808f090>,
  <temba_client.v2.types.Flow at 0x7fcf0808f150>,
  <temba_client.v2.types.Flow at 0x7fcf0808f210>,
  <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f390>,
  <temba_client.v2.types.Flow at 0x7fcf0808f450>,
  <temba_client.v2.types.Flow at 0x7fcf0808f510>,
  <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f690>,
  <temba_client.v2.types.Flow at 0x7fcf0808f750>,
  <temba_client.v2.types.Flow at 0x7fcf0808f810>,
  <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f990>,
  <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
  <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
  <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
  <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
  <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
  <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
  <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
  <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
  <temba_client.v2.types.Flow at 0x7fcf08093090>,
  <temba_client.v2.types.Flow at 0x7fcf08093150>,
  <temba_client.v2.types.Flow at 0x7fcf08093210>,
  <temba_client.v2.types.Flow at 0x7fcf080932d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093390>,
  <temba_client.v2.types.Flow at 0x7fcf08093450>,
  <temba_client.v2.types.Flow at 0x7fcf08093510>,
  <temba_client.v2.types.Flow at 0x7fcf080935d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093690>,
  <temba_client.v2.types.Flow at 0x7fcf08093750>,
  <temba_client.v2.types.Flow at 0x7fcf08093810>,
  <temba_client.v2.types.Flow at 0x7fcf080938d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093990>,
  <temba_client.v2.types.Flow at 0x7fcf08093a50>,
  <temba_client.v2.types.Flow at 0x7fcf08093b10>,
  <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
  <temba_client.v2.types.Flow at 0x7fcf08093c90>,
  <temba_client.v2.types.Flow at 0x7fcf08093d50>,
  <temba_client.v2.types.Flow at 0x7fcf08093e10>,
  <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
  <temba_client.v2.types.Flow at 0x7fcf08093f90>,
  <temba_client.v2.types.Flow at 0x7fcf08098090>,
  <temba_client.v2.types.Flow at 0x7fcf08098150>,
  <temba_client.v2.types.Flow at 0x7fcf08098210>,
  <temba_client.v2.types.Flow at 0x7fcf080982d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098390>,
  <temba_client.v2.types.Flow at 0x7fcf08098450>,
  <temba_client.v2.types.Flow at 0x7fcf08098510>,
  <temba_client.v2.types.Flow at 0x7fcf080985d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098690>,
  <temba_client.v2.types.Flow at 0x7fcf08098750>,
  <temba_client.v2.types.Flow at 0x7fcf08098810>,
  <temba_client.v2.types.Flow at 0x7fcf080988d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098990>,
  <temba_client.v2.types.Flow at 0x7fcf08098a50>,
  <temba_client.v2.types.Flow at 0x7fcf08098b10>,
  <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
  <temba_client.v2.types.Flow at 0x7fcf08098c90>,
  <temba_client.v2.types.Flow at 0x7fcf08098d50>,
  <temba_client.v2.types.Flow at 0x7fcf08098e10>,
  <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
  <temba_client.v2.types.Flow at 0x7fcf08098f90>,
  <temba_client.v2.types.Flow at 0x7fcf0809c090>,
  <temba_client.v2.types.Flow at 0x7fcf0809c150>,
  <temba_client.v2.types.Flow at 0x7fcf0809c210>,
  <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c390>,
  <temba_client.v2.types.Flow at 0x7fcf0809c450>,
  <temba_client.v2.types.Flow at 0x7fcf0809c510>,
  <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c690>,
  <temba_client.v2.types.Flow at 0x7fcf0809c750>,
  <temba_client.v2.types.Flow at 0x7fcf0809c810>,
  <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c990>,
  <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
  <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
  <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
  <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
  <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
  <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
  <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
  <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
  <temba_client.v2.types.Flow at 0x7fcf080a0090>,
  <temba_client.v2.types.Flow at 0x7fcf080a0150>,
  <temba_client.v2.types.Flow at 0x7fcf080a0210>,
  <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0390>,
  <temba_client.v2.types.Flow at 0x7fcf080a0450>,
  <temba_client.v2.types.Flow at 0x7fcf080a0510>,
  <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0690>,
  <temba_client.v2.types.Flow at 0x7fcf080a0750>,
  <temba_client.v2.types.Flow at 0x7fcf080a0810>,
  <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0990>,
  <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
  <temba_client.v2.types.Flow at 0x7fcf080a4090>,
  <temba_client.v2.types.Flow at 0x7fcf080a4150>,
  <temba_client.v2.types.Flow at 0x7fcf080a4210>,
  <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4390>,
  <temba_client.v2.types.Flow at 0x7fcf080a4450>,
  <temba_client.v2.types.Flow at 0x7fcf080a4510>,
  <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4690>,
  <temba_client.v2.types.Flow at 0x7fcf080a4750>,
  <temba_client.v2.types.Flow at 0x7fcf080a4810>,
  <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4990>,
  <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
  <temba_client.v2.types.Flow at 0x7fcf080a9090>,
  <temba_client.v2.types.Flow at 0x7fcf080a9150>,
  <temba_client.v2.types.Flow at 0x7fcf080a9210>,
  <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9390>,
  <temba_client.v2.types.Flow at 0x7fcf080a9450>,
  <temba_client.v2.types.Flow at 0x7fcf080a9510>,
  <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9690>,
  <temba_client.v2.types.Flow at 0x7fcf080a9750>,
  <temba_client.v2.types.Flow at 0x7fcf080a9810>,
  <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9990>,
  <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
  <temba_client.v2.types.Flow at 0x7fcf080ad090>,
  <temba_client.v2.types.Flow at 0x7fcf080ad150>,
  <temba_client.v2.types.Flow at 0x7fcf080ad210>,
  <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
  <temba_client.v2.types.Flow at 0x7fcf080ad390>,
  <temba_client.v2.types.Flow at 0x7fcf080ad450>,
  <temba_client.v2.types.Flow at 0x7fcf080ad550>,
  <temba_client.v2.types.Flow at 0x7fcf080ad650>,
  <temba_client.v2.types.Flow at 0x7fcf080ad750>,
  <temba_client.v2.types.Flow at 0x7fcf080ad850>,
  <temba_client.v2.types.Flow at 0x7fcf080ad950>,
  <temba_client.v2.types.Flow at 0x7fcf080ada50>,
  <temba_client.v2.types.Flow at 0x7fcf080adb50>,
  <temba_client.v2.types.Flow at 0x7fcf080adc50>,
  <temba_client.v2.types.Flow at 0x7fcf080add10>,
  <temba_client.v2.types.Flow at 0x7fcf080addd0>,
  <temba_client.v2.types.Flow at 0x7fcf080ade90>,
  <temba_client.v2.types.Flow at 0x7fcf080adf50>,
  <temba_client.v2.types.Flow at 0x7fcf080b1050>,
  <temba_client.v2.types.Flow at 0x7fcf080b1110>,
  <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
  <temba_client.v2.types.Flow at 0x7fcf080b1290>,
  <temba_client.v2.types.Flow at 0x7fcf080b1350>,
  <temba_client.v2.types.Flow at 0x7fcf080b1410>]]

In [13]: f=flows[0]

In [14]: f
Out[14]: 
[<temba_client.v2.types.Flow at 0x7fcf08071dd0>,
 <temba_client.v2.types.Flow at 0x7fcf08071c90>,
 <temba_client.v2.types.Flow at 0x7fcefb482050>,
 <temba_client.v2.types.Flow at 0x7fcefb482110>,
 <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482290>,
 <temba_client.v2.types.Flow at 0x7fcefb482390>,
 <temba_client.v2.types.Flow at 0x7fcefb482490>,
 <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482690>,
 <temba_client.v2.types.Flow at 0x7fcefb482750>,
 <temba_client.v2.types.Flow at 0x7fcefb482810>,
 <temba_client.v2.types.Flow at 0x7fcefb4828d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482990>,
 <temba_client.v2.types.Flow at 0x7fcefb482a50>,
 <temba_client.v2.types.Flow at 0x7fcefb482b10>,
 <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
 <temba_client.v2.types.Flow at 0x7fcefb482c90>,
 <temba_client.v2.types.Flow at 0x7fcefb482d90>,
 <temba_client.v2.types.Flow at 0x7fcefb482e50>,
 <temba_client.v2.types.Flow at 0x7fcefb482f10>,
 <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
 <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483190>,
 <temba_client.v2.types.Flow at 0x7fcefb483250>,
 <temba_client.v2.types.Flow at 0x7fcefb483310>,
 <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483490>,
 <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483690>,
 <temba_client.v2.types.Flow at 0x7fcefb483750>,
 <temba_client.v2.types.Flow at 0x7fcefb483810>,
 <temba_client.v2.types.Flow at 0x7fcefb483950>,
 <temba_client.v2.types.Flow at 0x7fcefb483a50>,
 <temba_client.v2.types.Flow at 0x7fcefb483b50>,
 <temba_client.v2.types.Flow at 0x7fcefb483c90>,
 <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
 <temba_client.v2.types.Flow at 0x7fcefb483f10>,
 <temba_client.v2.types.Flow at 0x7fcefb484090>,
 <temba_client.v2.types.Flow at 0x7fcefb484150>,
 <temba_client.v2.types.Flow at 0x7fcefb484210>,
 <temba_client.v2.types.Flow at 0x7fcefb4842d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484390>,
 <temba_client.v2.types.Flow at 0x7fcefb484450>,
 <temba_client.v2.types.Flow at 0x7fcefb484510>,
 <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484690>,
 <temba_client.v2.types.Flow at 0x7fcefb484750>,
 <temba_client.v2.types.Flow at 0x7fcefb484810>,
 <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484990>,
 <temba_client.v2.types.Flow at 0x7fcefb484a50>,
 <temba_client.v2.types.Flow at 0x7fcefb484b10>,
 <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
 <temba_client.v2.types.Flow at 0x7fcefb484c90>,
 <temba_client.v2.types.Flow at 0x7fcefb484d50>,
 <temba_client.v2.types.Flow at 0x7fcefb484e10>,
 <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
 <temba_client.v2.types.Flow at 0x7fcefb484f90>,
 <temba_client.v2.types.Flow at 0x7fcf0808f090>,
 <temba_client.v2.types.Flow at 0x7fcf0808f150>,
 <temba_client.v2.types.Flow at 0x7fcf0808f210>,
 <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f390>,
 <temba_client.v2.types.Flow at 0x7fcf0808f450>,
 <temba_client.v2.types.Flow at 0x7fcf0808f510>,
 <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f690>,
 <temba_client.v2.types.Flow at 0x7fcf0808f750>,
 <temba_client.v2.types.Flow at 0x7fcf0808f810>,
 <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f990>,
 <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
 <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
 <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
 <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
 <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
 <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
 <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
 <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
 <temba_client.v2.types.Flow at 0x7fcf08093090>,
 <temba_client.v2.types.Flow at 0x7fcf08093150>,
 <temba_client.v2.types.Flow at 0x7fcf08093210>,
 <temba_client.v2.types.Flow at 0x7fcf080932d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093390>,
 <temba_client.v2.types.Flow at 0x7fcf08093450>,
 <temba_client.v2.types.Flow at 0x7fcf08093510>,
 <temba_client.v2.types.Flow at 0x7fcf080935d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093690>,
 <temba_client.v2.types.Flow at 0x7fcf08093750>,
 <temba_client.v2.types.Flow at 0x7fcf08093810>,
 <temba_client.v2.types.Flow at 0x7fcf080938d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093990>,
 <temba_client.v2.types.Flow at 0x7fcf08093a50>,
 <temba_client.v2.types.Flow at 0x7fcf08093b10>,
 <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
 <temba_client.v2.types.Flow at 0x7fcf08093c90>,
 <temba_client.v2.types.Flow at 0x7fcf08093d50>,
 <temba_client.v2.types.Flow at 0x7fcf08093e10>,
 <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
 <temba_client.v2.types.Flow at 0x7fcf08093f90>,
 <temba_client.v2.types.Flow at 0x7fcf08098090>,
 <temba_client.v2.types.Flow at 0x7fcf08098150>,
 <temba_client.v2.types.Flow at 0x7fcf08098210>,
 <temba_client.v2.types.Flow at 0x7fcf080982d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098390>,
 <temba_client.v2.types.Flow at 0x7fcf08098450>,
 <temba_client.v2.types.Flow at 0x7fcf08098510>,
 <temba_client.v2.types.Flow at 0x7fcf080985d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098690>,
 <temba_client.v2.types.Flow at 0x7fcf08098750>,
 <temba_client.v2.types.Flow at 0x7fcf08098810>,
 <temba_client.v2.types.Flow at 0x7fcf080988d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098990>,
 <temba_client.v2.types.Flow at 0x7fcf08098a50>,
 <temba_client.v2.types.Flow at 0x7fcf08098b10>,
 <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
 <temba_client.v2.types.Flow at 0x7fcf08098c90>,
 <temba_client.v2.types.Flow at 0x7fcf08098d50>,
 <temba_client.v2.types.Flow at 0x7fcf08098e10>,
 <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
 <temba_client.v2.types.Flow at 0x7fcf08098f90>,
 <temba_client.v2.types.Flow at 0x7fcf0809c090>,
 <temba_client.v2.types.Flow at 0x7fcf0809c150>,
 <temba_client.v2.types.Flow at 0x7fcf0809c210>,
 <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c390>,
 <temba_client.v2.types.Flow at 0x7fcf0809c450>,
 <temba_client.v2.types.Flow at 0x7fcf0809c510>,
 <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c690>,
 <temba_client.v2.types.Flow at 0x7fcf0809c750>,
 <temba_client.v2.types.Flow at 0x7fcf0809c810>,
 <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c990>,
 <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
 <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
 <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
 <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
 <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
 <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
 <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
 <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
 <temba_client.v2.types.Flow at 0x7fcf080a0090>,
 <temba_client.v2.types.Flow at 0x7fcf080a0150>,
 <temba_client.v2.types.Flow at 0x7fcf080a0210>,
 <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0390>,
 <temba_client.v2.types.Flow at 0x7fcf080a0450>,
 <temba_client.v2.types.Flow at 0x7fcf080a0510>,
 <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0690>,
 <temba_client.v2.types.Flow at 0x7fcf080a0750>,
 <temba_client.v2.types.Flow at 0x7fcf080a0810>,
 <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0990>,
 <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
 <temba_client.v2.types.Flow at 0x7fcf080a4090>,
 <temba_client.v2.types.Flow at 0x7fcf080a4150>,
 <temba_client.v2.types.Flow at 0x7fcf080a4210>,
 <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4390>,
 <temba_client.v2.types.Flow at 0x7fcf080a4450>,
 <temba_client.v2.types.Flow at 0x7fcf080a4510>,
 <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4690>,
 <temba_client.v2.types.Flow at 0x7fcf080a4750>,
 <temba_client.v2.types.Flow at 0x7fcf080a4810>,
 <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4990>,
 <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
 <temba_client.v2.types.Flow at 0x7fcf080a9090>,
 <temba_client.v2.types.Flow at 0x7fcf080a9150>,
 <temba_client.v2.types.Flow at 0x7fcf080a9210>,
 <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9390>,
 <temba_client.v2.types.Flow at 0x7fcf080a9450>,
 <temba_client.v2.types.Flow at 0x7fcf080a9510>,
 <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9690>,
 <temba_client.v2.types.Flow at 0x7fcf080a9750>,
 <temba_client.v2.types.Flow at 0x7fcf080a9810>,
 <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9990>,
 <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
 <temba_client.v2.types.Flow at 0x7fcf080ad090>,
 <temba_client.v2.types.Flow at 0x7fcf080ad150>,
 <temba_client.v2.types.Flow at 0x7fcf080ad210>,
 <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
 <temba_client.v2.types.Flow at 0x7fcf080ad390>,
 <temba_client.v2.types.Flow at 0x7fcf080ad450>,
 <temba_client.v2.types.Flow at 0x7fcf080ad550>,
 <temba_client.v2.types.Flow at 0x7fcf080ad650>,
 <temba_client.v2.types.Flow at 0x7fcf080ad750>,
 <temba_client.v2.types.Flow at 0x7fcf080ad850>,
 <temba_client.v2.types.Flow at 0x7fcf080ad950>,
 <temba_client.v2.types.Flow at 0x7fcf080ada50>,
 <temba_client.v2.types.Flow at 0x7fcf080adb50>,
 <temba_client.v2.types.Flow at 0x7fcf080adc50>,
 <temba_client.v2.types.Flow at 0x7fcf080add10>,
 <temba_client.v2.types.Flow at 0x7fcf080addd0>,
 <temba_client.v2.types.Flow at 0x7fcf080ade90>,
 <temba_client.v2.types.Flow at 0x7fcf080adf50>,
 <temba_client.v2.types.Flow at 0x7fcf080b1050>,
 <temba_client.v2.types.Flow at 0x7fcf080b1110>,
 <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
 <temba_client.v2.types.Flow at 0x7fcf080b1290>,
 <temba_client.v2.types.Flow at 0x7fcf080b1350>,
 <temba_client.v2.types.Flow at 0x7fcf080b1410>]

In [15]: f = flows[0]

In [16]: f
Out[16]: 
[<temba_client.v2.types.Flow at 0x7fcf08071dd0>,
 <temba_client.v2.types.Flow at 0x7fcf08071c90>,
 <temba_client.v2.types.Flow at 0x7fcefb482050>,
 <temba_client.v2.types.Flow at 0x7fcefb482110>,
 <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482290>,
 <temba_client.v2.types.Flow at 0x7fcefb482390>,
 <temba_client.v2.types.Flow at 0x7fcefb482490>,
 <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482690>,
 <temba_client.v2.types.Flow at 0x7fcefb482750>,
 <temba_client.v2.types.Flow at 0x7fcefb482810>,
 <temba_client.v2.types.Flow at 0x7fcefb4828d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482990>,
 <temba_client.v2.types.Flow at 0x7fcefb482a50>,
 <temba_client.v2.types.Flow at 0x7fcefb482b10>,
 <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
 <temba_client.v2.types.Flow at 0x7fcefb482c90>,
 <temba_client.v2.types.Flow at 0x7fcefb482d90>,
 <temba_client.v2.types.Flow at 0x7fcefb482e50>,
 <temba_client.v2.types.Flow at 0x7fcefb482f10>,
 <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
 <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483190>,
 <temba_client.v2.types.Flow at 0x7fcefb483250>,
 <temba_client.v2.types.Flow at 0x7fcefb483310>,
 <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483490>,
 <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483690>,
 <temba_client.v2.types.Flow at 0x7fcefb483750>,
 <temba_client.v2.types.Flow at 0x7fcefb483810>,
 <temba_client.v2.types.Flow at 0x7fcefb483950>,
 <temba_client.v2.types.Flow at 0x7fcefb483a50>,
 <temba_client.v2.types.Flow at 0x7fcefb483b50>,
 <temba_client.v2.types.Flow at 0x7fcefb483c90>,
 <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
 <temba_client.v2.types.Flow at 0x7fcefb483f10>,
 <temba_client.v2.types.Flow at 0x7fcefb484090>,
 <temba_client.v2.types.Flow at 0x7fcefb484150>,
 <temba_client.v2.types.Flow at 0x7fcefb484210>,
 <temba_client.v2.types.Flow at 0x7fcefb4842d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484390>,
 <temba_client.v2.types.Flow at 0x7fcefb484450>,
 <temba_client.v2.types.Flow at 0x7fcefb484510>,
 <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484690>,
 <temba_client.v2.types.Flow at 0x7fcefb484750>,
 <temba_client.v2.types.Flow at 0x7fcefb484810>,
 <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484990>,
 <temba_client.v2.types.Flow at 0x7fcefb484a50>,
 <temba_client.v2.types.Flow at 0x7fcefb484b10>,
 <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
 <temba_client.v2.types.Flow at 0x7fcefb484c90>,
 <temba_client.v2.types.Flow at 0x7fcefb484d50>,
 <temba_client.v2.types.Flow at 0x7fcefb484e10>,
 <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
 <temba_client.v2.types.Flow at 0x7fcefb484f90>,
 <temba_client.v2.types.Flow at 0x7fcf0808f090>,
 <temba_client.v2.types.Flow at 0x7fcf0808f150>,
 <temba_client.v2.types.Flow at 0x7fcf0808f210>,
 <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f390>,
 <temba_client.v2.types.Flow at 0x7fcf0808f450>,
 <temba_client.v2.types.Flow at 0x7fcf0808f510>,
 <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f690>,
 <temba_client.v2.types.Flow at 0x7fcf0808f750>,
 <temba_client.v2.types.Flow at 0x7fcf0808f810>,
 <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f990>,
 <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
 <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
 <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
 <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
 <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
 <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
 <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
 <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
 <temba_client.v2.types.Flow at 0x7fcf08093090>,
 <temba_client.v2.types.Flow at 0x7fcf08093150>,
 <temba_client.v2.types.Flow at 0x7fcf08093210>,
 <temba_client.v2.types.Flow at 0x7fcf080932d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093390>,
 <temba_client.v2.types.Flow at 0x7fcf08093450>,
 <temba_client.v2.types.Flow at 0x7fcf08093510>,
 <temba_client.v2.types.Flow at 0x7fcf080935d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093690>,
 <temba_client.v2.types.Flow at 0x7fcf08093750>,
 <temba_client.v2.types.Flow at 0x7fcf08093810>,
 <temba_client.v2.types.Flow at 0x7fcf080938d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093990>,
 <temba_client.v2.types.Flow at 0x7fcf08093a50>,
 <temba_client.v2.types.Flow at 0x7fcf08093b10>,
 <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
 <temba_client.v2.types.Flow at 0x7fcf08093c90>,
 <temba_client.v2.types.Flow at 0x7fcf08093d50>,
 <temba_client.v2.types.Flow at 0x7fcf08093e10>,
 <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
 <temba_client.v2.types.Flow at 0x7fcf08093f90>,
 <temba_client.v2.types.Flow at 0x7fcf08098090>,
 <temba_client.v2.types.Flow at 0x7fcf08098150>,
 <temba_client.v2.types.Flow at 0x7fcf08098210>,
 <temba_client.v2.types.Flow at 0x7fcf080982d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098390>,
 <temba_client.v2.types.Flow at 0x7fcf08098450>,
 <temba_client.v2.types.Flow at 0x7fcf08098510>,
 <temba_client.v2.types.Flow at 0x7fcf080985d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098690>,
 <temba_client.v2.types.Flow at 0x7fcf08098750>,
 <temba_client.v2.types.Flow at 0x7fcf08098810>,
 <temba_client.v2.types.Flow at 0x7fcf080988d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098990>,
 <temba_client.v2.types.Flow at 0x7fcf08098a50>,
 <temba_client.v2.types.Flow at 0x7fcf08098b10>,
 <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
 <temba_client.v2.types.Flow at 0x7fcf08098c90>,
 <temba_client.v2.types.Flow at 0x7fcf08098d50>,
 <temba_client.v2.types.Flow at 0x7fcf08098e10>,
 <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
 <temba_client.v2.types.Flow at 0x7fcf08098f90>,
 <temba_client.v2.types.Flow at 0x7fcf0809c090>,
 <temba_client.v2.types.Flow at 0x7fcf0809c150>,
 <temba_client.v2.types.Flow at 0x7fcf0809c210>,
 <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c390>,
 <temba_client.v2.types.Flow at 0x7fcf0809c450>,
 <temba_client.v2.types.Flow at 0x7fcf0809c510>,
 <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c690>,
 <temba_client.v2.types.Flow at 0x7fcf0809c750>,
 <temba_client.v2.types.Flow at 0x7fcf0809c810>,
 <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c990>,
 <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
 <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
 <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
 <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
 <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
 <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
 <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
 <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
 <temba_client.v2.types.Flow at 0x7fcf080a0090>,
 <temba_client.v2.types.Flow at 0x7fcf080a0150>,
 <temba_client.v2.types.Flow at 0x7fcf080a0210>,
 <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0390>,
 <temba_client.v2.types.Flow at 0x7fcf080a0450>,
 <temba_client.v2.types.Flow at 0x7fcf080a0510>,
 <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0690>,
 <temba_client.v2.types.Flow at 0x7fcf080a0750>,
 <temba_client.v2.types.Flow at 0x7fcf080a0810>,
 <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0990>,
 <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
 <temba_client.v2.types.Flow at 0x7fcf080a4090>,
 <temba_client.v2.types.Flow at 0x7fcf080a4150>,
 <temba_client.v2.types.Flow at 0x7fcf080a4210>,
 <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4390>,
 <temba_client.v2.types.Flow at 0x7fcf080a4450>,
 <temba_client.v2.types.Flow at 0x7fcf080a4510>,
 <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4690>,
 <temba_client.v2.types.Flow at 0x7fcf080a4750>,
 <temba_client.v2.types.Flow at 0x7fcf080a4810>,
 <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4990>,
 <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
 <temba_client.v2.types.Flow at 0x7fcf080a9090>,
 <temba_client.v2.types.Flow at 0x7fcf080a9150>,
 <temba_client.v2.types.Flow at 0x7fcf080a9210>,
 <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9390>,
 <temba_client.v2.types.Flow at 0x7fcf080a9450>,
 <temba_client.v2.types.Flow at 0x7fcf080a9510>,
 <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9690>,
 <temba_client.v2.types.Flow at 0x7fcf080a9750>,
 <temba_client.v2.types.Flow at 0x7fcf080a9810>,
 <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9990>,
 <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
 <temba_client.v2.types.Flow at 0x7fcf080ad090>,
 <temba_client.v2.types.Flow at 0x7fcf080ad150>,
 <temba_client.v2.types.Flow at 0x7fcf080ad210>,
 <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
 <temba_client.v2.types.Flow at 0x7fcf080ad390>,
 <temba_client.v2.types.Flow at 0x7fcf080ad450>,
 <temba_client.v2.types.Flow at 0x7fcf080ad550>,
 <temba_client.v2.types.Flow at 0x7fcf080ad650>,
 <temba_client.v2.types.Flow at 0x7fcf080ad750>,
 <temba_client.v2.types.Flow at 0x7fcf080ad850>,
 <temba_client.v2.types.Flow at 0x7fcf080ad950>,
 <temba_client.v2.types.Flow at 0x7fcf080ada50>,
 <temba_client.v2.types.Flow at 0x7fcf080adb50>,
 <temba_client.v2.types.Flow at 0x7fcf080adc50>,
 <temba_client.v2.types.Flow at 0x7fcf080add10>,
 <temba_client.v2.types.Flow at 0x7fcf080addd0>,
 <temba_client.v2.types.Flow at 0x7fcf080ade90>,
 <temba_client.v2.types.Flow at 0x7fcf080adf50>,
 <temba_client.v2.types.Flow at 0x7fcf080b1050>,
 <temba_client.v2.types.Flow at 0x7fcf080b1110>,
 <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
 <temba_client.v2.types.Flow at 0x7fcf080b1290>,
 <temba_client.v2.types.Flow at 0x7fcf080b1350>,
 <temba_client.v2.types.Flow at 0x7fcf080b1410>]

In [17]: f = flows[0]

In [18]: f
Out[18]: 
[<temba_client.v2.types.Flow at 0x7fcf08071dd0>,
 <temba_client.v2.types.Flow at 0x7fcf08071c90>,
 <temba_client.v2.types.Flow at 0x7fcefb482050>,
 <temba_client.v2.types.Flow at 0x7fcefb482110>,
 <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482290>,
 <temba_client.v2.types.Flow at 0x7fcefb482390>,
 <temba_client.v2.types.Flow at 0x7fcefb482490>,
 <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482690>,
 <temba_client.v2.types.Flow at 0x7fcefb482750>,
 <temba_client.v2.types.Flow at 0x7fcefb482810>,
 <temba_client.v2.types.Flow at 0x7fcefb4828d0>,
 <temba_client.v2.types.Flow at 0x7fcefb482990>,
 <temba_client.v2.types.Flow at 0x7fcefb482a50>,
 <temba_client.v2.types.Flow at 0x7fcefb482b10>,
 <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
 <temba_client.v2.types.Flow at 0x7fcefb482c90>,
 <temba_client.v2.types.Flow at 0x7fcefb482d90>,
 <temba_client.v2.types.Flow at 0x7fcefb482e50>,
 <temba_client.v2.types.Flow at 0x7fcefb482f10>,
 <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
 <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483190>,
 <temba_client.v2.types.Flow at 0x7fcefb483250>,
 <temba_client.v2.types.Flow at 0x7fcefb483310>,
 <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483490>,
 <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
 <temba_client.v2.types.Flow at 0x7fcefb483690>,
 <temba_client.v2.types.Flow at 0x7fcefb483750>,
 <temba_client.v2.types.Flow at 0x7fcefb483810>,
 <temba_client.v2.types.Flow at 0x7fcefb483950>,
 <temba_client.v2.types.Flow at 0x7fcefb483a50>,
 <temba_client.v2.types.Flow at 0x7fcefb483b50>,
 <temba_client.v2.types.Flow at 0x7fcefb483c90>,
 <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
 <temba_client.v2.types.Flow at 0x7fcefb483f10>,
 <temba_client.v2.types.Flow at 0x7fcefb484090>,
 <temba_client.v2.types.Flow at 0x7fcefb484150>,
 <temba_client.v2.types.Flow at 0x7fcefb484210>,
 <temba_client.v2.types.Flow at 0x7fcefb4842d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484390>,
 <temba_client.v2.types.Flow at 0x7fcefb484450>,
 <temba_client.v2.types.Flow at 0x7fcefb484510>,
 <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484690>,
 <temba_client.v2.types.Flow at 0x7fcefb484750>,
 <temba_client.v2.types.Flow at 0x7fcefb484810>,
 <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
 <temba_client.v2.types.Flow at 0x7fcefb484990>,
 <temba_client.v2.types.Flow at 0x7fcefb484a50>,
 <temba_client.v2.types.Flow at 0x7fcefb484b10>,
 <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
 <temba_client.v2.types.Flow at 0x7fcefb484c90>,
 <temba_client.v2.types.Flow at 0x7fcefb484d50>,
 <temba_client.v2.types.Flow at 0x7fcefb484e10>,
 <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
 <temba_client.v2.types.Flow at 0x7fcefb484f90>,
 <temba_client.v2.types.Flow at 0x7fcf0808f090>,
 <temba_client.v2.types.Flow at 0x7fcf0808f150>,
 <temba_client.v2.types.Flow at 0x7fcf0808f210>,
 <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f390>,
 <temba_client.v2.types.Flow at 0x7fcf0808f450>,
 <temba_client.v2.types.Flow at 0x7fcf0808f510>,
 <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f690>,
 <temba_client.v2.types.Flow at 0x7fcf0808f750>,
 <temba_client.v2.types.Flow at 0x7fcf0808f810>,
 <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
 <temba_client.v2.types.Flow at 0x7fcf0808f990>,
 <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
 <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
 <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
 <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
 <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
 <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
 <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
 <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
 <temba_client.v2.types.Flow at 0x7fcf08093090>,
 <temba_client.v2.types.Flow at 0x7fcf08093150>,
 <temba_client.v2.types.Flow at 0x7fcf08093210>,
 <temba_client.v2.types.Flow at 0x7fcf080932d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093390>,
 <temba_client.v2.types.Flow at 0x7fcf08093450>,
 <temba_client.v2.types.Flow at 0x7fcf08093510>,
 <temba_client.v2.types.Flow at 0x7fcf080935d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093690>,
 <temba_client.v2.types.Flow at 0x7fcf08093750>,
 <temba_client.v2.types.Flow at 0x7fcf08093810>,
 <temba_client.v2.types.Flow at 0x7fcf080938d0>,
 <temba_client.v2.types.Flow at 0x7fcf08093990>,
 <temba_client.v2.types.Flow at 0x7fcf08093a50>,
 <temba_client.v2.types.Flow at 0x7fcf08093b10>,
 <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
 <temba_client.v2.types.Flow at 0x7fcf08093c90>,
 <temba_client.v2.types.Flow at 0x7fcf08093d50>,
 <temba_client.v2.types.Flow at 0x7fcf08093e10>,
 <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
 <temba_client.v2.types.Flow at 0x7fcf08093f90>,
 <temba_client.v2.types.Flow at 0x7fcf08098090>,
 <temba_client.v2.types.Flow at 0x7fcf08098150>,
 <temba_client.v2.types.Flow at 0x7fcf08098210>,
 <temba_client.v2.types.Flow at 0x7fcf080982d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098390>,
 <temba_client.v2.types.Flow at 0x7fcf08098450>,
 <temba_client.v2.types.Flow at 0x7fcf08098510>,
 <temba_client.v2.types.Flow at 0x7fcf080985d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098690>,
 <temba_client.v2.types.Flow at 0x7fcf08098750>,
 <temba_client.v2.types.Flow at 0x7fcf08098810>,
 <temba_client.v2.types.Flow at 0x7fcf080988d0>,
 <temba_client.v2.types.Flow at 0x7fcf08098990>,
 <temba_client.v2.types.Flow at 0x7fcf08098a50>,
 <temba_client.v2.types.Flow at 0x7fcf08098b10>,
 <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
 <temba_client.v2.types.Flow at 0x7fcf08098c90>,
 <temba_client.v2.types.Flow at 0x7fcf08098d50>,
 <temba_client.v2.types.Flow at 0x7fcf08098e10>,
 <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
 <temba_client.v2.types.Flow at 0x7fcf08098f90>,
 <temba_client.v2.types.Flow at 0x7fcf0809c090>,
 <temba_client.v2.types.Flow at 0x7fcf0809c150>,
 <temba_client.v2.types.Flow at 0x7fcf0809c210>,
 <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c390>,
 <temba_client.v2.types.Flow at 0x7fcf0809c450>,
 <temba_client.v2.types.Flow at 0x7fcf0809c510>,
 <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c690>,
 <temba_client.v2.types.Flow at 0x7fcf0809c750>,
 <temba_client.v2.types.Flow at 0x7fcf0809c810>,
 <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
 <temba_client.v2.types.Flow at 0x7fcf0809c990>,
 <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
 <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
 <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
 <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
 <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
 <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
 <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
 <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
 <temba_client.v2.types.Flow at 0x7fcf080a0090>,
 <temba_client.v2.types.Flow at 0x7fcf080a0150>,
 <temba_client.v2.types.Flow at 0x7fcf080a0210>,
 <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0390>,
 <temba_client.v2.types.Flow at 0x7fcf080a0450>,
 <temba_client.v2.types.Flow at 0x7fcf080a0510>,
 <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0690>,
 <temba_client.v2.types.Flow at 0x7fcf080a0750>,
 <temba_client.v2.types.Flow at 0x7fcf080a0810>,
 <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0990>,
 <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
 <temba_client.v2.types.Flow at 0x7fcf080a4090>,
 <temba_client.v2.types.Flow at 0x7fcf080a4150>,
 <temba_client.v2.types.Flow at 0x7fcf080a4210>,
 <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4390>,
 <temba_client.v2.types.Flow at 0x7fcf080a4450>,
 <temba_client.v2.types.Flow at 0x7fcf080a4510>,
 <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4690>,
 <temba_client.v2.types.Flow at 0x7fcf080a4750>,
 <temba_client.v2.types.Flow at 0x7fcf080a4810>,
 <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4990>,
 <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
 <temba_client.v2.types.Flow at 0x7fcf080a9090>,
 <temba_client.v2.types.Flow at 0x7fcf080a9150>,
 <temba_client.v2.types.Flow at 0x7fcf080a9210>,
 <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9390>,
 <temba_client.v2.types.Flow at 0x7fcf080a9450>,
 <temba_client.v2.types.Flow at 0x7fcf080a9510>,
 <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9690>,
 <temba_client.v2.types.Flow at 0x7fcf080a9750>,
 <temba_client.v2.types.Flow at 0x7fcf080a9810>,
 <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9990>,
 <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
 <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
 <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
 <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
 <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
 <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
 <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
 <temba_client.v2.types.Flow at 0x7fcf080ad090>,
 <temba_client.v2.types.Flow at 0x7fcf080ad150>,
 <temba_client.v2.types.Flow at 0x7fcf080ad210>,
 <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
 <temba_client.v2.types.Flow at 0x7fcf080ad390>,
 <temba_client.v2.types.Flow at 0x7fcf080ad450>,
 <temba_client.v2.types.Flow at 0x7fcf080ad550>,
 <temba_client.v2.types.Flow at 0x7fcf080ad650>,
 <temba_client.v2.types.Flow at 0x7fcf080ad750>,
 <temba_client.v2.types.Flow at 0x7fcf080ad850>,
 <temba_client.v2.types.Flow at 0x7fcf080ad950>,
 <temba_client.v2.types.Flow at 0x7fcf080ada50>,
 <temba_client.v2.types.Flow at 0x7fcf080adb50>,
 <temba_client.v2.types.Flow at 0x7fcf080adc50>,
 <temba_client.v2.types.Flow at 0x7fcf080add10>,
 <temba_client.v2.types.Flow at 0x7fcf080addd0>,
 <temba_client.v2.types.Flow at 0x7fcf080ade90>,
 <temba_client.v2.types.Flow at 0x7fcf080adf50>,
 <temba_client.v2.types.Flow at 0x7fcf080b1050>,
 <temba_client.v2.types.Flow at 0x7fcf080b1110>,
 <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
 <temba_client.v2.types.Flow at 0x7fcf080b1290>,
 <temba_client.v2.types.Flow at 0x7fcf080b1350>,
 <temba_client.v2.types.Flow at 0x7fcf080b1410>]

In [19]: flows
Out[19]: 
[[<temba_client.v2.types.Flow at 0x7fcf08071dd0>,
  <temba_client.v2.types.Flow at 0x7fcf08071c90>,
  <temba_client.v2.types.Flow at 0x7fcefb482050>,
  <temba_client.v2.types.Flow at 0x7fcefb482110>,
  <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482290>,
  <temba_client.v2.types.Flow at 0x7fcefb482390>,
  <temba_client.v2.types.Flow at 0x7fcefb482490>,
  <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482690>,
  <temba_client.v2.types.Flow at 0x7fcefb482750>,
  <temba_client.v2.types.Flow at 0x7fcefb482810>,
  <temba_client.v2.types.Flow at 0x7fcefb4828d0>,
  <temba_client.v2.types.Flow at 0x7fcefb482990>,
  <temba_client.v2.types.Flow at 0x7fcefb482a50>,
  <temba_client.v2.types.Flow at 0x7fcefb482b10>,
  <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
  <temba_client.v2.types.Flow at 0x7fcefb482c90>,
  <temba_client.v2.types.Flow at 0x7fcefb482d90>,
  <temba_client.v2.types.Flow at 0x7fcefb482e50>,
  <temba_client.v2.types.Flow at 0x7fcefb482f10>,
  <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
  <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483190>,
  <temba_client.v2.types.Flow at 0x7fcefb483250>,
  <temba_client.v2.types.Flow at 0x7fcefb483310>,
  <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483490>,
  <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
  <temba_client.v2.types.Flow at 0x7fcefb483690>,
  <temba_client.v2.types.Flow at 0x7fcefb483750>,
  <temba_client.v2.types.Flow at 0x7fcefb483810>,
  <temba_client.v2.types.Flow at 0x7fcefb483950>,
  <temba_client.v2.types.Flow at 0x7fcefb483a50>,
  <temba_client.v2.types.Flow at 0x7fcefb483b50>,
  <temba_client.v2.types.Flow at 0x7fcefb483c90>,
  <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
  <temba_client.v2.types.Flow at 0x7fcefb483f10>,
  <temba_client.v2.types.Flow at 0x7fcefb484090>,
  <temba_client.v2.types.Flow at 0x7fcefb484150>,
  <temba_client.v2.types.Flow at 0x7fcefb484210>,
  <temba_client.v2.types.Flow at 0x7fcefb4842d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484390>,
  <temba_client.v2.types.Flow at 0x7fcefb484450>,
  <temba_client.v2.types.Flow at 0x7fcefb484510>,
  <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484690>,
  <temba_client.v2.types.Flow at 0x7fcefb484750>,
  <temba_client.v2.types.Flow at 0x7fcefb484810>,
  <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
  <temba_client.v2.types.Flow at 0x7fcefb484990>,
  <temba_client.v2.types.Flow at 0x7fcefb484a50>,
  <temba_client.v2.types.Flow at 0x7fcefb484b10>,
  <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
  <temba_client.v2.types.Flow at 0x7fcefb484c90>,
  <temba_client.v2.types.Flow at 0x7fcefb484d50>,
  <temba_client.v2.types.Flow at 0x7fcefb484e10>,
  <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
  <temba_client.v2.types.Flow at 0x7fcefb484f90>,
  <temba_client.v2.types.Flow at 0x7fcf0808f090>,
  <temba_client.v2.types.Flow at 0x7fcf0808f150>,
  <temba_client.v2.types.Flow at 0x7fcf0808f210>,
  <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f390>,
  <temba_client.v2.types.Flow at 0x7fcf0808f450>,
  <temba_client.v2.types.Flow at 0x7fcf0808f510>,
  <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f690>,
  <temba_client.v2.types.Flow at 0x7fcf0808f750>,
  <temba_client.v2.types.Flow at 0x7fcf0808f810>,
  <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
  <temba_client.v2.types.Flow at 0x7fcf0808f990>,
  <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
  <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
  <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
  <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
  <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
  <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
  <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
  <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
  <temba_client.v2.types.Flow at 0x7fcf08093090>,
  <temba_client.v2.types.Flow at 0x7fcf08093150>,
  <temba_client.v2.types.Flow at 0x7fcf08093210>,
  <temba_client.v2.types.Flow at 0x7fcf080932d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093390>,
  <temba_client.v2.types.Flow at 0x7fcf08093450>,
  <temba_client.v2.types.Flow at 0x7fcf08093510>,
  <temba_client.v2.types.Flow at 0x7fcf080935d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093690>,
  <temba_client.v2.types.Flow at 0x7fcf08093750>,
  <temba_client.v2.types.Flow at 0x7fcf08093810>,
  <temba_client.v2.types.Flow at 0x7fcf080938d0>,
  <temba_client.v2.types.Flow at 0x7fcf08093990>,
  <temba_client.v2.types.Flow at 0x7fcf08093a50>,
  <temba_client.v2.types.Flow at 0x7fcf08093b10>,
  <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
  <temba_client.v2.types.Flow at 0x7fcf08093c90>,
  <temba_client.v2.types.Flow at 0x7fcf08093d50>,
  <temba_client.v2.types.Flow at 0x7fcf08093e10>,
  <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
  <temba_client.v2.types.Flow at 0x7fcf08093f90>,
  <temba_client.v2.types.Flow at 0x7fcf08098090>,
  <temba_client.v2.types.Flow at 0x7fcf08098150>,
  <temba_client.v2.types.Flow at 0x7fcf08098210>,
  <temba_client.v2.types.Flow at 0x7fcf080982d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098390>,
  <temba_client.v2.types.Flow at 0x7fcf08098450>,
  <temba_client.v2.types.Flow at 0x7fcf08098510>,
  <temba_client.v2.types.Flow at 0x7fcf080985d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098690>,
  <temba_client.v2.types.Flow at 0x7fcf08098750>,
  <temba_client.v2.types.Flow at 0x7fcf08098810>,
  <temba_client.v2.types.Flow at 0x7fcf080988d0>,
  <temba_client.v2.types.Flow at 0x7fcf08098990>,
  <temba_client.v2.types.Flow at 0x7fcf08098a50>,
  <temba_client.v2.types.Flow at 0x7fcf08098b10>,
  <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
  <temba_client.v2.types.Flow at 0x7fcf08098c90>,
  <temba_client.v2.types.Flow at 0x7fcf08098d50>,
  <temba_client.v2.types.Flow at 0x7fcf08098e10>,
  <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
  <temba_client.v2.types.Flow at 0x7fcf08098f90>,
  <temba_client.v2.types.Flow at 0x7fcf0809c090>,
  <temba_client.v2.types.Flow at 0x7fcf0809c150>,
  <temba_client.v2.types.Flow at 0x7fcf0809c210>,
  <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c390>,
  <temba_client.v2.types.Flow at 0x7fcf0809c450>,
  <temba_client.v2.types.Flow at 0x7fcf0809c510>,
  <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c690>,
  <temba_client.v2.types.Flow at 0x7fcf0809c750>,
  <temba_client.v2.types.Flow at 0x7fcf0809c810>,
  <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
  <temba_client.v2.types.Flow at 0x7fcf0809c990>,
  <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
  <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
  <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
  <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
  <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
  <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
  <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
  <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
  <temba_client.v2.types.Flow at 0x7fcf080a0090>,
  <temba_client.v2.types.Flow at 0x7fcf080a0150>,
  <temba_client.v2.types.Flow at 0x7fcf080a0210>,
  <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0390>,
  <temba_client.v2.types.Flow at 0x7fcf080a0450>,
  <temba_client.v2.types.Flow at 0x7fcf080a0510>,
  <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0690>,
  <temba_client.v2.types.Flow at 0x7fcf080a0750>,
  <temba_client.v2.types.Flow at 0x7fcf080a0810>,
  <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0990>,
  <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
  <temba_client.v2.types.Flow at 0x7fcf080a4090>,
  <temba_client.v2.types.Flow at 0x7fcf080a4150>,
  <temba_client.v2.types.Flow at 0x7fcf080a4210>,
  <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4390>,
  <temba_client.v2.types.Flow at 0x7fcf080a4450>,
  <temba_client.v2.types.Flow at 0x7fcf080a4510>,
  <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4690>,
  <temba_client.v2.types.Flow at 0x7fcf080a4750>,
  <temba_client.v2.types.Flow at 0x7fcf080a4810>,
  <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4990>,
  <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
  <temba_client.v2.types.Flow at 0x7fcf080a9090>,
  <temba_client.v2.types.Flow at 0x7fcf080a9150>,
  <temba_client.v2.types.Flow at 0x7fcf080a9210>,
  <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9390>,
  <temba_client.v2.types.Flow at 0x7fcf080a9450>,
  <temba_client.v2.types.Flow at 0x7fcf080a9510>,
  <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9690>,
  <temba_client.v2.types.Flow at 0x7fcf080a9750>,
  <temba_client.v2.types.Flow at 0x7fcf080a9810>,
  <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9990>,
  <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
  <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
  <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
  <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
  <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
  <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
  <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
  <temba_client.v2.types.Flow at 0x7fcf080ad090>,
  <temba_client.v2.types.Flow at 0x7fcf080ad150>,
  <temba_client.v2.types.Flow at 0x7fcf080ad210>,
  <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
  <temba_client.v2.types.Flow at 0x7fcf080ad390>,
  <temba_client.v2.types.Flow at 0x7fcf080ad450>,
  <temba_client.v2.types.Flow at 0x7fcf080ad550>,
  <temba_client.v2.types.Flow at 0x7fcf080ad650>,
  <temba_client.v2.types.Flow at 0x7fcf080ad750>,
  <temba_client.v2.types.Flow at 0x7fcf080ad850>,
  <temba_client.v2.types.Flow at 0x7fcf080ad950>,
  <temba_client.v2.types.Flow at 0x7fcf080ada50>,
  <temba_client.v2.types.Flow at 0x7fcf080adb50>,
  <temba_client.v2.types.Flow at 0x7fcf080adc50>,
  <temba_client.v2.types.Flow at 0x7fcf080add10>,
  <temba_client.v2.types.Flow at 0x7fcf080addd0>,
  <temba_client.v2.types.Flow at 0x7fcf080ade90>,
  <temba_client.v2.types.Flow at 0x7fcf080adf50>,
  <temba_client.v2.types.Flow at 0x7fcf080b1050>,
  <temba_client.v2.types.Flow at 0x7fcf080b1110>,
  <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
  <temba_client.v2.types.Flow at 0x7fcf080b1290>,
  <temba_client.v2.types.Flow at 0x7fcf080b1350>,
  <temba_client.v2.types.Flow at 0x7fcf080b1410>]]

In [20]: f = flows[0][0]

In [21]: f
Out[21]: <temba_client.v2.types.Flow at 0x7fcf08071dd0>

In [22]: f.name
Out[22]: u'Dispatch in'

In [23]: [x.name for x flows[0]]
  File "<ipython-input-23-6685073b6dad>", line 1
    [x.name for x flows[0]]
                      ^
SyntaxError: invalid syntax


In [24]: [x.name for x in flows[0]]
Out[24]: 
[u'Dispatch in',
 u'Dispatch',
 u'MNCH week Phone Return',
 u'Training on writing SMS',
 u'Use Trigger Word',
 u'MNP Program',
 u'MNP Registration',
 u'IMAM SMS Router',
 u'stockouttest',
 u'Letters_numbers',
 u'MNP Stock Monitoring Flow',
 u'Copy of MNP Stock Monitoring Flow',
 u'MNP LGA NFP Follow up',
 u'Copy of MNP Stock Monitoring Flow',
 u'Health poll (One.org)',
 u'MNP LGA NFP Follow up',
 u'SDGs ',
 u'MNP stock follow up',
 u'MNP Stock Monitoring Flow',
 u'Micronutrient Powders Caregivers',
 u'MNDC Taskforce',
 u'Copy of IMAM Register',
 u'MNCHW Supply Monitor - Flow B',
 u'Single Message (14159)',
 u'Single Message (14157)',
 u'test',
 u'MNCHW test',
 u'IMAM LGA State Stocks',
 u'Test contact',
 u'Validate',
 u'MYR Demo',
 u'IMAM Validate',
 u'IYCF',
 u'Choose Language',
 u'IMAM Stock',
 u'IMAM Screening',
 u'IMAM Program',
 u'IMAM Register',
 u'IMAM',
 u'MNCHW supply confirmation',
 u'Federal Monitors Confirmation',
 u'yvb',
 u'RPBA CMAM Monitoring',
 u'mnchlgatt',
 u'mnchlgatt',
 u'mnchw lga nfp flow B',
 u'MNCH lga nfp test',
 u'MNCHW LGA NFP-Day 2',
 u'MNCHW LGA Focal Person-Day 1',
 u'MNCHW Supply-Flow B',
 u'MNCHW Supply Monitor- Flow A',
 u'MNCHW_Monitoring Register',
 u'Ping',
 u'SAM Start',
 u'Example Flow Nutrition (Arabic)',
 u'Copy of Example Flow Nutrition (English)',
 u'Example Flow Nutrition (English)',
 u'Single Message (10470)',
 u'Single Message (10469)',
 u'Single Message (10468)',
 u'Single Message (10467)',
 u'Single Message (10466)',
 u'Single Message (10465)',
 u'Single Message (10464)',
 u'Single Message (10463)',
 u'Single Message (10462)',
 u'Single Message (10461)',
 u'Single Message (10460)',
 u'Single Message (10459)',
 u'Single Message (10458)',
 u'Single Message (10457)',
 u'Single Message (10456)',
 u'Single Message (10455)',
 u'Single Message (10454)',
 u'Single Message (10453)',
 u'Single Message (10452)',
 u'Single Message (10451)',
 u'Single Message (10450)',
 u'Single Message (10449)',
 u'Single Message (10448)',
 u'Single Message (10447)',
 u'Single Message (10446)',
 u'Single Message (10445)',
 u'Single Message (10444)',
 u'Single Message (10443)',
 u'Single Message (10442)',
 u'Single Message (10441)',
 u'Single Message (10440)',
 u'Single Message (10439)',
 u'Single Message (10438)',
 u'Single Message (10437)',
 u'Single Message (10436)',
 u'Single Message (10435)',
 u'Single Message (10434)',
 u'Single Message (10433)',
 u'Single Message (10432)',
 u'Single Message (10431)',
 u'Single Message (10430)',
 u'Single Message (10429)',
 u'Single Message (10428)',
 u'Single Message (10427)',
 u'Single Message (10426)',
 u'Single Message (10425)',
 u'Single Message (10424)',
 u'Single Message (10423)',
 u'Single Message (10422)',
 u'Single Message (10421)',
 u'Single Message (10420)',
 u'Single Message (10419)',
 u'Single Message (10418)',
 u'Single Message (10417)',
 u'Single Message (10416)',
 u'Single Message (10415)',
 u'Single Message (10414)',
 u'Single Message (10413)',
 u'Single Message (10412)',
 u'Single Message (10411)',
 u'Single Message (10410)',
 u'Single Message (10409)',
 u'Single Message (10408)',
 u'Single Message (10407)',
 u'Single Message (10406)',
 u'Single Message (10405)',
 u'Single Message (10404)',
 u'Single Message (10403)',
 u'Single Message (10402)',
 u'Single Message (10401)',
 u'Single Message (10400)',
 u'Single Message (10399)',
 u'Single Message (10398)',
 u'Single Message (10397)',
 u'Single Message (10396)',
 u'Single Message (10395)',
 u'Single Message (10394)',
 u'Single Message (10393)',
 u'Single Message (10392)',
 u'Single Message (10391)',
 u'Single Message (10390)',
 u'Single Message (10389)',
 u'Single Message (10388)',
 u'Single Message (10387)',
 u'Single Message (10386)',
 u'Single Message (10385)',
 u'Single Message (10384)',
 u'Single Message (10383)',
 u'Single Message (10382)',
 u'Single Message (10381)',
 u'Single Message (10380)',
 u'Single Message (10379)',
 u'Single Message (10378)',
 u'Single Message (10377)',
 u'Single Message (10376)',
 u'Single Message (10375)',
 u'Single Message (10374)',
 u'Single Message (10373)',
 u'Single Message (10372)',
 u'Single Message (10371)',
 u'Single Message (10370)',
 u'Single Message (10369)',
 u'Single Message (10368)',
 u'Single Message (10367)',
 u'Single Message (10366)',
 u'Single Message (10365)',
 u'Single Message (10364)',
 u'Single Message (10363)',
 u'Single Message (10362)',
 u'Single Message (10361)',
 u'Single Message (10360)',
 u'Single Message (10359)',
 u'Single Message (10358)',
 u'Single Message (10357)',
 u'Single Message (10356)',
 u'Single Message (10355)',
 u'Single Message (10354)',
 u'Single Message (10353)',
 u'Single Message (10352)',
 u'Single Message (10351)',
 u'Single Message (10350)',
 u'Single Message (10349)',
 u'Single Message (10348)',
 u'Single Message (10347)',
 u'Single Message (10346)',
 u'Single Message (10345)',
 u'Single Message (10344)',
 u'Single Message (10343)',
 u'Single Message (10342)',
 u'Single Message (10341)',
 u'Single Message (10340)',
 u'Single Message (10339)',
 u'Single Message (10338)',
 u'Single Message (10337)',
 u'Single Message (10336)',
 u'Single Message (10335)',
 u'Single Message (10334)',
 u'Single Message (10333)',
 u'Single Message (10332)',
 u'Single Message (10331)',
 u'Single Message (10330)',
 u'Single Message (10329)',
 u'Single Message (10328)',
 u'Single Message (10327)',
 u'Single Message (10326)',
 u'Single Message (10325)',
 u'Single Message (10324)',
 u'Single Message (10323)',
 u'Single Message (10322)',
 u'Single Message (10321)',
 u'Single Message (10320)',
 u'Single Message (10319)',
 u'Single Message (10318)',
 u'Single Message (10317)',
 u'CHW Mother Registration (Notify Mother)',
 u'CHW Mother Registration',
 u'1st ANC visit',
 u'CHW Screening',
 u'CHW Daily Report',
 u'CHW Stocks',
 u'CHW Planning Populations',
 u'CHW Registration',
 u'SAM Validate',
 u'SAM Stock Report',
 u'SAM Stockout and Update',
 u'SAM Screen',
 u'SAM Register',
 u'SAM Program',
 u'SAM Despatch',
 u'Sample Flow -  Simple Poll',
 u'Sample Flow -  Satisfaction Survey',
 u'Sample Flow -  Order Status Checker',
 u'Sample Flow -  Group Chat']

In [25]: f
Out[25]: <temba_client.v2.types.Flow at 0x7fcf08071dd0>

In [26]: f.Runs
Out[26]: temba_client.v2.types.Runs

In [27]: f.Runs?
Docstring: <no docstring>
File:      ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/v2/types.py
Type:      ABCMeta

In [28]: f.runs?
Type:        Runs
String form: <temba_client.v2.types.Runs object at 0x7fcf08071f90>
File:        ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/v2/types.py
Docstring:   <no docstring>

In [29]: f.runs
Out[29]: <temba_client.v2.types.Runs at 0x7fcf08071f90>

In [30]: f.Runs
Out[30]: temba_client.v2.types.Runs

In [31]: f.Runs.active
Out[31]: <temba_client.serialization.IntegerField at 0x7fcf0c900790>

In [32]: {x.name for x in flows[0]}
Out[32]: 
{u'1st ANC visit',
 u'CHW Daily Report',
 u'CHW Mother Registration',
 u'CHW Mother Registration (Notify Mother)',
 u'CHW Planning Populations',
 u'CHW Registration',
 u'CHW Screening',
 u'CHW Stocks',
 u'Choose Language',
 u'Copy of Example Flow Nutrition (English)',
 u'Copy of IMAM Register',
 u'Copy of MNP Stock Monitoring Flow',
 u'Dispatch',
 u'Dispatch in',
 u'Example Flow Nutrition (Arabic)',
 u'Example Flow Nutrition (English)',
 u'Federal Monitors Confirmation',
 u'Health poll (One.org)',
 u'IMAM',
 u'IMAM LGA State Stocks',
 u'IMAM Program',
 u'IMAM Register',
 u'IMAM SMS Router',
 u'IMAM Screening',
 u'IMAM Stock',
 u'IMAM Validate',
 u'IYCF',
 u'Letters_numbers',
 u'MNCH lga nfp test',
 u'MNCH week Phone Return',
 u'MNCHW LGA Focal Person-Day 1',
 u'MNCHW LGA NFP-Day 2',
 u'MNCHW Supply Monitor - Flow B',
 u'MNCHW Supply Monitor- Flow A',
 u'MNCHW Supply-Flow B',
 u'MNCHW supply confirmation',
 u'MNCHW test',
 u'MNCHW_Monitoring Register',
 u'MNDC Taskforce',
 u'MNP LGA NFP Follow up',
 u'MNP Program',
 u'MNP Registration',
 u'MNP Stock Monitoring Flow',
 u'MNP stock follow up',
 u'MYR Demo',
 u'Micronutrient Powders Caregivers',
 u'Ping',
 u'RPBA CMAM Monitoring',
 u'SAM Despatch',
 u'SAM Program',
 u'SAM Register',
 u'SAM Screen',
 u'SAM Start',
 u'SAM Stock Report',
 u'SAM Stockout and Update',
 u'SAM Validate',
 u'SDGs ',
 u'Sample Flow -  Group Chat',
 u'Sample Flow -  Order Status Checker',
 u'Sample Flow -  Satisfaction Survey',
 u'Sample Flow -  Simple Poll',
 u'Single Message (10317)',
 u'Single Message (10318)',
 u'Single Message (10319)',
 u'Single Message (10320)',
 u'Single Message (10321)',
 u'Single Message (10322)',
 u'Single Message (10323)',
 u'Single Message (10324)',
 u'Single Message (10325)',
 u'Single Message (10326)',
 u'Single Message (10327)',
 u'Single Message (10328)',
 u'Single Message (10329)',
 u'Single Message (10330)',
 u'Single Message (10331)',
 u'Single Message (10332)',
 u'Single Message (10333)',
 u'Single Message (10334)',
 u'Single Message (10335)',
 u'Single Message (10336)',
 u'Single Message (10337)',
 u'Single Message (10338)',
 u'Single Message (10339)',
 u'Single Message (10340)',
 u'Single Message (10341)',
 u'Single Message (10342)',
 u'Single Message (10343)',
 u'Single Message (10344)',
 u'Single Message (10345)',
 u'Single Message (10346)',
 u'Single Message (10347)',
 u'Single Message (10348)',
 u'Single Message (10349)',
 u'Single Message (10350)',
 u'Single Message (10351)',
 u'Single Message (10352)',
 u'Single Message (10353)',
 u'Single Message (10354)',
 u'Single Message (10355)',
 u'Single Message (10356)',
 u'Single Message (10357)',
 u'Single Message (10358)',
 u'Single Message (10359)',
 u'Single Message (10360)',
 u'Single Message (10361)',
 u'Single Message (10362)',
 u'Single Message (10363)',
 u'Single Message (10364)',
 u'Single Message (10365)',
 u'Single Message (10366)',
 u'Single Message (10367)',
 u'Single Message (10368)',
 u'Single Message (10369)',
 u'Single Message (10370)',
 u'Single Message (10371)',
 u'Single Message (10372)',
 u'Single Message (10373)',
 u'Single Message (10374)',
 u'Single Message (10375)',
 u'Single Message (10376)',
 u'Single Message (10377)',
 u'Single Message (10378)',
 u'Single Message (10379)',
 u'Single Message (10380)',
 u'Single Message (10381)',
 u'Single Message (10382)',
 u'Single Message (10383)',
 u'Single Message (10384)',
 u'Single Message (10385)',
 u'Single Message (10386)',
 u'Single Message (10387)',
 u'Single Message (10388)',
 u'Single Message (10389)',
 u'Single Message (10390)',
 u'Single Message (10391)',
 u'Single Message (10392)',
 u'Single Message (10393)',
 u'Single Message (10394)',
 u'Single Message (10395)',
 u'Single Message (10396)',
 u'Single Message (10397)',
 u'Single Message (10398)',
 u'Single Message (10399)',
 u'Single Message (10400)',
 u'Single Message (10401)',
 u'Single Message (10402)',
 u'Single Message (10403)',
 u'Single Message (10404)',
 u'Single Message (10405)',
 u'Single Message (10406)',
 u'Single Message (10407)',
 u'Single Message (10408)',
 u'Single Message (10409)',
 u'Single Message (10410)',
 u'Single Message (10411)',
 u'Single Message (10412)',
 u'Single Message (10413)',
 u'Single Message (10414)',
 u'Single Message (10415)',
 u'Single Message (10416)',
 u'Single Message (10417)',
 u'Single Message (10418)',
 u'Single Message (10419)',
 u'Single Message (10420)',
 u'Single Message (10421)',
 u'Single Message (10422)',
 u'Single Message (10423)',
 u'Single Message (10424)',
 u'Single Message (10425)',
 u'Single Message (10426)',
 u'Single Message (10427)',
 u'Single Message (10428)',
 u'Single Message (10429)',
 u'Single Message (10430)',
 u'Single Message (10431)',
 u'Single Message (10432)',
 u'Single Message (10433)',
 u'Single Message (10434)',
 u'Single Message (10435)',
 u'Single Message (10436)',
 u'Single Message (10437)',
 u'Single Message (10438)',
 u'Single Message (10439)',
 u'Single Message (10440)',
 u'Single Message (10441)',
 u'Single Message (10442)',
 u'Single Message (10443)',
 u'Single Message (10444)',
 u'Single Message (10445)',
 u'Single Message (10446)',
 u'Single Message (10447)',
 u'Single Message (10448)',
 u'Single Message (10449)',
 u'Single Message (10450)',
 u'Single Message (10451)',
 u'Single Message (10452)',
 u'Single Message (10453)',
 u'Single Message (10454)',
 u'Single Message (10455)',
 u'Single Message (10456)',
 u'Single Message (10457)',
 u'Single Message (10458)',
 u'Single Message (10459)',
 u'Single Message (10460)',
 u'Single Message (10461)',
 u'Single Message (10462)',
 u'Single Message (10463)',
 u'Single Message (10464)',
 u'Single Message (10465)',
 u'Single Message (10466)',
 u'Single Message (10467)',
 u'Single Message (10468)',
 u'Single Message (10469)',
 u'Single Message (10470)',
 u'Single Message (14157)',
 u'Single Message (14159)',
 u'Test contact',
 u'Training on writing SMS',
 u'Use Trigger Word',
 u'Validate',
 u'mnchlgatt',
 u'mnchw lga nfp flow B',
 u'stockouttest',
 u'test',
 u'yvb'}

In [33]: {x.name: x for x in flows[0]}
Out[33]: 
{u'1st ANC visit': <temba_client.v2.types.Flow at 0x7fcf080ad650>,
 u'CHW Daily Report': <temba_client.v2.types.Flow at 0x7fcf080ad850>,
 u'CHW Mother Registration': <temba_client.v2.types.Flow at 0x7fcf080ad550>,
 u'CHW Mother Registration (Notify Mother)': <temba_client.v2.types.Flow at 0x7fcf080ad450>,
 u'CHW Planning Populations': <temba_client.v2.types.Flow at 0x7fcf080ada50>,
 u'CHW Registration': <temba_client.v2.types.Flow at 0x7fcf080adb50>,
 u'CHW Screening': <temba_client.v2.types.Flow at 0x7fcf080ad750>,
 u'CHW Stocks': <temba_client.v2.types.Flow at 0x7fcf080ad950>,
 u'Choose Language': <temba_client.v2.types.Flow at 0x7fcefb483a50>,
 u'Copy of Example Flow Nutrition (English)': <temba_client.v2.types.Flow at 0x7fcefb484d50>,
 u'Copy of IMAM Register': <temba_client.v2.types.Flow at 0x7fcefb482fd0>,
 u'Copy of MNP Stock Monitoring Flow': <temba_client.v2.types.Flow at 0x7fcefb482990>,
 u'Dispatch': <temba_client.v2.types.Flow at 0x7fcf08071c90>,
 u'Dispatch in': <temba_client.v2.types.Flow at 0x7fcf08071dd0>,
 u'Example Flow Nutrition (Arabic)': <temba_client.v2.types.Flow at 0x7fcefb484c90>,
 u'Example Flow Nutrition (English)': <temba_client.v2.types.Flow at 0x7fcefb484e10>,
 u'Federal Monitors Confirmation': <temba_client.v2.types.Flow at 0x7fcefb484210>,
 u'Health poll (One.org)': <temba_client.v2.types.Flow at 0x7fcefb482a50>,
 u'IMAM': <temba_client.v2.types.Flow at 0x7fcefb484090>,
 u'IMAM LGA State Stocks': <temba_client.v2.types.Flow at 0x7fcefb483490>,
 u'IMAM Program': <temba_client.v2.types.Flow at 0x7fcefb483dd0>,
 u'IMAM Register': <temba_client.v2.types.Flow at 0x7fcefb483f10>,
 u'IMAM SMS Router': <temba_client.v2.types.Flow at 0x7fcefb482490>,
 u'IMAM Screening': <temba_client.v2.types.Flow at 0x7fcefb483c90>,
 u'IMAM Stock': <temba_client.v2.types.Flow at 0x7fcefb483b50>,
 u'IMAM Validate': <temba_client.v2.types.Flow at 0x7fcefb483810>,
 u'IYCF': <temba_client.v2.types.Flow at 0x7fcefb483950>,
 u'Letters_numbers': <temba_client.v2.types.Flow at 0x7fcefb482690>,
 u'MNCH lga nfp test': <temba_client.v2.types.Flow at 0x7fcefb484690>,
 u'MNCH week Phone Return': <temba_client.v2.types.Flow at 0x7fcefb482050>,
 u'MNCHW LGA Focal Person-Day 1': <temba_client.v2.types.Flow at 0x7fcefb484810>,
 u'MNCHW LGA NFP-Day 2': <temba_client.v2.types.Flow at 0x7fcefb484750>,
 u'MNCHW Supply Monitor - Flow B': <temba_client.v2.types.Flow at 0x7fcefb4830d0>,
 u'MNCHW Supply Monitor- Flow A': <temba_client.v2.types.Flow at 0x7fcefb484990>,
 u'MNCHW Supply-Flow B': <temba_client.v2.types.Flow at 0x7fcefb4848d0>,
 u'MNCHW supply confirmation': <temba_client.v2.types.Flow at 0x7fcefb484150>,
 u'MNCHW test': <temba_client.v2.types.Flow at 0x7fcefb4833d0>,
 u'MNCHW_Monitoring Register': <temba_client.v2.types.Flow at 0x7fcefb484a50>,
 u'MNDC Taskforce': <temba_client.v2.types.Flow at 0x7fcefb482f10>,
 u'MNP LGA NFP Follow up': <temba_client.v2.types.Flow at 0x7fcefb482b10>,
 u'MNP Program': <temba_client.v2.types.Flow at 0x7fcefb482290>,
 u'MNP Registration': <temba_client.v2.types.Flow at 0x7fcefb482390>,
 u'MNP Stock Monitoring Flow': <temba_client.v2.types.Flow at 0x7fcefb482d90>,
 u'MNP stock follow up': <temba_client.v2.types.Flow at 0x7fcefb482c90>,
 u'MYR Demo': <temba_client.v2.types.Flow at 0x7fcefb483750>,
 u'Micronutrient Powders Caregivers': <temba_client.v2.types.Flow at 0x7fcefb482e50>,
 u'Ping': <temba_client.v2.types.Flow at 0x7fcefb484b10>,
 u'RPBA CMAM Monitoring': <temba_client.v2.types.Flow at 0x7fcefb484390>,
 u'SAM Despatch': <temba_client.v2.types.Flow at 0x7fcf080b1110>,
 u'SAM Program': <temba_client.v2.types.Flow at 0x7fcf080b1050>,
 u'SAM Register': <temba_client.v2.types.Flow at 0x7fcf080adf50>,
 u'SAM Screen': <temba_client.v2.types.Flow at 0x7fcf080ade90>,
 u'SAM Start': <temba_client.v2.types.Flow at 0x7fcefb484bd0>,
 u'SAM Stock Report': <temba_client.v2.types.Flow at 0x7fcf080add10>,
 u'SAM Stockout and Update': <temba_client.v2.types.Flow at 0x7fcf080addd0>,
 u'SAM Validate': <temba_client.v2.types.Flow at 0x7fcf080adc50>,
 u'SDGs ': <temba_client.v2.types.Flow at 0x7fcefb482bd0>,
 u'Sample Flow -  Group Chat': <temba_client.v2.types.Flow at 0x7fcf080b1410>,
 u'Sample Flow -  Order Status Checker': <temba_client.v2.types.Flow at 0x7fcf080b1350>,
 u'Sample Flow -  Satisfaction Survey': <temba_client.v2.types.Flow at 0x7fcf080b1290>,
 u'Sample Flow -  Simple Poll': <temba_client.v2.types.Flow at 0x7fcf080b11d0>,
 u'Single Message (10317)': <temba_client.v2.types.Flow at 0x7fcf080ad390>,
 u'Single Message (10318)': <temba_client.v2.types.Flow at 0x7fcf080ad2d0>,
 u'Single Message (10319)': <temba_client.v2.types.Flow at 0x7fcf080ad210>,
 u'Single Message (10320)': <temba_client.v2.types.Flow at 0x7fcf080ad150>,
 u'Single Message (10321)': <temba_client.v2.types.Flow at 0x7fcf080ad090>,
 u'Single Message (10322)': <temba_client.v2.types.Flow at 0x7fcf080a9f90>,
 u'Single Message (10323)': <temba_client.v2.types.Flow at 0x7fcf080a9ed0>,
 u'Single Message (10324)': <temba_client.v2.types.Flow at 0x7fcf080a9e10>,
 u'Single Message (10325)': <temba_client.v2.types.Flow at 0x7fcf080a9d50>,
 u'Single Message (10326)': <temba_client.v2.types.Flow at 0x7fcf080a9c90>,
 u'Single Message (10327)': <temba_client.v2.types.Flow at 0x7fcf080a9bd0>,
 u'Single Message (10328)': <temba_client.v2.types.Flow at 0x7fcf080a9b10>,
 u'Single Message (10329)': <temba_client.v2.types.Flow at 0x7fcf080a9a50>,
 u'Single Message (10330)': <temba_client.v2.types.Flow at 0x7fcf080a9990>,
 u'Single Message (10331)': <temba_client.v2.types.Flow at 0x7fcf080a98d0>,
 u'Single Message (10332)': <temba_client.v2.types.Flow at 0x7fcf080a9810>,
 u'Single Message (10333)': <temba_client.v2.types.Flow at 0x7fcf080a9750>,
 u'Single Message (10334)': <temba_client.v2.types.Flow at 0x7fcf080a9690>,
 u'Single Message (10335)': <temba_client.v2.types.Flow at 0x7fcf080a95d0>,
 u'Single Message (10336)': <temba_client.v2.types.Flow at 0x7fcf080a9510>,
 u'Single Message (10337)': <temba_client.v2.types.Flow at 0x7fcf080a9450>,
 u'Single Message (10338)': <temba_client.v2.types.Flow at 0x7fcf080a9390>,
 u'Single Message (10339)': <temba_client.v2.types.Flow at 0x7fcf080a92d0>,
 u'Single Message (10340)': <temba_client.v2.types.Flow at 0x7fcf080a9210>,
 u'Single Message (10341)': <temba_client.v2.types.Flow at 0x7fcf080a9150>,
 u'Single Message (10342)': <temba_client.v2.types.Flow at 0x7fcf080a9090>,
 u'Single Message (10343)': <temba_client.v2.types.Flow at 0x7fcf080a4f90>,
 u'Single Message (10344)': <temba_client.v2.types.Flow at 0x7fcf080a4ed0>,
 u'Single Message (10345)': <temba_client.v2.types.Flow at 0x7fcf080a4e10>,
 u'Single Message (10346)': <temba_client.v2.types.Flow at 0x7fcf080a4d50>,
 u'Single Message (10347)': <temba_client.v2.types.Flow at 0x7fcf080a4c90>,
 u'Single Message (10348)': <temba_client.v2.types.Flow at 0x7fcf080a4bd0>,
 u'Single Message (10349)': <temba_client.v2.types.Flow at 0x7fcf080a4b10>,
 u'Single Message (10350)': <temba_client.v2.types.Flow at 0x7fcf080a4a50>,
 u'Single Message (10351)': <temba_client.v2.types.Flow at 0x7fcf080a4990>,
 u'Single Message (10352)': <temba_client.v2.types.Flow at 0x7fcf080a48d0>,
 u'Single Message (10353)': <temba_client.v2.types.Flow at 0x7fcf080a4810>,
 u'Single Message (10354)': <temba_client.v2.types.Flow at 0x7fcf080a4750>,
 u'Single Message (10355)': <temba_client.v2.types.Flow at 0x7fcf080a4690>,
 u'Single Message (10356)': <temba_client.v2.types.Flow at 0x7fcf080a45d0>,
 u'Single Message (10357)': <temba_client.v2.types.Flow at 0x7fcf080a4510>,
 u'Single Message (10358)': <temba_client.v2.types.Flow at 0x7fcf080a4450>,
 u'Single Message (10359)': <temba_client.v2.types.Flow at 0x7fcf080a4390>,
 u'Single Message (10360)': <temba_client.v2.types.Flow at 0x7fcf080a42d0>,
 u'Single Message (10361)': <temba_client.v2.types.Flow at 0x7fcf080a4210>,
 u'Single Message (10362)': <temba_client.v2.types.Flow at 0x7fcf080a4150>,
 u'Single Message (10363)': <temba_client.v2.types.Flow at 0x7fcf080a4090>,
 u'Single Message (10364)': <temba_client.v2.types.Flow at 0x7fcf080a0f90>,
 u'Single Message (10365)': <temba_client.v2.types.Flow at 0x7fcf080a0ed0>,
 u'Single Message (10366)': <temba_client.v2.types.Flow at 0x7fcf080a0e10>,
 u'Single Message (10367)': <temba_client.v2.types.Flow at 0x7fcf080a0d50>,
 u'Single Message (10368)': <temba_client.v2.types.Flow at 0x7fcf080a0c90>,
 u'Single Message (10369)': <temba_client.v2.types.Flow at 0x7fcf080a0bd0>,
 u'Single Message (10370)': <temba_client.v2.types.Flow at 0x7fcf080a0b10>,
 u'Single Message (10371)': <temba_client.v2.types.Flow at 0x7fcf080a0a50>,
 u'Single Message (10372)': <temba_client.v2.types.Flow at 0x7fcf080a0990>,
 u'Single Message (10373)': <temba_client.v2.types.Flow at 0x7fcf080a08d0>,
 u'Single Message (10374)': <temba_client.v2.types.Flow at 0x7fcf080a0810>,
 u'Single Message (10375)': <temba_client.v2.types.Flow at 0x7fcf080a0750>,
 u'Single Message (10376)': <temba_client.v2.types.Flow at 0x7fcf080a0690>,
 u'Single Message (10377)': <temba_client.v2.types.Flow at 0x7fcf080a05d0>,
 u'Single Message (10378)': <temba_client.v2.types.Flow at 0x7fcf080a0510>,
 u'Single Message (10379)': <temba_client.v2.types.Flow at 0x7fcf080a0450>,
 u'Single Message (10380)': <temba_client.v2.types.Flow at 0x7fcf080a0390>,
 u'Single Message (10381)': <temba_client.v2.types.Flow at 0x7fcf080a02d0>,
 u'Single Message (10382)': <temba_client.v2.types.Flow at 0x7fcf080a0210>,
 u'Single Message (10383)': <temba_client.v2.types.Flow at 0x7fcf080a0150>,
 u'Single Message (10384)': <temba_client.v2.types.Flow at 0x7fcf080a0090>,
 u'Single Message (10385)': <temba_client.v2.types.Flow at 0x7fcf0809cf90>,
 u'Single Message (10386)': <temba_client.v2.types.Flow at 0x7fcf0809ced0>,
 u'Single Message (10387)': <temba_client.v2.types.Flow at 0x7fcf0809ce10>,
 u'Single Message (10388)': <temba_client.v2.types.Flow at 0x7fcf0809cd50>,
 u'Single Message (10389)': <temba_client.v2.types.Flow at 0x7fcf0809cc90>,
 u'Single Message (10390)': <temba_client.v2.types.Flow at 0x7fcf0809cbd0>,
 u'Single Message (10391)': <temba_client.v2.types.Flow at 0x7fcf0809cb10>,
 u'Single Message (10392)': <temba_client.v2.types.Flow at 0x7fcf0809ca50>,
 u'Single Message (10393)': <temba_client.v2.types.Flow at 0x7fcf0809c990>,
 u'Single Message (10394)': <temba_client.v2.types.Flow at 0x7fcf0809c8d0>,
 u'Single Message (10395)': <temba_client.v2.types.Flow at 0x7fcf0809c810>,
 u'Single Message (10396)': <temba_client.v2.types.Flow at 0x7fcf0809c750>,
 u'Single Message (10397)': <temba_client.v2.types.Flow at 0x7fcf0809c690>,
 u'Single Message (10398)': <temba_client.v2.types.Flow at 0x7fcf0809c5d0>,
 u'Single Message (10399)': <temba_client.v2.types.Flow at 0x7fcf0809c510>,
 u'Single Message (10400)': <temba_client.v2.types.Flow at 0x7fcf0809c450>,
 u'Single Message (10401)': <temba_client.v2.types.Flow at 0x7fcf0809c390>,
 u'Single Message (10402)': <temba_client.v2.types.Flow at 0x7fcf0809c2d0>,
 u'Single Message (10403)': <temba_client.v2.types.Flow at 0x7fcf0809c210>,
 u'Single Message (10404)': <temba_client.v2.types.Flow at 0x7fcf0809c150>,
 u'Single Message (10405)': <temba_client.v2.types.Flow at 0x7fcf0809c090>,
 u'Single Message (10406)': <temba_client.v2.types.Flow at 0x7fcf08098f90>,
 u'Single Message (10407)': <temba_client.v2.types.Flow at 0x7fcf08098ed0>,
 u'Single Message (10408)': <temba_client.v2.types.Flow at 0x7fcf08098e10>,
 u'Single Message (10409)': <temba_client.v2.types.Flow at 0x7fcf08098d50>,
 u'Single Message (10410)': <temba_client.v2.types.Flow at 0x7fcf08098c90>,
 u'Single Message (10411)': <temba_client.v2.types.Flow at 0x7fcf08098bd0>,
 u'Single Message (10412)': <temba_client.v2.types.Flow at 0x7fcf08098b10>,
 u'Single Message (10413)': <temba_client.v2.types.Flow at 0x7fcf08098a50>,
 u'Single Message (10414)': <temba_client.v2.types.Flow at 0x7fcf08098990>,
 u'Single Message (10415)': <temba_client.v2.types.Flow at 0x7fcf080988d0>,
 u'Single Message (10416)': <temba_client.v2.types.Flow at 0x7fcf08098810>,
 u'Single Message (10417)': <temba_client.v2.types.Flow at 0x7fcf08098750>,
 u'Single Message (10418)': <temba_client.v2.types.Flow at 0x7fcf08098690>,
 u'Single Message (10419)': <temba_client.v2.types.Flow at 0x7fcf080985d0>,
 u'Single Message (10420)': <temba_client.v2.types.Flow at 0x7fcf08098510>,
 u'Single Message (10421)': <temba_client.v2.types.Flow at 0x7fcf08098450>,
 u'Single Message (10422)': <temba_client.v2.types.Flow at 0x7fcf08098390>,
 u'Single Message (10423)': <temba_client.v2.types.Flow at 0x7fcf080982d0>,
 u'Single Message (10424)': <temba_client.v2.types.Flow at 0x7fcf08098210>,
 u'Single Message (10425)': <temba_client.v2.types.Flow at 0x7fcf08098150>,
 u'Single Message (10426)': <temba_client.v2.types.Flow at 0x7fcf08098090>,
 u'Single Message (10427)': <temba_client.v2.types.Flow at 0x7fcf08093f90>,
 u'Single Message (10428)': <temba_client.v2.types.Flow at 0x7fcf08093ed0>,
 u'Single Message (10429)': <temba_client.v2.types.Flow at 0x7fcf08093e10>,
 u'Single Message (10430)': <temba_client.v2.types.Flow at 0x7fcf08093d50>,
 u'Single Message (10431)': <temba_client.v2.types.Flow at 0x7fcf08093c90>,
 u'Single Message (10432)': <temba_client.v2.types.Flow at 0x7fcf08093bd0>,
 u'Single Message (10433)': <temba_client.v2.types.Flow at 0x7fcf08093b10>,
 u'Single Message (10434)': <temba_client.v2.types.Flow at 0x7fcf08093a50>,
 u'Single Message (10435)': <temba_client.v2.types.Flow at 0x7fcf08093990>,
 u'Single Message (10436)': <temba_client.v2.types.Flow at 0x7fcf080938d0>,
 u'Single Message (10437)': <temba_client.v2.types.Flow at 0x7fcf08093810>,
 u'Single Message (10438)': <temba_client.v2.types.Flow at 0x7fcf08093750>,
 u'Single Message (10439)': <temba_client.v2.types.Flow at 0x7fcf08093690>,
 u'Single Message (10440)': <temba_client.v2.types.Flow at 0x7fcf080935d0>,
 u'Single Message (10441)': <temba_client.v2.types.Flow at 0x7fcf08093510>,
 u'Single Message (10442)': <temba_client.v2.types.Flow at 0x7fcf08093450>,
 u'Single Message (10443)': <temba_client.v2.types.Flow at 0x7fcf08093390>,
 u'Single Message (10444)': <temba_client.v2.types.Flow at 0x7fcf080932d0>,
 u'Single Message (10445)': <temba_client.v2.types.Flow at 0x7fcf08093210>,
 u'Single Message (10446)': <temba_client.v2.types.Flow at 0x7fcf08093150>,
 u'Single Message (10447)': <temba_client.v2.types.Flow at 0x7fcf08093090>,
 u'Single Message (10448)': <temba_client.v2.types.Flow at 0x7fcf0808ff90>,
 u'Single Message (10449)': <temba_client.v2.types.Flow at 0x7fcf0808fed0>,
 u'Single Message (10450)': <temba_client.v2.types.Flow at 0x7fcf0808fe10>,
 u'Single Message (10451)': <temba_client.v2.types.Flow at 0x7fcf0808fd50>,
 u'Single Message (10452)': <temba_client.v2.types.Flow at 0x7fcf0808fc90>,
 u'Single Message (10453)': <temba_client.v2.types.Flow at 0x7fcf0808fbd0>,
 u'Single Message (10454)': <temba_client.v2.types.Flow at 0x7fcf0808fb10>,
 u'Single Message (10455)': <temba_client.v2.types.Flow at 0x7fcf0808fa50>,
 u'Single Message (10456)': <temba_client.v2.types.Flow at 0x7fcf0808f990>,
 u'Single Message (10457)': <temba_client.v2.types.Flow at 0x7fcf0808f8d0>,
 u'Single Message (10458)': <temba_client.v2.types.Flow at 0x7fcf0808f810>,
 u'Single Message (10459)': <temba_client.v2.types.Flow at 0x7fcf0808f750>,
 u'Single Message (10460)': <temba_client.v2.types.Flow at 0x7fcf0808f690>,
 u'Single Message (10461)': <temba_client.v2.types.Flow at 0x7fcf0808f5d0>,
 u'Single Message (10462)': <temba_client.v2.types.Flow at 0x7fcf0808f510>,
 u'Single Message (10463)': <temba_client.v2.types.Flow at 0x7fcf0808f450>,
 u'Single Message (10464)': <temba_client.v2.types.Flow at 0x7fcf0808f390>,
 u'Single Message (10465)': <temba_client.v2.types.Flow at 0x7fcf0808f2d0>,
 u'Single Message (10466)': <temba_client.v2.types.Flow at 0x7fcf0808f210>,
 u'Single Message (10467)': <temba_client.v2.types.Flow at 0x7fcf0808f150>,
 u'Single Message (10468)': <temba_client.v2.types.Flow at 0x7fcf0808f090>,
 u'Single Message (10469)': <temba_client.v2.types.Flow at 0x7fcefb484f90>,
 u'Single Message (10470)': <temba_client.v2.types.Flow at 0x7fcefb484ed0>,
 u'Single Message (14157)': <temba_client.v2.types.Flow at 0x7fcefb483250>,
 u'Single Message (14159)': <temba_client.v2.types.Flow at 0x7fcefb483190>,
 u'Test contact': <temba_client.v2.types.Flow at 0x7fcefb4835d0>,
 u'Training on writing SMS': <temba_client.v2.types.Flow at 0x7fcefb482110>,
 u'Use Trigger Word': <temba_client.v2.types.Flow at 0x7fcefb4821d0>,
 u'Validate': <temba_client.v2.types.Flow at 0x7fcefb483690>,
 u'mnchlgatt': <temba_client.v2.types.Flow at 0x7fcefb484510>,
 u'mnchw lga nfp flow B': <temba_client.v2.types.Flow at 0x7fcefb4845d0>,
 u'stockouttest': <temba_client.v2.types.Flow at 0x7fcefb4825d0>,
 u'test': <temba_client.v2.types.Flow at 0x7fcefb483310>,
 u'yvb': <temba_client.v2.types.Flow at 0x7fcefb4842d0>}

In [34]: {x.name: x for x in flows[0]}[u'IMAM Program']
Out[34]: <temba_client.v2.types.Flow at 0x7fcefb483dd0>

In [35]: f = {x.name: x for x in flows[0]}[u'IMAM Program']

In [36]: f.runs
Out[36]: <temba_client.v2.types.Runs at 0x7fcefb483e10>

In [37]: f.Runs == f.runs
Out[37]: False

In [38]: f.Runs.active
Out[38]: <temba_client.serialization.IntegerField at 0x7fcf0c900790>

In [39]: f.Runs.active?
Type:        IntegerField
String form: <temba_client.serialization.IntegerField object at 0x7fcf0c900790>
File:        ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/serialization.py
Docstring:   <no docstring>

In [40]: f.Runs.active()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-40-a85b8391cabb> in <module>()
----> 1 f.Runs.active()

TypeError: 'IntegerField' object is not callable

In [41]: f.Runs.active
Out[41]: <temba_client.serialization.IntegerField at 0x7fcf0c900790>

In [42]: f.Runs.active.deserialize
Out[42]: <bound method IntegerField.deserialize of <temba_client.serialization.IntegerField object at 0x7fcf0c900790>>

In [43]: f.Runs.active.deserialize()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-43-1d1ca81f2917> in <module>()
----> 1 f.Runs.active.deserialize()

TypeError: deserialize() takes exactly 2 arguments (1 given)

In [44]: f.Runs.active.src

In [45]: f.Runs.active.optional
Out[45]: False

In [46]: f.Runs.active
Out[46]: <temba_client.serialization.IntegerField at 0x7fcf0c900790>

In [47]: f.runs.completed
Out[47]: 34784

In [48]: f.runs.active
Out[48]: 9

In [49]: f.runs.create
Out[49]: <bound method ABCMeta.create of <class 'temba_client.v2.types.Runs'>>

In [50]: a
Out[50]: <temba_client.clients.CursorIterator at 0x7fcf080711d0>

In [51]: client
Out[51]: <temba_client.v2.TembaClient at 0x7fcf08081590>

In [52]: client.get_runs
Out[52]: <bound method TembaClient.get_runs of <temba_client.v2.TembaClient object at 0x7fcf08081590>>

In [53]: client.get_runs?
Signature: client.get_runs(id=None, flow=None, contact=None, responded=None, before=None, after=None)
Docstring:
Gets all matching flow runs

:param id: flow run id
:param flow: flow object or UUID
:param contact: contact object or UUID
:param responded: whether to limit results to runs with responses
:param datetime before: modified before
:param datetime after: modified after
:return: flow run query
File:      ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/v2/__init__.py
Type:      instancemethod

In [54]: f
Out[54]: <temba_client.v2.types.Flow at 0x7fcefb483dd0>

In [55]: f.uuid
Out[55]: u'a9eed2f3-a92c-48dd-aa10-4f139b1171a4'

In [56]: client.get_runs(flow=f)
Out[56]: <temba_client.clients.CursorQuery at 0x7fcf0810cbd0>

In [57]: r = client.get_runs(flow=f).iterfetches()

In [58]: r
Out[58]: <temba_client.clients.CursorIterator at 0x7fcf080c4690>

In [59]: r.next()
Out[59]: 
[<temba_client.v2.types.Run at 0x7fcf080c4c10>,
 <temba_client.v2.types.Run at 0x7fcefa7ba9d0>,
 <temba_client.v2.types.Run at 0x7fcefa711dd0>,
 <temba_client.v2.types.Run at 0x7fcefa713d50>,
 <temba_client.v2.types.Run at 0x7fcefa714990>,
 <temba_client.v2.types.Run at 0x7fcefa716dd0>,
 <temba_client.v2.types.Run at 0x7fcefa71d250>,
 <temba_client.v2.types.Run at 0x7fcefa721690>,
 <temba_client.v2.types.Run at 0x7fcefa725410>,
 <temba_client.v2.types.Run at 0x7fcefa725810>,
 <temba_client.v2.types.Run at 0x7fcefb389350>,
 <temba_client.v2.types.Run at 0x7fcefb38d790>,
 <temba_client.v2.types.Run at 0x7fcefb391bd0>,
 <temba_client.v2.types.Run at 0x7fcefb398050>,
 <temba_client.v2.types.Run at 0x7fcefb39c590>,
 <temba_client.v2.types.Run at 0x7fcefb3a09d0>,
 <temba_client.v2.types.Run at 0x7fcefb3a3e10>,
 <temba_client.v2.types.Run at 0x7fcefb3ab310>,
 <temba_client.v2.types.Run at 0x7fcefb3ae850>,
 <temba_client.v2.types.Run at 0x7fcefb3b2c90>,
 <temba_client.v2.types.Run at 0x7fcefb3b9110>,
 <temba_client.v2.types.Run at 0x7fcefb3bd550>,
 <temba_client.v2.types.Run at 0x7fcefb3c1990>,
 <temba_client.v2.types.Run at 0x7fcefb3c4e50>,
 <temba_client.v2.types.Run at 0x7fcefb34c3d0>,
 <temba_client.v2.types.Run at 0x7fcefb350810>,
 <temba_client.v2.types.Run at 0x7fcefb353c50>,
 <temba_client.v2.types.Run at 0x7fcefb35b0d0>,
 <temba_client.v2.types.Run at 0x7fcefb35e490>,
 <temba_client.v2.types.Run at 0x7fcefb361850>,
 <temba_client.v2.types.Run at 0x7fcefb366c90>,
 <temba_client.v2.types.Run at 0x7fcefb36d110>,
 <temba_client.v2.types.Run at 0x7fcefb371550>,
 <temba_client.v2.types.Run at 0x7fcefb374990>,
 <temba_client.v2.types.Run at 0x7fcefb378dd0>,
 <temba_client.v2.types.Run at 0x7fcefb37f250>,
 <temba_client.v2.types.Run at 0x7fcefb383690>,
 <temba_client.v2.types.Run at 0x7fcefb386ad0>,
 <temba_client.v2.types.Run at 0x7fcefb30e0d0>,
 <temba_client.v2.types.Run at 0x7fcefb311510>,
 <temba_client.v2.types.Run at 0x7fcefb3169d0>,
 <temba_client.v2.types.Run at 0x7fcefb319f10>,
 <temba_client.v2.types.Run at 0x7fcefb321390>,
 <temba_client.v2.types.Run at 0x7fcefb3247d0>,
 <temba_client.v2.types.Run at 0x7fcefb328c10>,
 <temba_client.v2.types.Run at 0x7fcefb32f110>,
 <temba_client.v2.types.Run at 0x7fcefb333650>,
 <temba_client.v2.types.Run at 0x7fcefb336a90>,
 <temba_client.v2.types.Run at 0x7fcefb33e110>,
 <temba_client.v2.types.Run at 0x7fcefb341650>,
 <temba_client.v2.types.Run at 0x7fcefb346a90>,
 <temba_client.v2.types.Run at 0x7fcefb2c9ed0>,
 <temba_client.v2.types.Run at 0x7fcefb2d1350>,
 <temba_client.v2.types.Run at 0x7fcefb2d4790>,
 <temba_client.v2.types.Run at 0x7fcefb2d78d0>,
 <temba_client.v2.types.Run at 0x7fcefb2db810>,
 <temba_client.v2.types.Run at 0x7fcefb2dfc50>,
 <temba_client.v2.types.Run at 0x7fcefb2e60d0>,
 <temba_client.v2.types.Run at 0x7fcefb2ea510>,
 <temba_client.v2.types.Run at 0x7fcefb2ee4d0>,
 <temba_client.v2.types.Run at 0x7fcefb2f1110>,
 <temba_client.v2.types.Run at 0x7fcefb2f5550>,
 <temba_client.v2.types.Run at 0x7fcefb2f9990>,
 <temba_client.v2.types.Run at 0x7fcefb2fcdd0>,
 <temba_client.v2.types.Run at 0x7fcefb304250>,
 <temba_client.v2.types.Run at 0x7fcefb307710>,
 <temba_client.v2.types.Run at 0x7fcefb28bc50>,
 <temba_client.v2.types.Run at 0x7fcefb2920d0>,
 <temba_client.v2.types.Run at 0x7fcefb296510>,
 <temba_client.v2.types.Run at 0x7fcefb29aad0>,
 <temba_client.v2.types.Run at 0x7fcefb2a1050>,
 <temba_client.v2.types.Run at 0x7fcefb2a5490>,
 <temba_client.v2.types.Run at 0x7fcefb2a98d0>,
 <temba_client.v2.types.Run at 0x7fcefb2acd10>,
 <temba_client.v2.types.Run at 0x7fcefb2b4190>,
 <temba_client.v2.types.Run at 0x7fcefb2b7290>,
 <temba_client.v2.types.Run at 0x7fcefb2bc150>,
 <temba_client.v2.types.Run at 0x7fcefb2bf510>,
 <temba_client.v2.types.Run at 0x7fcefb2c2950>,
 <temba_client.v2.types.Run at 0x7fcefb2c6d90>,
 <temba_client.v2.types.Run at 0x7fcefb24d290>,
 <temba_client.v2.types.Run at 0x7fcefb2512d0>,
 <temba_client.v2.types.Run at 0x7fcefb251dd0>,
 <temba_client.v2.types.Run at 0x7fcefb259250>,
 <temba_client.v2.types.Run at 0x7fcefb25c710>,
 <temba_client.v2.types.Run at 0x7fcefb260c50>,
 <temba_client.v2.types.Run at 0x7fcefb2670d0>,
 <temba_client.v2.types.Run at 0x7fcefb26b610>,
 <temba_client.v2.types.Run at 0x7fcefb26fb50>,
 <temba_client.v2.types.Run at 0x7fcefb272f90>,
 <temba_client.v2.types.Run at 0x7fcefb27a410>,
 <temba_client.v2.types.Run at 0x7fcefb27d310>,
 <temba_client.v2.types.Run at 0x7fcefb27de10>,
 <temba_client.v2.types.Run at 0x7fcefb285290>,
 <temba_client.v2.types.Run at 0x7fcefb2086d0>,
 <temba_client.v2.types.Run at 0x7fcefb20cb10>,
 <temba_client.v2.types.Run at 0x7fcefb210f50>,
 <temba_client.v2.types.Run at 0x7fcefb214ed0>,
 <temba_client.v2.types.Run at 0x7fcefb217b10>,
 <temba_client.v2.types.Run at 0x7fcefb21f090>,
 <temba_client.v2.types.Run at 0x7fcefb222550>,
 <temba_client.v2.types.Run at 0x7fcefb226a90>,
 <temba_client.v2.types.Run at 0x7fcefb22aed0>,
 <temba_client.v2.types.Run at 0x7fcefb232350>,
 <temba_client.v2.types.Run at 0x7fcefb235790>,
 <temba_client.v2.types.Run at 0x7fcefb238bd0>,
 <temba_client.v2.types.Run at 0x7fcefb240050>,
 <temba_client.v2.types.Run at 0x7fcefb243490>,
 <temba_client.v2.types.Run at 0x7fcefb2478d0>,
 <temba_client.v2.types.Run at 0x7fcefb1cbd10>,
 <temba_client.v2.types.Run at 0x7fcefb1d2190>,
 <temba_client.v2.types.Run at 0x7fcefb1d65d0>,
 <temba_client.v2.types.Run at 0x7fcefb1daa10>,
 <temba_client.v2.types.Run at 0x7fcefb1dde50>,
 <temba_client.v2.types.Run at 0x7fcefb1e54d0>,
 <temba_client.v2.types.Run at 0x7fcefb1e8810>,
 <temba_client.v2.types.Run at 0x7fcefb1ec750>,
 <temba_client.v2.types.Run at 0x7fcefb1f0b90>,
 <temba_client.v2.types.Run at 0x7fcefb1f3fd0>,
 <temba_client.v2.types.Run at 0x7fcefb1f7f10>,
 <temba_client.v2.types.Run at 0x7fcefb1fbad0>,
 <temba_client.v2.types.Run at 0x7fcefb1fef90>,
 <temba_client.v2.types.Run at 0x7fcefb206510>,
 <temba_client.v2.types.Run at 0x7fcefb18a950>,
 <temba_client.v2.types.Run at 0x7fcefb18df10>,
 <temba_client.v2.types.Run at 0x7fcefb195390>,
 <temba_client.v2.types.Run at 0x7fcefb198850>,
 <temba_client.v2.types.Run at 0x7fcefb19bd90>,
 <temba_client.v2.types.Run at 0x7fcefb1a3210>,
 <temba_client.v2.types.Run at 0x7fcefb1a76d0>,
 <temba_client.v2.types.Run at 0x7fcefb1abc10>,
 <temba_client.v2.types.Run at 0x7fcefb1b2190>,
 <temba_client.v2.types.Run at 0x7fcefb1b6650>,
 <temba_client.v2.types.Run at 0x7fcefb1b9c10>,
 <temba_client.v2.types.Run at 0x7fcefb1bdad0>,
 <temba_client.v2.types.Run at 0x7fcefb1c1490>,
 <temba_client.v2.types.Run at 0x7fcefb1c59d0>,
 <temba_client.v2.types.Run at 0x7fcefb148e10>,
 <temba_client.v2.types.Run at 0x7fcefb150290>,
 <temba_client.v2.types.Run at 0x7fcefb1536d0>,
 <temba_client.v2.types.Run at 0x7fcefb156b10>,
 <temba_client.v2.types.Run at 0x7fcefb15bf50>,
 <temba_client.v2.types.Run at 0x7fcefb1623d0>,
 <temba_client.v2.types.Run at 0x7fcefb166810>,
 <temba_client.v2.types.Run at 0x7fcefb169c50>,
 <temba_client.v2.types.Run at 0x7fcefb171150>,
 <temba_client.v2.types.Run at 0x7fcefb174690>,
 <temba_client.v2.types.Run at 0x7fcefb178ad0>,
 <temba_client.v2.types.Run at 0x7fcefb17bf10>,
 <temba_client.v2.types.Run at 0x7fcefb183390>,
 <temba_client.v2.types.Run at 0x7fcefb1867d0>,
 <temba_client.v2.types.Run at 0x7fcefb10bc90>,
 <temba_client.v2.types.Run at 0x7fcefb111210>,
 <temba_client.v2.types.Run at 0x7fcefb116650>,
 <temba_client.v2.types.Run at 0x7fcefb119a90>,
 <temba_client.v2.types.Run at 0x7fcefb11ded0>,
 <temba_client.v2.types.Run at 0x7fcefb124350>,
 <temba_client.v2.types.Run at 0x7fcefb128790>,
 <temba_client.v2.types.Run at 0x7fcefb12bc50>,
 <temba_client.v2.types.Run at 0x7fcefb1331d0>,
 <temba_client.v2.types.Run at 0x7fcefb136610>,
 <temba_client.v2.types.Run at 0x7fcefb13bad0>,
 <temba_client.v2.types.Run at 0x7fcefb141050>,
 <temba_client.v2.types.Run at 0x7fcefb141d90>,
 <temba_client.v2.types.Run at 0x7fcefb146750>,
 <temba_client.v2.types.Run at 0x7fcefb0c9c90>,
 <temba_client.v2.types.Run at 0x7fcefb0d1110>,
 <temba_client.v2.types.Run at 0x7fcefb0d4550>,
 <temba_client.v2.types.Run at 0x7fcefb0d8990>,
 <temba_client.v2.types.Run at 0x7fcefb0dbdd0>,
 <temba_client.v2.types.Run at 0x7fcefb0e3250>,
 <temba_client.v2.types.Run at 0x7fcefb0e7690>,
 <temba_client.v2.types.Run at 0x7fcefb0eaad0>,
 <temba_client.v2.types.Run at 0x7fcefb0ee990>,
 <temba_client.v2.types.Run at 0x7fcefb0f14d0>,
 <temba_client.v2.types.Run at 0x7fcefb0f6a10>,
 <temba_client.v2.types.Run at 0x7fcefb0f9b10>,
 <temba_client.v2.types.Run at 0x7fcefb0fca50>,
 <temba_client.v2.types.Run at 0x7fcefb101f90>,
 <temba_client.v2.types.Run at 0x7fcefb104f90>,
 <temba_client.v2.types.Run at 0x7fcefb107c50>,
 <temba_client.v2.types.Run at 0x7fcefb08f0d0>,
 <temba_client.v2.types.Run at 0x7fcefb093510>,
 <temba_client.v2.types.Run at 0x7fcefb097950>,
 <temba_client.v2.types.Run at 0x7fcefb09ae10>,
 <temba_client.v2.types.Run at 0x7fcefb0a2390>,
 <temba_client.v2.types.Run at 0x7fcefb0a5850>,
 <temba_client.v2.types.Run at 0x7fcefb0a9d90>,
 <temba_client.v2.types.Run at 0x7fcefb0b1210>,
 <temba_client.v2.types.Run at 0x7fcefb0b4650>,
 <temba_client.v2.types.Run at 0x7fcefb0b7a90>,
 <temba_client.v2.types.Run at 0x7fcefb0bced0>,
 <temba_client.v2.types.Run at 0x7fcefb0c2350>,
 <temba_client.v2.types.Run at 0x7fcefb0c6790>,
 <temba_client.v2.types.Run at 0x7fcefb04abd0>,
 <temba_client.v2.types.Run at 0x7fcefb052050>,
 <temba_client.v2.types.Run at 0x7fcefb055490>,
 <temba_client.v2.types.Run at 0x7fcefb0598d0>,
 <temba_client.v2.types.Run at 0x7fcefb05cd10>,
 <temba_client.v2.types.Run at 0x7fcefb064190>,
 <temba_client.v2.types.Run at 0x7fcefb067550>,
 <temba_client.v2.types.Run at 0x7fcefb06c910>,
 <temba_client.v2.types.Run at 0x7fcefb06fd50>,
 <temba_client.v2.types.Run at 0x7fcefb077090>,
 <temba_client.v2.types.Run at 0x7fcefb07a3d0>,
 <temba_client.v2.types.Run at 0x7fcefb07d810>,
 <temba_client.v2.types.Run at 0x7fcefb0819d0>,
 <temba_client.v2.types.Run at 0x7fcefb085a10>,
 <temba_client.v2.types.Run at 0x7fcefb009ed0>,
 <temba_client.v2.types.Run at 0x7fcefb010450>,
 <temba_client.v2.types.Run at 0x7fcefb014890>,
 <temba_client.v2.types.Run at 0x7fcefb017cd0>,
 <temba_client.v2.types.Run at 0x7fcefb01f150>,
 <temba_client.v2.types.Run at 0x7fcefb01ffd0>,
 <temba_client.v2.types.Run at 0x7fcefb022510>,
 <temba_client.v2.types.Run at 0x7fcefb027050>,
 <temba_client.v2.types.Run at 0x7fcefb02a490>,
 <temba_client.v2.types.Run at 0x7fcefb02d550>,
 <temba_client.v2.types.Run at 0x7fcefb032390>,
 <temba_client.v2.types.Run at 0x7fcefb0357d0>,
 <temba_client.v2.types.Run at 0x7fcefb038c10>,
 <temba_client.v2.types.Run at 0x7fcefb040090>,
 <temba_client.v2.types.Run at 0x7fcefb0444d0>,
 <temba_client.v2.types.Run at 0x7fcefb047910>,
 <temba_client.v2.types.Run at 0x7fcefafcb6d0>,
 <temba_client.v2.types.Run at 0x7fcefafcbfd0>,
 <temba_client.v2.types.Run at 0x7fcefafd34d0>,
 <temba_client.v2.types.Run at 0x7fcefafd6510>,
 <temba_client.v2.types.Run at 0x7fcefafda050>,
 <temba_client.v2.types.Run at 0x7fcefafdd490>,
 <temba_client.v2.types.Run at 0x7fcefafe28d0>,
 <temba_client.v2.types.Run at 0x7fcefafe5d90>,
 <temba_client.v2.types.Run at 0x7fcefafed310>,
 <temba_client.v2.types.Run at 0x7fcefaff0750>,
 <temba_client.v2.types.Run at 0x7fcefaff3b90>,
 <temba_client.v2.types.Run at 0x7fcefaff8fd0>,
 <temba_client.v2.types.Run at 0x7fcefafff450>,
 <temba_client.v2.types.Run at 0x7fcefb002890>,
 <temba_client.v2.types.Run at 0x7fcefb006cd0>,
 <temba_client.v2.types.Run at 0x7fcefaf8d150>,
 <temba_client.v2.types.Run at 0x7fcefaf91590>,
 <temba_client.v2.types.Run at 0x7fcefaf959d0>,
 <temba_client.v2.types.Run at 0x7fcefaf98e10>,
 <temba_client.v2.types.Run at 0x7fcefafa0290>,
 <temba_client.v2.types.Run at 0x7fcefafa36d0>,
 <temba_client.v2.types.Run at 0x7fcefafa7a90>,
 <temba_client.v2.types.Run at 0x7fcefafabe50>,
 <temba_client.v2.types.Run at 0x7fcefafb32d0>,
 <temba_client.v2.types.Run at 0x7fcefafb6690>,
 <temba_client.v2.types.Run at 0x7fcefafbab50>]

In [60]: runs = _

In [61]: run = runs[0]

In [62]: run
Out[62]: <temba_client.v2.types.Run at 0x7fcf080c4c10>

In [63]: run.values()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-63-7fdfce13bb22> in <module>()
----> 1 run.values()

TypeError: 'dict' object is not callable

In [64]: run.values
Out[64]: 
{u'amar_o': <temba_client.v2.types.Value at 0x7fcefb43c590>,
 u'beg_o': <temba_client.v2.types.Value at 0x7fcefb43c4d0>,
 u'confirm': <temba_client.v2.types.Value at 0x7fcf080c2c50>,
 u'dcur_o': <temba_client.v2.types.Value at 0x7fcefb43c5d0>,
 u'dead_o': <temba_client.v2.types.Value at 0x7fcefb43c490>,
 u'defu_o': <temba_client.v2.types.Value at 0x7fcf080c2250>,
 u'dmed_o': <temba_client.v2.types.Value at 0x7fcefa7ba890>,
 u'msg_routing': <temba_client.v2.types.Value at 0x7fcefa7ba910>,
 u'role': <temba_client.v2.types.Value at 0x7fcefb43c450>,
 u'tin_o': <temba_client.v2.types.Value at 0x7fcefb43c350>,
 u'tout_o': <temba_client.v2.types.Value at 0x7fcf080c29d0>,
 u'type': <temba_client.v2.types.Value at 0x7fcefa7ba810>,
 u'weeknum': <temba_client.v2.types.Value at 0x7fcefb43c110>}

In [65]: run.contact
Out[65]: <temba_client.v2.types.ObjectRef at 0x7fcf080c4190>

In [66]: run.contact.uuid
Out[66]: u'e39d3459-2e1e-40c3-b9c4-1c5df51d937f'

In [67]: 

In [67]: run
Out[67]: <temba_client.v2.types.Run at 0x7fcf080c4c10>

In [68]: run.path
Out[68]: 
[<temba_client.v2.types.Step at 0x7fcefa7baa10>,
 <temba_client.v2.types.Step at 0x7fcefa7baa90>,
 <temba_client.v2.types.Step at 0x7fcefa7bab10>,
 <temba_client.v2.types.Step at 0x7fcefa7bab90>,
 <temba_client.v2.types.Step at 0x7fcefa7bac10>,
 <temba_client.v2.types.Step at 0x7fcefa7bac90>,
 <temba_client.v2.types.Step at 0x7fcefa7bad10>,
 <temba_client.v2.types.Step at 0x7fcefa7bad90>,
 <temba_client.v2.types.Step at 0x7fcefa7bae10>,
 <temba_client.v2.types.Step at 0x7fcefa7bae90>,
 <temba_client.v2.types.Step at 0x7fcefa7baf10>,
 <temba_client.v2.types.Step at 0x7fcefa7baf90>,
 <temba_client.v2.types.Step at 0x7fcefa711050>,
 <temba_client.v2.types.Step at 0x7fcefa7110d0>,
 <temba_client.v2.types.Step at 0x7fcefa711150>,
 <temba_client.v2.types.Step at 0x7fcefa7111d0>,
 <temba_client.v2.types.Step at 0x7fcefa711250>,
 <temba_client.v2.types.Step at 0x7fcefa7112d0>,
 <temba_client.v2.types.Step at 0x7fcefa711350>,
 <temba_client.v2.types.Step at 0x7fcefa7113d0>,
 <temba_client.v2.types.Step at 0x7fcefa711450>,
 <temba_client.v2.types.Step at 0x7fcefa7114d0>,
 <temba_client.v2.types.Step at 0x7fcefa711550>,
 <temba_client.v2.types.Step at 0x7fcefa7115d0>]

In [69]: run.responded
Out[69]: True

In [70]: run.Value
Out[70]: temba_client.v2.types.Value

In [71]: run.Value.category
Out[71]: <temba_client.serialization.SimpleField at 0x7fcf08191ad0>

In [72]: run[]
  File "<ipython-input-72-5d42cca09709>", line 1
    run[]
        ^
SyntaxError: invalid syntax


In [73]: run['']
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-73-40a63f52b260> in <module>()
----> 1 run['']

TypeError: 'Run' object has no attribute '__getitem__'

In [74]: run.values
Out[74]: 
{u'amar_o': <temba_client.v2.types.Value at 0x7fcefb43c590>,
 u'beg_o': <temba_client.v2.types.Value at 0x7fcefb43c4d0>,
 u'confirm': <temba_client.v2.types.Value at 0x7fcf080c2c50>,
 u'dcur_o': <temba_client.v2.types.Value at 0x7fcefb43c5d0>,
 u'dead_o': <temba_client.v2.types.Value at 0x7fcefb43c490>,
 u'defu_o': <temba_client.v2.types.Value at 0x7fcf080c2250>,
 u'dmed_o': <temba_client.v2.types.Value at 0x7fcefa7ba890>,
 u'msg_routing': <temba_client.v2.types.Value at 0x7fcefa7ba910>,
 u'role': <temba_client.v2.types.Value at 0x7fcefb43c450>,
 u'tin_o': <temba_client.v2.types.Value at 0x7fcefb43c350>,
 u'tout_o': <temba_client.v2.types.Value at 0x7fcf080c29d0>,
 u'type': <temba_client.v2.types.Value at 0x7fcefa7ba810>,
 u'weeknum': <temba_client.v2.types.Value at 0x7fcefb43c110>}

In [75]: run.values['amar_o']
Out[75]: <temba_client.v2.types.Value at 0x7fcefb43c590>

In [76]: amar = run.values['amar_o']

In [77]: amar.value
Out[77]: 0.0

In [78]: amar.category
Out[78]: u'0 - 9999'

In [79]: amar.node
Out[79]: u'e7d96279-b9fb-4ed6-8d0f-85fca4ed272d'

In [80]: amar.deserialize
Out[80]: <bound method ABCMeta.deserialize of <class 'temba_client.v2.types.Value'>>

In [81]: amar.deserialize?
Signature: amar.deserialize(item)
Docstring: <no docstring>
File:      ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/serialization.py
Type:      instancemethod

In [82]: amar.time
Out[82]: datetime.datetime(2017, 4, 10, 13, 7, 18, 683588, tzinfo=<UTC>)

In [83]: run.exit_type
Out[83]: u'completed'

In [84]: run.contact
Out[84]: <temba_client.v2.types.ObjectRef at 0x7fcf080c4190>

In [85]: client.get_contacts()
Out[85]: <temba_client.clients.CursorQuery at 0x7fcefa7baad0>

In [86]: client.get_contacts(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True).next()
Out[86]: 
[<temba_client.v2.types.Contact at 0x7fcefa713310>,
 <temba_client.v2.types.Contact at 0x7fcf080c4a10>,
 <temba_client.v2.types.Contact at 0x7fcefa714110>,
 <temba_client.v2.types.Contact at 0x7fcefa714e90>,
 <temba_client.v2.types.Contact at 0x7fcefb32b890>,
 <temba_client.v2.types.Contact at 0x7fcefb3339d0>,
 <temba_client.v2.types.Contact at 0x7fcefb333e50>,
 <temba_client.v2.types.Contact at 0x7fcefb3333d0>,
 <temba_client.v2.types.Contact at 0x7fcefb333050>,
 <temba_client.v2.types.Contact at 0x7fcefb32f410>,
 <temba_client.v2.types.Contact at 0x7fcefb32f890>,
 <temba_client.v2.types.Contact at 0x7fcefb32fc10>,
 <temba_client.v2.types.Contact at 0x7fcefb32fe50>,
 <temba_client.v2.types.Contact at 0x7fcefb336c90>,
 <temba_client.v2.types.Contact at 0x7fcefb336f90>,
 <temba_client.v2.types.Contact at 0x7fcefb336790>,
 <temba_client.v2.types.Contact at 0x7fcefb336350>,
 <temba_client.v2.types.Contact at 0x7fcefb33a350>,
 <temba_client.v2.types.Contact at 0x7fcefb33a750>,
 <temba_client.v2.types.Contact at 0x7fcefb33ad50>,
 <temba_client.v2.types.Contact at 0x7fcefb33a910>,
 <temba_client.v2.types.Contact at 0x7fcefb341950>,
 <temba_client.v2.types.Contact at 0x7fcefb341dd0>,
 <temba_client.v2.types.Contact at 0x7fcefb3414d0>,
 <temba_client.v2.types.Contact at 0x7fcefb3410d0>,
 <temba_client.v2.types.Contact at 0x7fcefb33e490>,
 <temba_client.v2.types.Contact at 0x7fcefb33e910>,
 <temba_client.v2.types.Contact at 0x7fcefb33ed10>,
 <temba_client.v2.types.Contact at 0x7fcefb346090>,
 <temba_client.v2.types.Contact at 0x7fcefb346c10>,
 <temba_client.v2.types.Contact at 0x7fcefb346f90>,
 <temba_client.v2.types.Contact at 0x7fcefb346710>,
 <temba_client.v2.types.Contact at 0x7fcefb2c90d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2c95d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2c9d50>,
 <temba_client.v2.types.Contact at 0x7fcefb2c9950>,
 <temba_client.v2.types.Contact at 0x7fcefb2cc290>,
 <temba_client.v2.types.Contact at 0x7fcefb2cc690>,
 <temba_client.v2.types.Contact at 0x7fcefb2ccb10>,
 <temba_client.v2.types.Contact at 0x7fcefb2ccbd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d4b90>,
 <temba_client.v2.types.Contact at 0x7fcefb2d4e10>,
 <temba_client.v2.types.Contact at 0x7fcefb2d4610>,
 <temba_client.v2.types.Contact at 0x7fcefb2d4210>,
 <temba_client.v2.types.Contact at 0x7fcefb2d15d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d19d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d1dd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d11d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d71d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d7ad0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d7ed0>,
 <temba_client.v2.types.Contact at 0x7fcefb2d76d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2dba10>,
 <temba_client.v2.types.Contact at 0x7fcefb2dbe90>,
 <temba_client.v2.types.Contact at 0x7fcefb2db590>,
 <temba_client.v2.types.Contact at 0x7fcefb2db190>,
 <temba_client.v2.types.Contact at 0x7fcefb2df250>,
 <temba_client.v2.types.Contact at 0x7fcefb2dfed0>,
 <temba_client.v2.types.Contact at 0x7fcefb2df950>,
 <temba_client.v2.types.Contact at 0x7fcefb2df5d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2e3390>,
 <temba_client.v2.types.Contact at 0x7fcefb2e3810>,
 <temba_client.v2.types.Contact at 0x7fcefb2e3d10>,
 <temba_client.v2.types.Contact at 0x7fcefb2e38d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2ea910>,
 <temba_client.v2.types.Contact at 0x7fcefb2eae10>,
 <temba_client.v2.types.Contact at 0x7fcefb2ea310>,
 <temba_client.v2.types.Contact at 0x7fcefb2ea090>,
 <temba_client.v2.types.Contact at 0x7fcefb2e6550>,
 <temba_client.v2.types.Contact at 0x7fcefb2e69d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2e6fd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2ee150>,
 <temba_client.v2.types.Contact at 0x7fcefb2ee8d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2eefd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2eeb50>,
 <temba_client.v2.types.Contact at 0x7fcefb2f5750>,
 <temba_client.v2.types.Contact at 0x7fcefb2f5b50>,
 <temba_client.v2.types.Contact at 0x7fcefb2f5f50>,
 <temba_client.v2.types.Contact at 0x7fcefb2f51d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2f1410>,
 <temba_client.v2.types.Contact at 0x7fcefb2f1790>,
 <temba_client.v2.types.Contact at 0x7fcefb2f1b10>,
 <temba_client.v2.types.Contact at 0x7fcefb2f10d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2f9110>,
 <temba_client.v2.types.Contact at 0x7fcefb2f9d10>,
 <temba_client.v2.types.Contact at 0x7fcefb2f9810>,
 <temba_client.v2.types.Contact at 0x7fcefb2f9390>,
 <temba_client.v2.types.Contact at 0x7fcefb2fc250>,
 <temba_client.v2.types.Contact at 0x7fcefb2fce50>,
 <temba_client.v2.types.Contact at 0x7fcefb2fcbd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2fc850>,
 <temba_client.v2.types.Contact at 0x7fcefb301190>,
 <temba_client.v2.types.Contact at 0x7fcefb301610>,
 <temba_client.v2.types.Contact at 0x7fcefb301f90>,
 <temba_client.v2.types.Contact at 0x7fcefb301c10>,
 <temba_client.v2.types.Contact at 0x7fcefb307a10>,
 <temba_client.v2.types.Contact at 0x7fcefb307c10>,
 <temba_client.v2.types.Contact at 0x7fcefb3076d0>,
 <temba_client.v2.types.Contact at 0x7fcefb307290>,
 <temba_client.v2.types.Contact at 0x7fcefb3044d0>,
 <temba_client.v2.types.Contact at 0x7fcefb3048d0>,
 <temba_client.v2.types.Contact at 0x7fcefb304cd0>,
 <temba_client.v2.types.Contact at 0x7fcefb304fd0>,
 <temba_client.v2.types.Contact at 0x7fcefb28b2d0>,
 <temba_client.v2.types.Contact at 0x7fcefb28bf50>,
 <temba_client.v2.types.Contact at 0x7fcefb28b9d0>,
 <temba_client.v2.types.Contact at 0x7fcefb28b5d0>,
 <temba_client.v2.types.Contact at 0x7fcefb28f310>,
 <temba_client.v2.types.Contact at 0x7fcefb28f810>,
 <temba_client.v2.types.Contact at 0x7fcefb28fe10>,
 <temba_client.v2.types.Contact at 0x7fcefb28fb90>,
 <temba_client.v2.types.Contact at 0x7fcefb296690>,
 <temba_client.v2.types.Contact at 0x7fcefb296a90>,
 <temba_client.v2.types.Contact at 0x7fcefb296d10>,
 <temba_client.v2.types.Contact at 0x7fcefb296410>,
 <temba_client.v2.types.Contact at 0x7fcefb2921d0>,
 <temba_client.v2.types.Contact at 0x7fcefb292650>,
 <temba_client.v2.types.Contact at 0x7fcefb292ad0>,
 <temba_client.v2.types.Contact at 0x7fcefb292ed0>,
 <temba_client.v2.types.Contact at 0x7fcefb29a250>,
 <temba_client.v2.types.Contact at 0x7fcefb29ae50>,
 <temba_client.v2.types.Contact at 0x7fcefb29aa90>,
 <temba_client.v2.types.Contact at 0x7fcefb29a650>,
 <temba_client.v2.types.Contact at 0x7fcefb29e110>,
 <temba_client.v2.types.Contact at 0x7fcefb29e590>,
 <temba_client.v2.types.Contact at 0x7fcefb29e810>,
 <temba_client.v2.types.Contact at 0x7fcefb29ed10>,
 <temba_client.v2.types.Contact at 0x7fcefb29e8d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2a5810>,
 <temba_client.v2.types.Contact at 0x7fcefb2a5b90>,
 <temba_client.v2.types.Contact at 0x7fcefb2a5450>,
 <temba_client.v2.types.Contact at 0x7fcefb2a5090>,
 <temba_client.v2.types.Contact at 0x7fcefb2a14d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2a18d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2a1ed0>,
 <temba_client.v2.types.Contact at 0x7fcefb2a9a50>,
 <temba_client.v2.types.Contact at 0x7fcefb2a9e50>,
 <temba_client.v2.types.Contact at 0x7fcefb2a96d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2a9250>,
 <temba_client.v2.types.Contact at 0x7fcefb2ac310>,
 <temba_client.v2.types.Contact at 0x7fcefb2acf90>,
 <temba_client.v2.types.Contact at 0x7fcefb2ac990>,
 <temba_client.v2.types.Contact at 0x7fcefb2ac550>,
 <temba_client.v2.types.Contact at 0x7fcefb2b03d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2b07d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2b0dd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2b4210>,
 <temba_client.v2.types.Contact at 0x7fcefb2b4510>,
 <temba_client.v2.types.Contact at 0x7fcefb2b4990>,
 <temba_client.v2.types.Contact at 0x7fcefb2b4c90>,
 <temba_client.v2.types.Contact at 0x7fcefb2b4ed0>,
 <temba_client.v2.types.Contact at 0x7fcefb2b7690>,
 <temba_client.v2.types.Contact at 0x7fcefb2b7210>,
 <temba_client.v2.types.Contact at 0x7fcefb2b7e10>,
 <temba_client.v2.types.Contact at 0x7fcefb2b79d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2bfa10>,
 <temba_client.v2.types.Contact at 0x7fcefb2bfd90>,
 <temba_client.v2.types.Contact at 0x7fcefb2bf290>,
 <temba_client.v2.types.Contact at 0x7fcefb2bc350>,
 <temba_client.v2.types.Contact at 0x7fcefb2bc7d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2bccd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2bcd10>,
 <temba_client.v2.types.Contact at 0x7fcefb2c2c50>,
 <temba_client.v2.types.Contact at 0x7fcefb2c28d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2c2450>,
 <temba_client.v2.types.Contact at 0x7fcefb2c6210>,
 <temba_client.v2.types.Contact at 0x7fcefb2c6e90>,
 <temba_client.v2.types.Contact at 0x7fcefb2c6a90>,
 <temba_client.v2.types.Contact at 0x7fcefb2c65d0>,
 <temba_client.v2.types.Contact at 0x7fcefb24a4d0>,
 <temba_client.v2.types.Contact at 0x7fcefb24a950>,
 <temba_client.v2.types.Contact at 0x7fcefb24ac50>,
 <temba_client.v2.types.Contact at 0x7fcefb24d610>,
 <temba_client.v2.types.Contact at 0x7fcefb24da90>,
 <temba_client.v2.types.Contact at 0x7fcefb24df10>,
 <temba_client.v2.types.Contact at 0x7fcefb2513d0>,
 <temba_client.v2.types.Contact at 0x7fcefb251090>,
 <temba_client.v2.types.Contact at 0x7fcefb251c50>,
 <temba_client.v2.types.Contact at 0x7fcefb2517d0>,
 <temba_client.v2.types.Contact at 0x7fcefb255310>,
 <temba_client.v2.types.Contact at 0x7fcefb255710>,
 <temba_client.v2.types.Contact at 0x7fcefb255e10>,
 <temba_client.v2.types.Contact at 0x7fcefb25c790>,
 <temba_client.v2.types.Contact at 0x7fcefb25cb90>,
 <temba_client.v2.types.Contact at 0x7fcefb25cf90>,
 <temba_client.v2.types.Contact at 0x7fcefb25c390>,
 <temba_client.v2.types.Contact at 0x7fcefb2593d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2597d0>,
 <temba_client.v2.types.Contact at 0x7fcefb259bd0>,
 <temba_client.v2.types.Contact at 0x7fcefb2590d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2601d0>,
 <temba_client.v2.types.Contact at 0x7fcefb260dd0>,
 <temba_client.v2.types.Contact at 0x7fcefb260950>,
 <temba_client.v2.types.Contact at 0x7fcefb260510>,
 <temba_client.v2.types.Contact at 0x7fcefb264390>,
 <temba_client.v2.types.Contact at 0x7fcefb264790>,
 <temba_client.v2.types.Contact at 0x7fcefb264d10>,
 <temba_client.v2.types.Contact at 0x7fcefb2648d0>,
 <temba_client.v2.types.Contact at 0x7fcefb26ba10>,
 <temba_client.v2.types.Contact at 0x7fcefb26be10>,
 <temba_client.v2.types.Contact at 0x7fcefb26b410>,
 <temba_client.v2.types.Contact at 0x7fcefb267150>,
 <temba_client.v2.types.Contact at 0x7fcefb267550>,
 <temba_client.v2.types.Contact at 0x7fcefb267950>,
 <temba_client.v2.types.Contact at 0x7fcefb267d50>,
 <temba_client.v2.types.Contact at 0x7fcefb26f050>,
 <temba_client.v2.types.Contact at 0x7fcefb26fdd0>,
 <temba_client.v2.types.Contact at 0x7fcefb26f9d0>,
 <temba_client.v2.types.Contact at 0x7fcefb26f5d0>,
 <temba_client.v2.types.Contact at 0x7fcefb272390>,
 <temba_client.v2.types.Contact at 0x7fcefb272f50>,
 <temba_client.v2.types.Contact at 0x7fcefb272b10>,
 <temba_client.v2.types.Contact at 0x7fcefb27a510>,
 <temba_client.v2.types.Contact at 0x7fcefb27a910>,
 <temba_client.v2.types.Contact at 0x7fcefb27ad90>,
 <temba_client.v2.types.Contact at 0x7fcefb27a210>,
 <temba_client.v2.types.Contact at 0x7fcefb2773d0>,
 <temba_client.v2.types.Contact at 0x7fcefb277850>,
 <temba_client.v2.types.Contact at 0x7fcefb277f50>,
 <temba_client.v2.types.Contact at 0x7fcefb27d410>,
 <temba_client.v2.types.Contact at 0x7fcefb27d0d0>,
 <temba_client.v2.types.Contact at 0x7fcefb27db90>,
 <temba_client.v2.types.Contact at 0x7fcefb27d6d0>,
 <temba_client.v2.types.Contact at 0x7fcefb2813d0>,
 <temba_client.v2.types.Contact at 0x7fcefb281850>,
 <temba_client.v2.types.Contact at 0x7fcefb281dd0>,
 <temba_client.v2.types.Contact at 0x7fcefb208850>,
 <temba_client.v2.types.Contact at 0x7fcefb208cd0>,
 <temba_client.v2.types.Contact at 0x7fcefb208650>,
 <temba_client.v2.types.Contact at 0x7fcefb208250>,
 <temba_client.v2.types.Contact at 0x7fcefb285510>,
 <temba_client.v2.types.Contact at 0x7fcefb285910>,
 <temba_client.v2.types.Contact at 0x7fcefb285d90>,
 <temba_client.v2.types.Contact at 0x7fcefb285ed0>,
 <temba_client.v2.types.Contact at 0x7fcefb20cc90>,
 <temba_client.v2.types.Contact at 0x7fcefb20ca10>,
 <temba_client.v2.types.Contact at 0x7fcefb20c590>,
 <temba_client.v2.types.Contact at 0x7fcefb210250>,
 <temba_client.v2.types.Contact at 0x7fcefb2106d0>,
 <temba_client.v2.types.Contact at 0x7fcefb210c50>,
 <temba_client.v2.types.Contact at 0x7fcefb210810>,
 <temba_client.v2.types.Contact at 0x7fcefb214410>,
 <temba_client.v2.types.Contact at 0x7fcefb214890>,
 <temba_client.v2.types.Contact at 0x7fcefb214e90>,
 <temba_client.v2.types.Contact at 0x7fcefb217190>,
 <temba_client.v2.types.Contact at 0x7fcefb217e10>,
 <temba_client.v2.types.Contact at 0x7fcefb217790>,
 <temba_client.v2.types.Contact at 0x7fcefb217350>,
 <temba_client.v2.types.Contact at 0x7fcefb21b3d0>,
 <temba_client.v2.types.Contact at 0x7fcefb21b850>]

In [87]: contacts = _

In [88]: contact = contacts[0]

In [89]: contact.fields
Out[89]: 
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In [90]: contact.fields
Out[90]: 
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In [91]: contact.uuid
Out[91]: u'c80583bd-5aff-4bc8-b309-0e8ac9d12479'

In [92]: contact.urns
Out[92]: [u'tel:+2347032791311']

In [93]: contact.name
Out[93]: u'Hassana Tijjani.'

In [94]: contact.groups
Out[94]: 
[<temba_client.v2.types.ObjectRef at 0x7fcefa713cd0>,
 <temba_client.v2.types.ObjectRef at 0x7fcf080c42d0>,
 <temba_client.v2.types.ObjectRef at 0x7fcf080c4f50>,
 <temba_client.v2.types.ObjectRef at 0x7fcf080c4f10>,
 <temba_client.v2.types.ObjectRef at 0x7fcf080c4290>]

In [95]: contact.groups[0].name
Out[95]: u'Imam Supervision 3'

In [96]: [x.name for x in contact.groups]
Out[96]: 
[u'Imam Supervision 3',
 u'Imam Supervision 2',
 u'Imam Supervision',
 u'Nut Personnel',
 u'No_Email']

In [97]: contact.fields
Out[97]: 
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In [98]: contact['siteid']
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-98-9f055b55025f> in <module>()
----> 1 contact['siteid']

TypeError: 'Contact' object has no attribute '__getitem__'

In [99]: contact.modified_on
Out[99]: datetime.datetime(2017, 4, 10, 13, 29, 34, 733325, tzinfo=<UTC>)

In [100]: contact.blocked
Out[100]: False

In [101]: contact.created_on
Out[101]: datetime.datetime(2016, 10, 18, 10, 14, 22, 965210, tzinfo=<UTC>)

In [102]: contact.stopped
Out[102]: False

In [103]: [x.modified_on for x in contacts]
Out[103]: 
[datetime.datetime(2017, 4, 10, 13, 29, 34, 733325, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 24, 39, 22642, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 23, 28, 157967, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 12, 13, 20334, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 8, 11, 246011, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 5, 31, 313794, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 5, 26, 130577, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 13, 2, 41, 403071, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 59, 24, 52737, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 54, 7, 389953, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 53, 26, 967967, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 45, 10, 956355, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 39, 0, 990799, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 34, 42, 879732, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 32, 29, 73858, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 30, 19, 619353, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 24, 43, 632993, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 19, 24, 798648, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 18, 31, 406092, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 9, 48, 226495, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 8, 39, 595412, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 7, 38, 35129, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 3, 51, 107139, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 12, 1, 2, 41705, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 58, 24, 493700, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 55, 56, 897560, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 55, 33, 516567, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 55, 31, 471392, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 46, 41, 749246, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 39, 45, 913606, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 34, 47, 262971, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 24, 3, 127398, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 23, 11, 245200, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 19, 17, 672190, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 12, 47, 195803, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 10, 19, 327148, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 9, 12, 424374, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 8, 41, 990604, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 8, 34, 969558, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 8, 20, 523525, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 5, 29, 45381, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 4, 59, 209844, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 3, 5, 560585, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 11, 3, 3, 778499, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 55, 57, 15334, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 50, 52, 686095, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 49, 51, 933727, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 49, 45, 778843, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 45, 50, 755188, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 43, 43, 606150, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 42, 8, 590985, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 40, 30, 985430, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 39, 11, 520445, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 35, 37, 297469, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 33, 12, 760354, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 33, 4, 998651, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 32, 11, 641670, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 30, 59, 735248, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 30, 50, 73395, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 30, 14, 46197, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 27, 43, 322779, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 21, 24, 883254, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 20, 57, 627703, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 18, 26, 544643, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 18, 17, 584914, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 11, 39, 789778, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 9, 6, 397865, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 9, 4, 888180, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 4, 32, 760361, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 3, 5, 315849, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 10, 0, 12, 732777, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 57, 29, 490055, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 54, 41, 7634, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 52, 9, 127164, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 51, 18, 798206, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 48, 5, 615075, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 45, 11, 782595, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 45, 9, 114235, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 43, 9, 14614, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 42, 21, 468033, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 40, 10, 346754, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 38, 59, 106838, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 38, 37, 250580, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 38, 2, 765500, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 35, 40, 172423, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 25, 34, 332909, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 25, 18, 673591, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 20, 48, 24292, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 20, 47, 60903, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 17, 47, 133589, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 8, 22, 37633, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 7, 32, 986512, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 4, 21, 944437, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 2, 50, 754904, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 9, 1, 38, 621827, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 59, 48, 110759, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 57, 27, 858135, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 55, 50, 825616, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 53, 51, 581696, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 53, 34, 667468, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 47, 7, 553334, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 47, 2, 71216, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 46, 14, 654694, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 45, 47, 230964, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 44, 50, 662894, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 43, 35, 350784, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 43, 12, 439249, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 43, 2, 829054, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 35, 4, 171866, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 32, 14, 134969, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 29, 3, 97238, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 28, 54, 573151, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 25, 33, 276962, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 24, 57, 250852, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 23, 44, 345818, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 20, 54, 350480, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 16, 15, 36531, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 15, 47, 285109, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 14, 57, 458684, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 13, 26, 767955, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 8, 10, 765436, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 8, 8, 676282, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 8, 0, 35, 216908, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 56, 48, 504629, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 55, 23, 715347, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 47, 31, 692825, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 46, 45, 144148, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 46, 32, 705010, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 45, 22, 652171, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 43, 53, 413971, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 43, 38, 153906, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 42, 40, 415121, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 42, 6, 529720, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 39, 6, 627174, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 37, 18, 875238, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 37, 5, 993362, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 34, 9, 203517, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 33, 23, 872978, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 29, 11, 941046, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 26, 8, 462349, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 25, 16, 319443, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 24, 43, 177741, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 23, 58, 776444, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 21, 43, 134846, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 21, 13, 234952, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 21, 4, 528832, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 19, 58, 5956, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 18, 26, 126834, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 18, 3, 757301, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 17, 59, 870291, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 17, 27, 65542, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 17, 20, 758320, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 16, 51, 6589, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 14, 15, 54254, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 14, 2, 899179, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 13, 37, 265466, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 12, 58, 321380, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 12, 22, 969622, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 12, 8, 621526, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 11, 17, 221421, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 57, 363217, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 56, 966955, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 56, 578649, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 56, 186560, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 55, 734180, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 55, 314767, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 54, 893626, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 54, 438539, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 53, 974102, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 53, 558753, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 53, 133586, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 52, 706024, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 52, 259585, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 51, 833960, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 51, 22952, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 50, 591972, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 50, 180044, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 49, 734170, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 49, 292573, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 48, 845548, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 48, 24259, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 47, 623641, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 47, 252853, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 46, 853165, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 46, 452201, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 46, 37672, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 45, 263415, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 44, 832950, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 44, 440459, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 44, 79124, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 43, 719060, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 43, 377551, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 43, 41515, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 42, 653992, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 42, 307254, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 41, 960441, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 41, 624434, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 41, 279888, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 40, 890721, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 40, 521337, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 40, 156620, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 39, 794800, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 39, 57439, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 38, 691737, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 38, 322579, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 37, 944877, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 37, 548028, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 37, 152318, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 36, 765609, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 36, 376909, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 35, 242258, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 34, 823014, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 34, 362452, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 33, 597438, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 33, 187567, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 32, 791591, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 32, 404515, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 31, 978100, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 31, 596969, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 31, 205290, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 30, 768318, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 30, 336367, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 29, 906100, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 29, 532664, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 28, 298495, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 27, 911607, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 27, 69840, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 26, 242759, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 25, 861918, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 25, 466123, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 25, 84413, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 24, 720629, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 24, 323318, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 23, 930925, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 23, 563498, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 23, 196903, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 22, 815309, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 22, 394346, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 22, 10046, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 21, 596527, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 20, 936375, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 20, 406766, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 19, 983933, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 19, 604938, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 19, 202415, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 18, 453483, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 17, 336536, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 16, 981366, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 16, 611103, tzinfo=<UTC>),
 datetime.datetime(2017, 4, 10, 7, 10, 16, 151054, tzinfo=<UTC>)]

In [104]: contact.created_on
Out[104]: datetime.datetime(2016, 10, 18, 10, 14, 22, 965210, tzinfo=<UTC>)

In [105]: contact.fields
Out[105]: 
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In [106]: from uuid import UUID

In [107]: contact.uuid
Out[107]: u'c80583bd-5aff-4bc8-b309-0e8ac9d12479'

In [108]: UUID(contact.uuid)
Out[108]: UUID('c80583bd-5aff-4bc8-b309-0e8ac9d12479')

In [109]: len(contact.uuid)
Out[109]: 36

In [110]: client.get_contacts(group='Nut Personnel')
Out[110]: <temba_client.clients.CursorQuery at 0x7fcefb346d10>

In [111]: client.get_contacts(group='Nut Personnel').count
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-111-f5131037d408> in <module>()
----> 1 client.get_contacts(group='Nut Personnel').count

AttributeError: 'CursorQuery' object has no attribute 'count'

In [112]: z = client.get_contacts(group='Nut Personnel')

In [113]: z.params
Out[113]: {'group': 'Nut Personnel'}

In [114]: z.url
Out[114]: u'https://rapidpro.io/api/v2/contacts.json'

In [115]: run
Out[115]: <temba_client.v2.types.Run at 0x7fcf080c4c10>

In [116]: run.fields
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-116-8cc90d7ac291> in <module>()
----> 1 run.fields

AttributeError: 'Run' object has no attribute 'fields'

In [117]: run.value
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-117-4aae7a3d1fa8> in <module>()
----> 1 run.value

AttributeError: 'Run' object has no attribute 'value'

In [118]: run.values
Out[118]: 
{u'amar_o': <temba_client.v2.types.Value at 0x7fcefb43c590>,
 u'beg_o': <temba_client.v2.types.Value at 0x7fcefb43c4d0>,
 u'confirm': <temba_client.v2.types.Value at 0x7fcf080c2c50>,
 u'dcur_o': <temba_client.v2.types.Value at 0x7fcefb43c5d0>,
 u'dead_o': <temba_client.v2.types.Value at 0x7fcefb43c490>,
 u'defu_o': <temba_client.v2.types.Value at 0x7fcf080c2250>,
 u'dmed_o': <temba_client.v2.types.Value at 0x7fcefa7ba890>,
 u'msg_routing': <temba_client.v2.types.Value at 0x7fcefa7ba910>,
 u'role': <temba_client.v2.types.Value at 0x7fcefb43c450>,
 u'tin_o': <temba_client.v2.types.Value at 0x7fcefb43c350>,
 u'tout_o': <temba_client.v2.types.Value at 0x7fcf080c29d0>,
 u'type': <temba_client.v2.types.Value at 0x7fcefa7ba810>,
 u'weeknum': <temba_client.v2.types.Value at 0x7fcefb43c110>}

In [119]: run.values
Out[119]: 
{u'amar_o': <temba_client.v2.types.Value at 0x7fcefb43c590>,
 u'beg_o': <temba_client.v2.types.Value at 0x7fcefb43c4d0>,
 u'confirm': <temba_client.v2.types.Value at 0x7fcf080c2c50>,
 u'dcur_o': <temba_client.v2.types.Value at 0x7fcefb43c5d0>,
 u'dead_o': <temba_client.v2.types.Value at 0x7fcefb43c490>,
 u'defu_o': <temba_client.v2.types.Value at 0x7fcf080c2250>,
 u'dmed_o': <temba_client.v2.types.Value at 0x7fcefa7ba890>,
 u'msg_routing': <temba_client.v2.types.Value at 0x7fcefa7ba910>,
 u'role': <temba_client.v2.types.Value at 0x7fcefb43c450>,
 u'tin_o': <temba_client.v2.types.Value at 0x7fcefb43c350>,
 u'tout_o': <temba_client.v2.types.Value at 0x7fcf080c29d0>,
 u'type': <temba_client.v2.types.Value at 0x7fcefa7ba810>,
 u'weeknum': <temba_client.v2.types.Value at 0x7fcefb43c110>}

In [120]: run.values['amar_o']
Out[120]: <temba_client.v2.types.Value at 0x7fcefb43c590>

In [121]: w = run.values['amar_o']

In [122]: w.value
Out[122]: 0.0

In [123]: w.category
Out[123]: u'0 - 9999'

In [124]: w.value
Out[124]: 0.0

In [125]: w.deserialize?
Signature: w.deserialize(item)
Docstring: <no docstring>
File:      ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/serialization.py
Type:      instancemethod

In [126]: w??
Type:        Value
String form: <temba_client.v2.types.Value object at 0x7fcefb43c590>
File:        ~/PycharmProjects/IMAM/ve/local/lib/python2.7/site-packages/temba_client/v2/types.py
Source:     
    class Value(TembaObject):
        value = SimpleField()
        category = SimpleField()
        node = SimpleField()
        time = DatetimeField()

In [127]: w.value
Out[127]: 0.0

In [128]: w.time
Out[128]: datetime.datetime(2017, 4, 10, 13, 7, 18, 683588, tzinfo=<UTC>)

In[1]:
from temba_client.v2 import TembaClient

In[2]: client = TembaClient('rapidpro.io', open('token').read())

In[3]: client.get_flows()
Out[3]: < temba_client.clients.CursorQuery
at
0x7fcf081b9e10 >

In[4]: list(client.get_flows())
---------------------------------------------------------------------------
TypeError
Traceback(most
recent
call
last)
< ipython - input - 4 - 3
adda10cf3a5 > in < module > ()
----> 1
list(client.get_flows())

TypeError: 'CursorQuery'
object is not iterable

In[5]: a = client.get_flows().iterfetches()

In[6]: a
Out[6]: < temba_client.clients.CursorIterator
at
0x7fcf08107350 >

In[7]: list(a)
---------------------------------------------------------------------------
ValueError
Traceback(most
recent
call
last)
< ipython - input - 7 - 61
edcfee5862 > in < module > ()
----> 1
list(a)

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / six.pyc in next(self)
556
557


def next(self):


  --> 558
return type(self).__next__(self)
559
560
callable = callable

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / clients.pyc in __next__(self)
273
274
response = self.client._request('get', self.url, params=self.params,
                                --> 275
retry_on_rate_exceed = self.retry_on_rate_exceed)
276
277
self.url = response['next']

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / clients.pyc in _request(self, method, url, params, body, retry_on_rate_exceed)
350
return self._request_wth_rate_limit_retry(method, url, params=params, body=body)
351         else:
--> 352
return super(BaseCursorClient, self)._request(method, url, params=params, body=body)
353
354


def _request_wth_rate_limit_retry(self, method, url, params=None, body=None):

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / clients.pyc in _request(self, method, url, params, body)
86
kwargs['verify'] = self.verify_ssl
87
---> 88
response = request(method, url, **kwargs)
89
90
if response.status_code == 400:

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / utils.pyc in request(method, url, **kwargs)
52
kwargs['data'] = json.dumps(kwargs['data'])
53
---> 54
return requests.request(method, url, **kwargs)

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / requests / api.pyc in request(method, url, **kwargs)
54  # cases, and look like a memory leak in others.
55
with sessions.Session() as session:
  ---> 56
return session.request(method=method, url=url, **kwargs)
57
58

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / requests / sessions.pyc in request(self, method, url, params, data, headers, cookies, files,
                                                          auth, timeout, allow_redirects, proxies, hooks, stream,
                                                          verify, cert, json)
486}
487
send_kwargs.update(settings)
--> 488
resp = self.send(prep, **send_kwargs)
489
490
return resp

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / requests / sessions.pyc in send(self, request, **kwargs)
607
608  # Send the request
--> 609
r = adapter.send(request, **kwargs)
610
611  # Total elapsed time of the request (approximately)

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / requests / adapters.pyc in send(self, request, stream, timeout, verify, cert, proxies)
421
decode_content = False,
422
retries = self.max_retries,
--> 423
timeout = timeout
424                 )
425

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / requests / packages / urllib3 / connectionpool.pyc in urlopen(self, method, url, body, headers,
                                                                                     retries, redirect,
                                                                                     assert_same_host, timeout,
                                                                                     pool_timeout, release_conn,
                                                                                     chunked, body_pos, **response_kw)
598
timeout = timeout_obj,
          599
body = body, headers = headers,
                       --> 600
chunked = chunked)
601
602  # If we're going to release the connection in ``finally:``, then

/ home / robert / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / requests / packages / urllib3 / connectionpool.pyc in _make_request(self, conn, method, url,
                                                                                           timeout, chunked,
                                                                                           **httplib_request_kw)
354
conn.request_chunked(method, url, **httplib_request_kw)
355         else:
--> 356
conn.request(method, url, **httplib_request_kw)
357
358  # Reset the timeout for the recv() on the socket

/ usr / lib / python2
.7 / httplib.pyc in request(self, method, url, body, headers)
1055


def request(self, method, url, body=None, headers={}):
  1056
  """Send a complete request to the server."""

-> 1057
self._send_request(method, url, body, headers)
1058
1059


def _set_content_length(self, body, method):

/ usr / lib / python2
.7 / httplib.pyc in _send_request(self, method, url, body, headers)
1094
self._set_content_length(body, method)
1095
for hdr, value in headers.iteritems():
  -> 1096
self.putheader(hdr, value)
1097
self.endheaders(body)
1098

/ usr / lib / python2
.7 / httplib.pyc in putheader(self, header, *values)
1033
for one_value in values:
  1034
  if _is_illegal_header_value(one_value):
-> 1035
raise ValueError('Invalid header value %r' % (one_value,))
1036
1037
hdr = '%s: %s' % (header, '\r\n\t'.join(values))

ValueError: Invalid
header
value
'Token 7367778c1befefbe75ebb99484839f30e18c8fba\n'

In[8]: client = TembaClient('rapidpro.io', open('token').read().strip())

In[9]: a = client.get_flows().iterfetches()

In[10]: list(a)
Out[10]:
[[ < temba_client.v2.types.Flow at 0x7fcf08071dd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482050 >,
< temba_client.v2.types.Flow
at
0x7fcefb482110 >,
< temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482290 >,
< temba_client.v2.types.Flow
at
0x7fcefb482390 >,
< temba_client.v2.types.Flow
at
0x7fcefb482490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482690 >,
< temba_client.v2.types.Flow
at
0x7fcefb482750 >,
< temba_client.v2.types.Flow
at
0x7fcefb482810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4828d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482990 >,
< temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483190 >,
< temba_client.v2.types.Flow
at
0x7fcefb483250 >,
< temba_client.v2.types.Flow
at
0x7fcefb483310 >,
< temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483690 >,
< temba_client.v2.types.Flow
at
0x7fcefb483750 >,
< temba_client.v2.types.Flow
at
0x7fcefb483810 >,
< temba_client.v2.types.Flow
at
0x7fcefb483950 >,
< temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484090 >,
< temba_client.v2.types.Flow
at
0x7fcefb484150 >,
< temba_client.v2.types.Flow
at
0x7fcefb484210 >,
< temba_client.v2.types.Flow
at
0x7fcefb4842d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484390 >,
< temba_client.v2.types.Flow
at
0x7fcefb484450 >,
< temba_client.v2.types.Flow
at
0x7fcefb484510 >,
< temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484690 >,
< temba_client.v2.types.Flow
at
0x7fcefb484750 >,
< temba_client.v2.types.Flow
at
0x7fcefb484810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484990 >,
< temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093090 >,
< temba_client.v2.types.Flow
at
0x7fcf08093150 >,
< temba_client.v2.types.Flow
at
0x7fcf08093210 >,
< temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093390 >,
< temba_client.v2.types.Flow
at
0x7fcf08093450 >,
< temba_client.v2.types.Flow
at
0x7fcf08093510 >,
< temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093690 >,
< temba_client.v2.types.Flow
at
0x7fcf08093750 >,
< temba_client.v2.types.Flow
at
0x7fcf08093810 >,
< temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093990 >,
< temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098090 >,
< temba_client.v2.types.Flow
at
0x7fcf08098150 >,
< temba_client.v2.types.Flow
at
0x7fcf08098210 >,
< temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098390 >,
< temba_client.v2.types.Flow
at
0x7fcf08098450 >,
< temba_client.v2.types.Flow
at
0x7fcf08098510 >,
< temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098690 >,
< temba_client.v2.types.Flow
at
0x7fcf08098750 >,
< temba_client.v2.types.Flow
at
0x7fcf08098810 >,
< temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098990 >,
< temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
< temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
< temba_client.v2.types.Flow
at
0x7fcf080add10 >,
< temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
< temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
< temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1410 >]]

In[11]: flows = _

In[12]: flows
Out[12]:
[[ < temba_client.v2.types.Flow at 0x7fcf08071dd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482050 >,
< temba_client.v2.types.Flow
at
0x7fcefb482110 >,
< temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482290 >,
< temba_client.v2.types.Flow
at
0x7fcefb482390 >,
< temba_client.v2.types.Flow
at
0x7fcefb482490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482690 >,
< temba_client.v2.types.Flow
at
0x7fcefb482750 >,
< temba_client.v2.types.Flow
at
0x7fcefb482810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4828d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482990 >,
< temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483190 >,
< temba_client.v2.types.Flow
at
0x7fcefb483250 >,
< temba_client.v2.types.Flow
at
0x7fcefb483310 >,
< temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483690 >,
< temba_client.v2.types.Flow
at
0x7fcefb483750 >,
< temba_client.v2.types.Flow
at
0x7fcefb483810 >,
< temba_client.v2.types.Flow
at
0x7fcefb483950 >,
< temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484090 >,
< temba_client.v2.types.Flow
at
0x7fcefb484150 >,
< temba_client.v2.types.Flow
at
0x7fcefb484210 >,
< temba_client.v2.types.Flow
at
0x7fcefb4842d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484390 >,
< temba_client.v2.types.Flow
at
0x7fcefb484450 >,
< temba_client.v2.types.Flow
at
0x7fcefb484510 >,
< temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484690 >,
< temba_client.v2.types.Flow
at
0x7fcefb484750 >,
< temba_client.v2.types.Flow
at
0x7fcefb484810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484990 >,
< temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093090 >,
< temba_client.v2.types.Flow
at
0x7fcf08093150 >,
< temba_client.v2.types.Flow
at
0x7fcf08093210 >,
< temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093390 >,
< temba_client.v2.types.Flow
at
0x7fcf08093450 >,
< temba_client.v2.types.Flow
at
0x7fcf08093510 >,
< temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093690 >,
< temba_client.v2.types.Flow
at
0x7fcf08093750 >,
< temba_client.v2.types.Flow
at
0x7fcf08093810 >,
< temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093990 >,
< temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098090 >,
< temba_client.v2.types.Flow
at
0x7fcf08098150 >,
< temba_client.v2.types.Flow
at
0x7fcf08098210 >,
< temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098390 >,
< temba_client.v2.types.Flow
at
0x7fcf08098450 >,
< temba_client.v2.types.Flow
at
0x7fcf08098510 >,
< temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098690 >,
< temba_client.v2.types.Flow
at
0x7fcf08098750 >,
< temba_client.v2.types.Flow
at
0x7fcf08098810 >,
< temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098990 >,
< temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
< temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
< temba_client.v2.types.Flow
at
0x7fcf080add10 >,
< temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
< temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
< temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1410 >]]

In[13]: f = flows[0]

In[14]: f
Out[14]:
[ < temba_client.v2.types.Flow
at
0x7fcf08071dd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482050 >,
< temba_client.v2.types.Flow
at
0x7fcefb482110 >,
< temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482290 >,
< temba_client.v2.types.Flow
at
0x7fcefb482390 >,
< temba_client.v2.types.Flow
at
0x7fcefb482490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482690 >,
< temba_client.v2.types.Flow
at
0x7fcefb482750 >,
< temba_client.v2.types.Flow
at
0x7fcefb482810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4828d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482990 >,
< temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483190 >,
< temba_client.v2.types.Flow
at
0x7fcefb483250 >,
< temba_client.v2.types.Flow
at
0x7fcefb483310 >,
< temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483690 >,
< temba_client.v2.types.Flow
at
0x7fcefb483750 >,
< temba_client.v2.types.Flow
at
0x7fcefb483810 >,
< temba_client.v2.types.Flow
at
0x7fcefb483950 >,
< temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484090 >,
< temba_client.v2.types.Flow
at
0x7fcefb484150 >,
< temba_client.v2.types.Flow
at
0x7fcefb484210 >,
< temba_client.v2.types.Flow
at
0x7fcefb4842d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484390 >,
< temba_client.v2.types.Flow
at
0x7fcefb484450 >,
< temba_client.v2.types.Flow
at
0x7fcefb484510 >,
< temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484690 >,
< temba_client.v2.types.Flow
at
0x7fcefb484750 >,
< temba_client.v2.types.Flow
at
0x7fcefb484810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484990 >,
< temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093090 >,
< temba_client.v2.types.Flow
at
0x7fcf08093150 >,
< temba_client.v2.types.Flow
at
0x7fcf08093210 >,
< temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093390 >,
< temba_client.v2.types.Flow
at
0x7fcf08093450 >,
< temba_client.v2.types.Flow
at
0x7fcf08093510 >,
< temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093690 >,
< temba_client.v2.types.Flow
at
0x7fcf08093750 >,
< temba_client.v2.types.Flow
at
0x7fcf08093810 >,
< temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093990 >,
< temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098090 >,
< temba_client.v2.types.Flow
at
0x7fcf08098150 >,
< temba_client.v2.types.Flow
at
0x7fcf08098210 >,
< temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098390 >,
< temba_client.v2.types.Flow
at
0x7fcf08098450 >,
< temba_client.v2.types.Flow
at
0x7fcf08098510 >,
< temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098690 >,
< temba_client.v2.types.Flow
at
0x7fcf08098750 >,
< temba_client.v2.types.Flow
at
0x7fcf08098810 >,
< temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098990 >,
< temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
< temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
< temba_client.v2.types.Flow
at
0x7fcf080add10 >,
< temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
< temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
< temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1410 >]

In[15]: f = flows[0]

In[16]: f
Out[16]:
[ < temba_client.v2.types.Flow
at
0x7fcf08071dd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482050 >,
< temba_client.v2.types.Flow
at
0x7fcefb482110 >,
< temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482290 >,
< temba_client.v2.types.Flow
at
0x7fcefb482390 >,
< temba_client.v2.types.Flow
at
0x7fcefb482490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482690 >,
< temba_client.v2.types.Flow
at
0x7fcefb482750 >,
< temba_client.v2.types.Flow
at
0x7fcefb482810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4828d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482990 >,
< temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483190 >,
< temba_client.v2.types.Flow
at
0x7fcefb483250 >,
< temba_client.v2.types.Flow
at
0x7fcefb483310 >,
< temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483690 >,
< temba_client.v2.types.Flow
at
0x7fcefb483750 >,
< temba_client.v2.types.Flow
at
0x7fcefb483810 >,
< temba_client.v2.types.Flow
at
0x7fcefb483950 >,
< temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484090 >,
< temba_client.v2.types.Flow
at
0x7fcefb484150 >,
< temba_client.v2.types.Flow
at
0x7fcefb484210 >,
< temba_client.v2.types.Flow
at
0x7fcefb4842d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484390 >,
< temba_client.v2.types.Flow
at
0x7fcefb484450 >,
< temba_client.v2.types.Flow
at
0x7fcefb484510 >,
< temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484690 >,
< temba_client.v2.types.Flow
at
0x7fcefb484750 >,
< temba_client.v2.types.Flow
at
0x7fcefb484810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484990 >,
< temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093090 >,
< temba_client.v2.types.Flow
at
0x7fcf08093150 >,
< temba_client.v2.types.Flow
at
0x7fcf08093210 >,
< temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093390 >,
< temba_client.v2.types.Flow
at
0x7fcf08093450 >,
< temba_client.v2.types.Flow
at
0x7fcf08093510 >,
< temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093690 >,
< temba_client.v2.types.Flow
at
0x7fcf08093750 >,
< temba_client.v2.types.Flow
at
0x7fcf08093810 >,
< temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093990 >,
< temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098090 >,
< temba_client.v2.types.Flow
at
0x7fcf08098150 >,
< temba_client.v2.types.Flow
at
0x7fcf08098210 >,
< temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098390 >,
< temba_client.v2.types.Flow
at
0x7fcf08098450 >,
< temba_client.v2.types.Flow
at
0x7fcf08098510 >,
< temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098690 >,
< temba_client.v2.types.Flow
at
0x7fcf08098750 >,
< temba_client.v2.types.Flow
at
0x7fcf08098810 >,
< temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098990 >,
< temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
< temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
< temba_client.v2.types.Flow
at
0x7fcf080add10 >,
< temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
< temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
< temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1410 >]

In[17]: f = flows[0]

In[18]: f
Out[18]:
[ < temba_client.v2.types.Flow
at
0x7fcf08071dd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482050 >,
< temba_client.v2.types.Flow
at
0x7fcefb482110 >,
< temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482290 >,
< temba_client.v2.types.Flow
at
0x7fcefb482390 >,
< temba_client.v2.types.Flow
at
0x7fcefb482490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482690 >,
< temba_client.v2.types.Flow
at
0x7fcefb482750 >,
< temba_client.v2.types.Flow
at
0x7fcefb482810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4828d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482990 >,
< temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483190 >,
< temba_client.v2.types.Flow
at
0x7fcefb483250 >,
< temba_client.v2.types.Flow
at
0x7fcefb483310 >,
< temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483690 >,
< temba_client.v2.types.Flow
at
0x7fcefb483750 >,
< temba_client.v2.types.Flow
at
0x7fcefb483810 >,
< temba_client.v2.types.Flow
at
0x7fcefb483950 >,
< temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484090 >,
< temba_client.v2.types.Flow
at
0x7fcefb484150 >,
< temba_client.v2.types.Flow
at
0x7fcefb484210 >,
< temba_client.v2.types.Flow
at
0x7fcefb4842d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484390 >,
< temba_client.v2.types.Flow
at
0x7fcefb484450 >,
< temba_client.v2.types.Flow
at
0x7fcefb484510 >,
< temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484690 >,
< temba_client.v2.types.Flow
at
0x7fcefb484750 >,
< temba_client.v2.types.Flow
at
0x7fcefb484810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484990 >,
< temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093090 >,
< temba_client.v2.types.Flow
at
0x7fcf08093150 >,
< temba_client.v2.types.Flow
at
0x7fcf08093210 >,
< temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093390 >,
< temba_client.v2.types.Flow
at
0x7fcf08093450 >,
< temba_client.v2.types.Flow
at
0x7fcf08093510 >,
< temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093690 >,
< temba_client.v2.types.Flow
at
0x7fcf08093750 >,
< temba_client.v2.types.Flow
at
0x7fcf08093810 >,
< temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093990 >,
< temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098090 >,
< temba_client.v2.types.Flow
at
0x7fcf08098150 >,
< temba_client.v2.types.Flow
at
0x7fcf08098210 >,
< temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098390 >,
< temba_client.v2.types.Flow
at
0x7fcf08098450 >,
< temba_client.v2.types.Flow
at
0x7fcf08098510 >,
< temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098690 >,
< temba_client.v2.types.Flow
at
0x7fcf08098750 >,
< temba_client.v2.types.Flow
at
0x7fcf08098810 >,
< temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098990 >,
< temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
< temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
< temba_client.v2.types.Flow
at
0x7fcf080add10 >,
< temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
< temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
< temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1410 >]

In[19]: flows
Out[19]:
[[ < temba_client.v2.types.Flow at 0x7fcf08071dd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482050 >,
< temba_client.v2.types.Flow
at
0x7fcefb482110 >,
< temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482290 >,
< temba_client.v2.types.Flow
at
0x7fcefb482390 >,
< temba_client.v2.types.Flow
at
0x7fcefb482490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482690 >,
< temba_client.v2.types.Flow
at
0x7fcefb482750 >,
< temba_client.v2.types.Flow
at
0x7fcefb482810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4828d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482990 >,
< temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
< temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
< temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483190 >,
< temba_client.v2.types.Flow
at
0x7fcefb483250 >,
< temba_client.v2.types.Flow
at
0x7fcefb483310 >,
< temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483490 >,
< temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483690 >,
< temba_client.v2.types.Flow
at
0x7fcefb483750 >,
< temba_client.v2.types.Flow
at
0x7fcefb483810 >,
< temba_client.v2.types.Flow
at
0x7fcefb483950 >,
< temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
< temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484090 >,
< temba_client.v2.types.Flow
at
0x7fcefb484150 >,
< temba_client.v2.types.Flow
at
0x7fcefb484210 >,
< temba_client.v2.types.Flow
at
0x7fcefb4842d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484390 >,
< temba_client.v2.types.Flow
at
0x7fcefb484450 >,
< temba_client.v2.types.Flow
at
0x7fcefb484510 >,
< temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484690 >,
< temba_client.v2.types.Flow
at
0x7fcefb484750 >,
< temba_client.v2.types.Flow
at
0x7fcefb484810 >,
< temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484990 >,
< temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
< temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
< temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
< temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
< temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
< temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
< temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093090 >,
< temba_client.v2.types.Flow
at
0x7fcf08093150 >,
< temba_client.v2.types.Flow
at
0x7fcf08093210 >,
< temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093390 >,
< temba_client.v2.types.Flow
at
0x7fcf08093450 >,
< temba_client.v2.types.Flow
at
0x7fcf08093510 >,
< temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093690 >,
< temba_client.v2.types.Flow
at
0x7fcf08093750 >,
< temba_client.v2.types.Flow
at
0x7fcf08093810 >,
< temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093990 >,
< temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098090 >,
< temba_client.v2.types.Flow
at
0x7fcf08098150 >,
< temba_client.v2.types.Flow
at
0x7fcf08098210 >,
< temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098390 >,
< temba_client.v2.types.Flow
at
0x7fcf08098450 >,
< temba_client.v2.types.Flow
at
0x7fcf08098510 >,
< temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098690 >,
< temba_client.v2.types.Flow
at
0x7fcf08098750 >,
< temba_client.v2.types.Flow
at
0x7fcf08098810 >,
< temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098990 >,
< temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
< temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
< temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
< temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
< temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
< temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
< temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
< temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
< temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
< temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
< temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
< temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
< temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
< temba_client.v2.types.Flow
at
0x7fcf080add10 >,
< temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
< temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
< temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
< temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
< temba_client.v2.types.Flow
at
0x7fcf080b1410 >]]

In[20]: f = flows[0][0]

In[21]: f
Out[21]: < temba_client.v2.types.Flow
at
0x7fcf08071dd0 >

In[22]: f.name
Out[22]: u'Dispatch in'

In[23]: [x.name for x flows[0]]
File
"<ipython-input-23-6685073b6dad>", line
1
[x.name for x flows[0]]
^
SyntaxError: invalid
syntax

In[24]: [x.name for x in flows[0]]
Out[24]:
[u'Dispatch in',
 u'Dispatch',
 u'MNCH week Phone Return',
 u'Training on writing SMS',
 u'Use Trigger Word',
 u'MNP Program',
 u'MNP Registration',
 u'IMAM SMS Router',
 u'stockouttest',
 u'Letters_numbers',
 u'MNP Stock Monitoring Flow',
 u'Copy of MNP Stock Monitoring Flow',
 u'MNP LGA NFP Follow up',
 u'Copy of MNP Stock Monitoring Flow',
 u'Health poll (One.org)',
 u'MNP LGA NFP Follow up',
 u'SDGs ',
 u'MNP stock follow up',
 u'MNP Stock Monitoring Flow',
 u'Micronutrient Powders Caregivers',
 u'MNDC Taskforce',
 u'Copy of IMAM Register',
 u'MNCHW Supply Monitor - Flow B',
 u'Single Message (14159)',
 u'Single Message (14157)',
 u'test',
 u'MNCHW test',
 u'IMAM LGA State Stocks',
 u'Test contact',
 u'Validate',
 u'MYR Demo',
 u'IMAM Validate',
 u'IYCF',
 u'Choose Language',
 u'IMAM Stock',
 u'IMAM Screening',
 u'IMAM Program',
 u'IMAM Register',
 u'IMAM',
 u'MNCHW supply confirmation',
 u'Federal Monitors Confirmation',
 u'yvb',
 u'RPBA CMAM Monitoring',
 u'mnchlgatt',
 u'mnchlgatt',
 u'mnchw lga nfp flow B',
 u'MNCH lga nfp test',
 u'MNCHW LGA NFP-Day 2',
 u'MNCHW LGA Focal Person-Day 1',
 u'MNCHW Supply-Flow B',
 u'MNCHW Supply Monitor- Flow A',
 u'MNCHW_Monitoring Register',
 u'Ping',
 u'SAM Start',
 u'Example Flow Nutrition (Arabic)',
 u'Copy of Example Flow Nutrition (English)',
 u'Example Flow Nutrition (English)',
 u'Single Message (10470)',
 u'Single Message (10469)',
 u'Single Message (10468)',
 u'Single Message (10467)',
 u'Single Message (10466)',
 u'Single Message (10465)',
 u'Single Message (10464)',
 u'Single Message (10463)',
 u'Single Message (10462)',
 u'Single Message (10461)',
 u'Single Message (10460)',
 u'Single Message (10459)',
 u'Single Message (10458)',
 u'Single Message (10457)',
 u'Single Message (10456)',
 u'Single Message (10455)',
 u'Single Message (10454)',
 u'Single Message (10453)',
 u'Single Message (10452)',
 u'Single Message (10451)',
 u'Single Message (10450)',
 u'Single Message (10449)',
 u'Single Message (10448)',
 u'Single Message (10447)',
 u'Single Message (10446)',
 u'Single Message (10445)',
 u'Single Message (10444)',
 u'Single Message (10443)',
 u'Single Message (10442)',
 u'Single Message (10441)',
 u'Single Message (10440)',
 u'Single Message (10439)',
 u'Single Message (10438)',
 u'Single Message (10437)',
 u'Single Message (10436)',
 u'Single Message (10435)',
 u'Single Message (10434)',
 u'Single Message (10433)',
 u'Single Message (10432)',
 u'Single Message (10431)',
 u'Single Message (10430)',
 u'Single Message (10429)',
 u'Single Message (10428)',
 u'Single Message (10427)',
 u'Single Message (10426)',
 u'Single Message (10425)',
 u'Single Message (10424)',
 u'Single Message (10423)',
 u'Single Message (10422)',
 u'Single Message (10421)',
 u'Single Message (10420)',
 u'Single Message (10419)',
 u'Single Message (10418)',
 u'Single Message (10417)',
 u'Single Message (10416)',
 u'Single Message (10415)',
 u'Single Message (10414)',
 u'Single Message (10413)',
 u'Single Message (10412)',
 u'Single Message (10411)',
 u'Single Message (10410)',
 u'Single Message (10409)',
 u'Single Message (10408)',
 u'Single Message (10407)',
 u'Single Message (10406)',
 u'Single Message (10405)',
 u'Single Message (10404)',
 u'Single Message (10403)',
 u'Single Message (10402)',
 u'Single Message (10401)',
 u'Single Message (10400)',
 u'Single Message (10399)',
 u'Single Message (10398)',
 u'Single Message (10397)',
 u'Single Message (10396)',
 u'Single Message (10395)',
 u'Single Message (10394)',
 u'Single Message (10393)',
 u'Single Message (10392)',
 u'Single Message (10391)',
 u'Single Message (10390)',
 u'Single Message (10389)',
 u'Single Message (10388)',
 u'Single Message (10387)',
 u'Single Message (10386)',
 u'Single Message (10385)',
 u'Single Message (10384)',
 u'Single Message (10383)',
 u'Single Message (10382)',
 u'Single Message (10381)',
 u'Single Message (10380)',
 u'Single Message (10379)',
 u'Single Message (10378)',
 u'Single Message (10377)',
 u'Single Message (10376)',
 u'Single Message (10375)',
 u'Single Message (10374)',
 u'Single Message (10373)',
 u'Single Message (10372)',
 u'Single Message (10371)',
 u'Single Message (10370)',
 u'Single Message (10369)',
 u'Single Message (10368)',
 u'Single Message (10367)',
 u'Single Message (10366)',
 u'Single Message (10365)',
 u'Single Message (10364)',
 u'Single Message (10363)',
 u'Single Message (10362)',
 u'Single Message (10361)',
 u'Single Message (10360)',
 u'Single Message (10359)',
 u'Single Message (10358)',
 u'Single Message (10357)',
 u'Single Message (10356)',
 u'Single Message (10355)',
 u'Single Message (10354)',
 u'Single Message (10353)',
 u'Single Message (10352)',
 u'Single Message (10351)',
 u'Single Message (10350)',
 u'Single Message (10349)',
 u'Single Message (10348)',
 u'Single Message (10347)',
 u'Single Message (10346)',
 u'Single Message (10345)',
 u'Single Message (10344)',
 u'Single Message (10343)',
 u'Single Message (10342)',
 u'Single Message (10341)',
 u'Single Message (10340)',
 u'Single Message (10339)',
 u'Single Message (10338)',
 u'Single Message (10337)',
 u'Single Message (10336)',
 u'Single Message (10335)',
 u'Single Message (10334)',
 u'Single Message (10333)',
 u'Single Message (10332)',
 u'Single Message (10331)',
 u'Single Message (10330)',
 u'Single Message (10329)',
 u'Single Message (10328)',
 u'Single Message (10327)',
 u'Single Message (10326)',
 u'Single Message (10325)',
 u'Single Message (10324)',
 u'Single Message (10323)',
 u'Single Message (10322)',
 u'Single Message (10321)',
 u'Single Message (10320)',
 u'Single Message (10319)',
 u'Single Message (10318)',
 u'Single Message (10317)',
 u'CHW Mother Registration (Notify Mother)',
 u'CHW Mother Registration',
 u'1st ANC visit',
 u'CHW Screening',
 u'CHW Daily Report',
 u'CHW Stocks',
 u'CHW Planning Populations',
 u'CHW Registration',
 u'SAM Validate',
 u'SAM Stock Report',
 u'SAM Stockout and Update',
 u'SAM Screen',
 u'SAM Register',
 u'SAM Program',
 u'SAM Despatch',
 u'Sample Flow -  Simple Poll',
 u'Sample Flow -  Satisfaction Survey',
 u'Sample Flow -  Order Status Checker',
 u'Sample Flow -  Group Chat']

In[25]: f
Out[25]: < temba_client.v2.types.Flow
at
0x7fcf08071dd0 >

In[26]: f.Runs
Out[26]: temba_client.v2.types.Runs

In[27]: f.Runs?
Docstring: < no
docstring >
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / v2 / types.py
Type: ABCMeta

In[28]: f.runs?
Type: Runs
String
form: < temba_client.v2.types.Runs
object
at
0x7fcf08071f90 >
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / v2 / types.py
Docstring: < no
docstring >

In[29]: f.runs
Out[29]: < temba_client.v2.types.Runs
at
0x7fcf08071f90 >

In[30]: f.Runs
Out[30]: temba_client.v2.types.Runs

In[31]: f.Runs.active
Out[31]: < temba_client.serialization.IntegerField
at
0x7fcf0c900790 >

In[32]: {x.name for x in flows[0]}
Out[32]:
{u'1st ANC visit',
 u'CHW Daily Report',
 u'CHW Mother Registration',
 u'CHW Mother Registration (Notify Mother)',
 u'CHW Planning Populations',
 u'CHW Registration',
 u'CHW Screening',
 u'CHW Stocks',
 u'Choose Language',
 u'Copy of Example Flow Nutrition (English)',
 u'Copy of IMAM Register',
 u'Copy of MNP Stock Monitoring Flow',
 u'Dispatch',
 u'Dispatch in',
 u'Example Flow Nutrition (Arabic)',
 u'Example Flow Nutrition (English)',
 u'Federal Monitors Confirmation',
 u'Health poll (One.org)',
 u'IMAM',
 u'IMAM LGA State Stocks',
 u'IMAM Program',
 u'IMAM Register',
 u'IMAM SMS Router',
 u'IMAM Screening',
 u'IMAM Stock',
 u'IMAM Validate',
 u'IYCF',
 u'Letters_numbers',
 u'MNCH lga nfp test',
 u'MNCH week Phone Return',
 u'MNCHW LGA Focal Person-Day 1',
 u'MNCHW LGA NFP-Day 2',
 u'MNCHW Supply Monitor - Flow B',
 u'MNCHW Supply Monitor- Flow A',
 u'MNCHW Supply-Flow B',
 u'MNCHW supply confirmation',
 u'MNCHW test',
 u'MNCHW_Monitoring Register',
 u'MNDC Taskforce',
 u'MNP LGA NFP Follow up',
 u'MNP Program',
 u'MNP Registration',
 u'MNP Stock Monitoring Flow',
 u'MNP stock follow up',
 u'MYR Demo',
 u'Micronutrient Powders Caregivers',
 u'Ping',
 u'RPBA CMAM Monitoring',
 u'SAM Despatch',
 u'SAM Program',
 u'SAM Register',
 u'SAM Screen',
 u'SAM Start',
 u'SAM Stock Report',
 u'SAM Stockout and Update',
 u'SAM Validate',
 u'SDGs ',
 u'Sample Flow -  Group Chat',
 u'Sample Flow -  Order Status Checker',
 u'Sample Flow -  Satisfaction Survey',
 u'Sample Flow -  Simple Poll',
 u'Single Message (10317)',
 u'Single Message (10318)',
 u'Single Message (10319)',
 u'Single Message (10320)',
 u'Single Message (10321)',
 u'Single Message (10322)',
 u'Single Message (10323)',
 u'Single Message (10324)',
 u'Single Message (10325)',
 u'Single Message (10326)',
 u'Single Message (10327)',
 u'Single Message (10328)',
 u'Single Message (10329)',
 u'Single Message (10330)',
 u'Single Message (10331)',
 u'Single Message (10332)',
 u'Single Message (10333)',
 u'Single Message (10334)',
 u'Single Message (10335)',
 u'Single Message (10336)',
 u'Single Message (10337)',
 u'Single Message (10338)',
 u'Single Message (10339)',
 u'Single Message (10340)',
 u'Single Message (10341)',
 u'Single Message (10342)',
 u'Single Message (10343)',
 u'Single Message (10344)',
 u'Single Message (10345)',
 u'Single Message (10346)',
 u'Single Message (10347)',
 u'Single Message (10348)',
 u'Single Message (10349)',
 u'Single Message (10350)',
 u'Single Message (10351)',
 u'Single Message (10352)',
 u'Single Message (10353)',
 u'Single Message (10354)',
 u'Single Message (10355)',
 u'Single Message (10356)',
 u'Single Message (10357)',
 u'Single Message (10358)',
 u'Single Message (10359)',
 u'Single Message (10360)',
 u'Single Message (10361)',
 u'Single Message (10362)',
 u'Single Message (10363)',
 u'Single Message (10364)',
 u'Single Message (10365)',
 u'Single Message (10366)',
 u'Single Message (10367)',
 u'Single Message (10368)',
 u'Single Message (10369)',
 u'Single Message (10370)',
 u'Single Message (10371)',
 u'Single Message (10372)',
 u'Single Message (10373)',
 u'Single Message (10374)',
 u'Single Message (10375)',
 u'Single Message (10376)',
 u'Single Message (10377)',
 u'Single Message (10378)',
 u'Single Message (10379)',
 u'Single Message (10380)',
 u'Single Message (10381)',
 u'Single Message (10382)',
 u'Single Message (10383)',
 u'Single Message (10384)',
 u'Single Message (10385)',
 u'Single Message (10386)',
 u'Single Message (10387)',
 u'Single Message (10388)',
 u'Single Message (10389)',
 u'Single Message (10390)',
 u'Single Message (10391)',
 u'Single Message (10392)',
 u'Single Message (10393)',
 u'Single Message (10394)',
 u'Single Message (10395)',
 u'Single Message (10396)',
 u'Single Message (10397)',
 u'Single Message (10398)',
 u'Single Message (10399)',
 u'Single Message (10400)',
 u'Single Message (10401)',
 u'Single Message (10402)',
 u'Single Message (10403)',
 u'Single Message (10404)',
 u'Single Message (10405)',
 u'Single Message (10406)',
 u'Single Message (10407)',
 u'Single Message (10408)',
 u'Single Message (10409)',
 u'Single Message (10410)',
 u'Single Message (10411)',
 u'Single Message (10412)',
 u'Single Message (10413)',
 u'Single Message (10414)',
 u'Single Message (10415)',
 u'Single Message (10416)',
 u'Single Message (10417)',
 u'Single Message (10418)',
 u'Single Message (10419)',
 u'Single Message (10420)',
 u'Single Message (10421)',
 u'Single Message (10422)',
 u'Single Message (10423)',
 u'Single Message (10424)',
 u'Single Message (10425)',
 u'Single Message (10426)',
 u'Single Message (10427)',
 u'Single Message (10428)',
 u'Single Message (10429)',
 u'Single Message (10430)',
 u'Single Message (10431)',
 u'Single Message (10432)',
 u'Single Message (10433)',
 u'Single Message (10434)',
 u'Single Message (10435)',
 u'Single Message (10436)',
 u'Single Message (10437)',
 u'Single Message (10438)',
 u'Single Message (10439)',
 u'Single Message (10440)',
 u'Single Message (10441)',
 u'Single Message (10442)',
 u'Single Message (10443)',
 u'Single Message (10444)',
 u'Single Message (10445)',
 u'Single Message (10446)',
 u'Single Message (10447)',
 u'Single Message (10448)',
 u'Single Message (10449)',
 u'Single Message (10450)',
 u'Single Message (10451)',
 u'Single Message (10452)',
 u'Single Message (10453)',
 u'Single Message (10454)',
 u'Single Message (10455)',
 u'Single Message (10456)',
 u'Single Message (10457)',
 u'Single Message (10458)',
 u'Single Message (10459)',
 u'Single Message (10460)',
 u'Single Message (10461)',
 u'Single Message (10462)',
 u'Single Message (10463)',
 u'Single Message (10464)',
 u'Single Message (10465)',
 u'Single Message (10466)',
 u'Single Message (10467)',
 u'Single Message (10468)',
 u'Single Message (10469)',
 u'Single Message (10470)',
 u'Single Message (14157)',
 u'Single Message (14159)',
 u'Test contact',
 u'Training on writing SMS',
 u'Use Trigger Word',
 u'Validate',
 u'mnchlgatt',
 u'mnchw lga nfp flow B',
 u'stockouttest',
 u'test',
 u'yvb'}

In[33]: {x.name: x for x in flows[0]}
Out[33]:
{u'1st ANC visit': < temba_client.v2.types.Flow
at
0x7fcf080ad650 >,
u'CHW Daily Report': < temba_client.v2.types.Flow
at
0x7fcf080ad850 >,
u'CHW Mother Registration': < temba_client.v2.types.Flow
at
0x7fcf080ad550 >,
u'CHW Mother Registration (Notify Mother)': < temba_client.v2.types.Flow
at
0x7fcf080ad450 >,
u'CHW Planning Populations': < temba_client.v2.types.Flow
at
0x7fcf080ada50 >,
u'CHW Registration': < temba_client.v2.types.Flow
at
0x7fcf080adb50 >,
u'CHW Screening': < temba_client.v2.types.Flow
at
0x7fcf080ad750 >,
u'CHW Stocks': < temba_client.v2.types.Flow
at
0x7fcf080ad950 >,
u'Choose Language': < temba_client.v2.types.Flow
at
0x7fcefb483a50 >,
u'Copy of Example Flow Nutrition (English)': < temba_client.v2.types.Flow
at
0x7fcefb484d50 >,
u'Copy of IMAM Register': < temba_client.v2.types.Flow
at
0x7fcefb482fd0 >,
u'Copy of MNP Stock Monitoring Flow': < temba_client.v2.types.Flow
at
0x7fcefb482990 >,
u'Dispatch': < temba_client.v2.types.Flow
at
0x7fcf08071c90 >,
u'Dispatch in': < temba_client.v2.types.Flow
at
0x7fcf08071dd0 >,
u'Example Flow Nutrition (Arabic)': < temba_client.v2.types.Flow
at
0x7fcefb484c90 >,
u'Example Flow Nutrition (English)': < temba_client.v2.types.Flow
at
0x7fcefb484e10 >,
u'Federal Monitors Confirmation': < temba_client.v2.types.Flow
at
0x7fcefb484210 >,
u'Health poll (One.org)': < temba_client.v2.types.Flow
at
0x7fcefb482a50 >,
u'IMAM': < temba_client.v2.types.Flow
at
0x7fcefb484090 >,
u'IMAM LGA State Stocks': < temba_client.v2.types.Flow
at
0x7fcefb483490 >,
u'IMAM Program': < temba_client.v2.types.Flow
at
0x7fcefb483dd0 >,
u'IMAM Register': < temba_client.v2.types.Flow
at
0x7fcefb483f10 >,
u'IMAM SMS Router': < temba_client.v2.types.Flow
at
0x7fcefb482490 >,
u'IMAM Screening': < temba_client.v2.types.Flow
at
0x7fcefb483c90 >,
u'IMAM Stock': < temba_client.v2.types.Flow
at
0x7fcefb483b50 >,
u'IMAM Validate': < temba_client.v2.types.Flow
at
0x7fcefb483810 >,
u'IYCF': < temba_client.v2.types.Flow
at
0x7fcefb483950 >,
u'Letters_numbers': < temba_client.v2.types.Flow
at
0x7fcefb482690 >,
u'MNCH lga nfp test': < temba_client.v2.types.Flow
at
0x7fcefb484690 >,
u'MNCH week Phone Return': < temba_client.v2.types.Flow
at
0x7fcefb482050 >,
u'MNCHW LGA Focal Person-Day 1': < temba_client.v2.types.Flow
at
0x7fcefb484810 >,
u'MNCHW LGA NFP-Day 2': < temba_client.v2.types.Flow
at
0x7fcefb484750 >,
u'MNCHW Supply Monitor - Flow B': < temba_client.v2.types.Flow
at
0x7fcefb4830d0 >,
u'MNCHW Supply Monitor- Flow A': < temba_client.v2.types.Flow
at
0x7fcefb484990 >,
u'MNCHW Supply-Flow B': < temba_client.v2.types.Flow
at
0x7fcefb4848d0 >,
u'MNCHW supply confirmation': < temba_client.v2.types.Flow
at
0x7fcefb484150 >,
u'MNCHW test': < temba_client.v2.types.Flow
at
0x7fcefb4833d0 >,
u'MNCHW_Monitoring Register': < temba_client.v2.types.Flow
at
0x7fcefb484a50 >,
u'MNDC Taskforce': < temba_client.v2.types.Flow
at
0x7fcefb482f10 >,
u'MNP LGA NFP Follow up': < temba_client.v2.types.Flow
at
0x7fcefb482b10 >,
u'MNP Program': < temba_client.v2.types.Flow
at
0x7fcefb482290 >,
u'MNP Registration': < temba_client.v2.types.Flow
at
0x7fcefb482390 >,
u'MNP Stock Monitoring Flow': < temba_client.v2.types.Flow
at
0x7fcefb482d90 >,
u'MNP stock follow up': < temba_client.v2.types.Flow
at
0x7fcefb482c90 >,
u'MYR Demo': < temba_client.v2.types.Flow
at
0x7fcefb483750 >,
u'Micronutrient Powders Caregivers': < temba_client.v2.types.Flow
at
0x7fcefb482e50 >,
u'Ping': < temba_client.v2.types.Flow
at
0x7fcefb484b10 >,
u'RPBA CMAM Monitoring': < temba_client.v2.types.Flow
at
0x7fcefb484390 >,
u'SAM Despatch': < temba_client.v2.types.Flow
at
0x7fcf080b1110 >,
u'SAM Program': < temba_client.v2.types.Flow
at
0x7fcf080b1050 >,
u'SAM Register': < temba_client.v2.types.Flow
at
0x7fcf080adf50 >,
u'SAM Screen': < temba_client.v2.types.Flow
at
0x7fcf080ade90 >,
u'SAM Start': < temba_client.v2.types.Flow
at
0x7fcefb484bd0 >,
u'SAM Stock Report': < temba_client.v2.types.Flow
at
0x7fcf080add10 >,
u'SAM Stockout and Update': < temba_client.v2.types.Flow
at
0x7fcf080addd0 >,
u'SAM Validate': < temba_client.v2.types.Flow
at
0x7fcf080adc50 >,
u'SDGs ': < temba_client.v2.types.Flow
at
0x7fcefb482bd0 >,
u'Sample Flow -  Group Chat': < temba_client.v2.types.Flow
at
0x7fcf080b1410 >,
u'Sample Flow -  Order Status Checker': < temba_client.v2.types.Flow
at
0x7fcf080b1350 >,
u'Sample Flow -  Satisfaction Survey': < temba_client.v2.types.Flow
at
0x7fcf080b1290 >,
u'Sample Flow -  Simple Poll': < temba_client.v2.types.Flow
at
0x7fcf080b11d0 >,
u'Single Message (10317)': < temba_client.v2.types.Flow
at
0x7fcf080ad390 >,
u'Single Message (10318)': < temba_client.v2.types.Flow
at
0x7fcf080ad2d0 >,
u'Single Message (10319)': < temba_client.v2.types.Flow
at
0x7fcf080ad210 >,
u'Single Message (10320)': < temba_client.v2.types.Flow
at
0x7fcf080ad150 >,
u'Single Message (10321)': < temba_client.v2.types.Flow
at
0x7fcf080ad090 >,
u'Single Message (10322)': < temba_client.v2.types.Flow
at
0x7fcf080a9f90 >,
u'Single Message (10323)': < temba_client.v2.types.Flow
at
0x7fcf080a9ed0 >,
u'Single Message (10324)': < temba_client.v2.types.Flow
at
0x7fcf080a9e10 >,
u'Single Message (10325)': < temba_client.v2.types.Flow
at
0x7fcf080a9d50 >,
u'Single Message (10326)': < temba_client.v2.types.Flow
at
0x7fcf080a9c90 >,
u'Single Message (10327)': < temba_client.v2.types.Flow
at
0x7fcf080a9bd0 >,
u'Single Message (10328)': < temba_client.v2.types.Flow
at
0x7fcf080a9b10 >,
u'Single Message (10329)': < temba_client.v2.types.Flow
at
0x7fcf080a9a50 >,
u'Single Message (10330)': < temba_client.v2.types.Flow
at
0x7fcf080a9990 >,
u'Single Message (10331)': < temba_client.v2.types.Flow
at
0x7fcf080a98d0 >,
u'Single Message (10332)': < temba_client.v2.types.Flow
at
0x7fcf080a9810 >,
u'Single Message (10333)': < temba_client.v2.types.Flow
at
0x7fcf080a9750 >,
u'Single Message (10334)': < temba_client.v2.types.Flow
at
0x7fcf080a9690 >,
u'Single Message (10335)': < temba_client.v2.types.Flow
at
0x7fcf080a95d0 >,
u'Single Message (10336)': < temba_client.v2.types.Flow
at
0x7fcf080a9510 >,
u'Single Message (10337)': < temba_client.v2.types.Flow
at
0x7fcf080a9450 >,
u'Single Message (10338)': < temba_client.v2.types.Flow
at
0x7fcf080a9390 >,
u'Single Message (10339)': < temba_client.v2.types.Flow
at
0x7fcf080a92d0 >,
u'Single Message (10340)': < temba_client.v2.types.Flow
at
0x7fcf080a9210 >,
u'Single Message (10341)': < temba_client.v2.types.Flow
at
0x7fcf080a9150 >,
u'Single Message (10342)': < temba_client.v2.types.Flow
at
0x7fcf080a9090 >,
u'Single Message (10343)': < temba_client.v2.types.Flow
at
0x7fcf080a4f90 >,
u'Single Message (10344)': < temba_client.v2.types.Flow
at
0x7fcf080a4ed0 >,
u'Single Message (10345)': < temba_client.v2.types.Flow
at
0x7fcf080a4e10 >,
u'Single Message (10346)': < temba_client.v2.types.Flow
at
0x7fcf080a4d50 >,
u'Single Message (10347)': < temba_client.v2.types.Flow
at
0x7fcf080a4c90 >,
u'Single Message (10348)': < temba_client.v2.types.Flow
at
0x7fcf080a4bd0 >,
u'Single Message (10349)': < temba_client.v2.types.Flow
at
0x7fcf080a4b10 >,
u'Single Message (10350)': < temba_client.v2.types.Flow
at
0x7fcf080a4a50 >,
u'Single Message (10351)': < temba_client.v2.types.Flow
at
0x7fcf080a4990 >,
u'Single Message (10352)': < temba_client.v2.types.Flow
at
0x7fcf080a48d0 >,
u'Single Message (10353)': < temba_client.v2.types.Flow
at
0x7fcf080a4810 >,
u'Single Message (10354)': < temba_client.v2.types.Flow
at
0x7fcf080a4750 >,
u'Single Message (10355)': < temba_client.v2.types.Flow
at
0x7fcf080a4690 >,
u'Single Message (10356)': < temba_client.v2.types.Flow
at
0x7fcf080a45d0 >,
u'Single Message (10357)': < temba_client.v2.types.Flow
at
0x7fcf080a4510 >,
u'Single Message (10358)': < temba_client.v2.types.Flow
at
0x7fcf080a4450 >,
u'Single Message (10359)': < temba_client.v2.types.Flow
at
0x7fcf080a4390 >,
u'Single Message (10360)': < temba_client.v2.types.Flow
at
0x7fcf080a42d0 >,
u'Single Message (10361)': < temba_client.v2.types.Flow
at
0x7fcf080a4210 >,
u'Single Message (10362)': < temba_client.v2.types.Flow
at
0x7fcf080a4150 >,
u'Single Message (10363)': < temba_client.v2.types.Flow
at
0x7fcf080a4090 >,
u'Single Message (10364)': < temba_client.v2.types.Flow
at
0x7fcf080a0f90 >,
u'Single Message (10365)': < temba_client.v2.types.Flow
at
0x7fcf080a0ed0 >,
u'Single Message (10366)': < temba_client.v2.types.Flow
at
0x7fcf080a0e10 >,
u'Single Message (10367)': < temba_client.v2.types.Flow
at
0x7fcf080a0d50 >,
u'Single Message (10368)': < temba_client.v2.types.Flow
at
0x7fcf080a0c90 >,
u'Single Message (10369)': < temba_client.v2.types.Flow
at
0x7fcf080a0bd0 >,
u'Single Message (10370)': < temba_client.v2.types.Flow
at
0x7fcf080a0b10 >,
u'Single Message (10371)': < temba_client.v2.types.Flow
at
0x7fcf080a0a50 >,
u'Single Message (10372)': < temba_client.v2.types.Flow
at
0x7fcf080a0990 >,
u'Single Message (10373)': < temba_client.v2.types.Flow
at
0x7fcf080a08d0 >,
u'Single Message (10374)': < temba_client.v2.types.Flow
at
0x7fcf080a0810 >,
u'Single Message (10375)': < temba_client.v2.types.Flow
at
0x7fcf080a0750 >,
u'Single Message (10376)': < temba_client.v2.types.Flow
at
0x7fcf080a0690 >,
u'Single Message (10377)': < temba_client.v2.types.Flow
at
0x7fcf080a05d0 >,
u'Single Message (10378)': < temba_client.v2.types.Flow
at
0x7fcf080a0510 >,
u'Single Message (10379)': < temba_client.v2.types.Flow
at
0x7fcf080a0450 >,
u'Single Message (10380)': < temba_client.v2.types.Flow
at
0x7fcf080a0390 >,
u'Single Message (10381)': < temba_client.v2.types.Flow
at
0x7fcf080a02d0 >,
u'Single Message (10382)': < temba_client.v2.types.Flow
at
0x7fcf080a0210 >,
u'Single Message (10383)': < temba_client.v2.types.Flow
at
0x7fcf080a0150 >,
u'Single Message (10384)': < temba_client.v2.types.Flow
at
0x7fcf080a0090 >,
u'Single Message (10385)': < temba_client.v2.types.Flow
at
0x7fcf0809cf90 >,
u'Single Message (10386)': < temba_client.v2.types.Flow
at
0x7fcf0809ced0 >,
u'Single Message (10387)': < temba_client.v2.types.Flow
at
0x7fcf0809ce10 >,
u'Single Message (10388)': < temba_client.v2.types.Flow
at
0x7fcf0809cd50 >,
u'Single Message (10389)': < temba_client.v2.types.Flow
at
0x7fcf0809cc90 >,
u'Single Message (10390)': < temba_client.v2.types.Flow
at
0x7fcf0809cbd0 >,
u'Single Message (10391)': < temba_client.v2.types.Flow
at
0x7fcf0809cb10 >,
u'Single Message (10392)': < temba_client.v2.types.Flow
at
0x7fcf0809ca50 >,
u'Single Message (10393)': < temba_client.v2.types.Flow
at
0x7fcf0809c990 >,
u'Single Message (10394)': < temba_client.v2.types.Flow
at
0x7fcf0809c8d0 >,
u'Single Message (10395)': < temba_client.v2.types.Flow
at
0x7fcf0809c810 >,
u'Single Message (10396)': < temba_client.v2.types.Flow
at
0x7fcf0809c750 >,
u'Single Message (10397)': < temba_client.v2.types.Flow
at
0x7fcf0809c690 >,
u'Single Message (10398)': < temba_client.v2.types.Flow
at
0x7fcf0809c5d0 >,
u'Single Message (10399)': < temba_client.v2.types.Flow
at
0x7fcf0809c510 >,
u'Single Message (10400)': < temba_client.v2.types.Flow
at
0x7fcf0809c450 >,
u'Single Message (10401)': < temba_client.v2.types.Flow
at
0x7fcf0809c390 >,
u'Single Message (10402)': < temba_client.v2.types.Flow
at
0x7fcf0809c2d0 >,
u'Single Message (10403)': < temba_client.v2.types.Flow
at
0x7fcf0809c210 >,
u'Single Message (10404)': < temba_client.v2.types.Flow
at
0x7fcf0809c150 >,
u'Single Message (10405)': < temba_client.v2.types.Flow
at
0x7fcf0809c090 >,
u'Single Message (10406)': < temba_client.v2.types.Flow
at
0x7fcf08098f90 >,
u'Single Message (10407)': < temba_client.v2.types.Flow
at
0x7fcf08098ed0 >,
u'Single Message (10408)': < temba_client.v2.types.Flow
at
0x7fcf08098e10 >,
u'Single Message (10409)': < temba_client.v2.types.Flow
at
0x7fcf08098d50 >,
u'Single Message (10410)': < temba_client.v2.types.Flow
at
0x7fcf08098c90 >,
u'Single Message (10411)': < temba_client.v2.types.Flow
at
0x7fcf08098bd0 >,
u'Single Message (10412)': < temba_client.v2.types.Flow
at
0x7fcf08098b10 >,
u'Single Message (10413)': < temba_client.v2.types.Flow
at
0x7fcf08098a50 >,
u'Single Message (10414)': < temba_client.v2.types.Flow
at
0x7fcf08098990 >,
u'Single Message (10415)': < temba_client.v2.types.Flow
at
0x7fcf080988d0 >,
u'Single Message (10416)': < temba_client.v2.types.Flow
at
0x7fcf08098810 >,
u'Single Message (10417)': < temba_client.v2.types.Flow
at
0x7fcf08098750 >,
u'Single Message (10418)': < temba_client.v2.types.Flow
at
0x7fcf08098690 >,
u'Single Message (10419)': < temba_client.v2.types.Flow
at
0x7fcf080985d0 >,
u'Single Message (10420)': < temba_client.v2.types.Flow
at
0x7fcf08098510 >,
u'Single Message (10421)': < temba_client.v2.types.Flow
at
0x7fcf08098450 >,
u'Single Message (10422)': < temba_client.v2.types.Flow
at
0x7fcf08098390 >,
u'Single Message (10423)': < temba_client.v2.types.Flow
at
0x7fcf080982d0 >,
u'Single Message (10424)': < temba_client.v2.types.Flow
at
0x7fcf08098210 >,
u'Single Message (10425)': < temba_client.v2.types.Flow
at
0x7fcf08098150 >,
u'Single Message (10426)': < temba_client.v2.types.Flow
at
0x7fcf08098090 >,
u'Single Message (10427)': < temba_client.v2.types.Flow
at
0x7fcf08093f90 >,
u'Single Message (10428)': < temba_client.v2.types.Flow
at
0x7fcf08093ed0 >,
u'Single Message (10429)': < temba_client.v2.types.Flow
at
0x7fcf08093e10 >,
u'Single Message (10430)': < temba_client.v2.types.Flow
at
0x7fcf08093d50 >,
u'Single Message (10431)': < temba_client.v2.types.Flow
at
0x7fcf08093c90 >,
u'Single Message (10432)': < temba_client.v2.types.Flow
at
0x7fcf08093bd0 >,
u'Single Message (10433)': < temba_client.v2.types.Flow
at
0x7fcf08093b10 >,
u'Single Message (10434)': < temba_client.v2.types.Flow
at
0x7fcf08093a50 >,
u'Single Message (10435)': < temba_client.v2.types.Flow
at
0x7fcf08093990 >,
u'Single Message (10436)': < temba_client.v2.types.Flow
at
0x7fcf080938d0 >,
u'Single Message (10437)': < temba_client.v2.types.Flow
at
0x7fcf08093810 >,
u'Single Message (10438)': < temba_client.v2.types.Flow
at
0x7fcf08093750 >,
u'Single Message (10439)': < temba_client.v2.types.Flow
at
0x7fcf08093690 >,
u'Single Message (10440)': < temba_client.v2.types.Flow
at
0x7fcf080935d0 >,
u'Single Message (10441)': < temba_client.v2.types.Flow
at
0x7fcf08093510 >,
u'Single Message (10442)': < temba_client.v2.types.Flow
at
0x7fcf08093450 >,
u'Single Message (10443)': < temba_client.v2.types.Flow
at
0x7fcf08093390 >,
u'Single Message (10444)': < temba_client.v2.types.Flow
at
0x7fcf080932d0 >,
u'Single Message (10445)': < temba_client.v2.types.Flow
at
0x7fcf08093210 >,
u'Single Message (10446)': < temba_client.v2.types.Flow
at
0x7fcf08093150 >,
u'Single Message (10447)': < temba_client.v2.types.Flow
at
0x7fcf08093090 >,
u'Single Message (10448)': < temba_client.v2.types.Flow
at
0x7fcf0808ff90 >,
u'Single Message (10449)': < temba_client.v2.types.Flow
at
0x7fcf0808fed0 >,
u'Single Message (10450)': < temba_client.v2.types.Flow
at
0x7fcf0808fe10 >,
u'Single Message (10451)': < temba_client.v2.types.Flow
at
0x7fcf0808fd50 >,
u'Single Message (10452)': < temba_client.v2.types.Flow
at
0x7fcf0808fc90 >,
u'Single Message (10453)': < temba_client.v2.types.Flow
at
0x7fcf0808fbd0 >,
u'Single Message (10454)': < temba_client.v2.types.Flow
at
0x7fcf0808fb10 >,
u'Single Message (10455)': < temba_client.v2.types.Flow
at
0x7fcf0808fa50 >,
u'Single Message (10456)': < temba_client.v2.types.Flow
at
0x7fcf0808f990 >,
u'Single Message (10457)': < temba_client.v2.types.Flow
at
0x7fcf0808f8d0 >,
u'Single Message (10458)': < temba_client.v2.types.Flow
at
0x7fcf0808f810 >,
u'Single Message (10459)': < temba_client.v2.types.Flow
at
0x7fcf0808f750 >,
u'Single Message (10460)': < temba_client.v2.types.Flow
at
0x7fcf0808f690 >,
u'Single Message (10461)': < temba_client.v2.types.Flow
at
0x7fcf0808f5d0 >,
u'Single Message (10462)': < temba_client.v2.types.Flow
at
0x7fcf0808f510 >,
u'Single Message (10463)': < temba_client.v2.types.Flow
at
0x7fcf0808f450 >,
u'Single Message (10464)': < temba_client.v2.types.Flow
at
0x7fcf0808f390 >,
u'Single Message (10465)': < temba_client.v2.types.Flow
at
0x7fcf0808f2d0 >,
u'Single Message (10466)': < temba_client.v2.types.Flow
at
0x7fcf0808f210 >,
u'Single Message (10467)': < temba_client.v2.types.Flow
at
0x7fcf0808f150 >,
u'Single Message (10468)': < temba_client.v2.types.Flow
at
0x7fcf0808f090 >,
u'Single Message (10469)': < temba_client.v2.types.Flow
at
0x7fcefb484f90 >,
u'Single Message (10470)': < temba_client.v2.types.Flow
at
0x7fcefb484ed0 >,
u'Single Message (14157)': < temba_client.v2.types.Flow
at
0x7fcefb483250 >,
u'Single Message (14159)': < temba_client.v2.types.Flow
at
0x7fcefb483190 >,
u'Test contact': < temba_client.v2.types.Flow
at
0x7fcefb4835d0 >,
u'Training on writing SMS': < temba_client.v2.types.Flow
at
0x7fcefb482110 >,
u'Use Trigger Word': < temba_client.v2.types.Flow
at
0x7fcefb4821d0 >,
u'Validate': < temba_client.v2.types.Flow
at
0x7fcefb483690 >,
u'mnchlgatt': < temba_client.v2.types.Flow
at
0x7fcefb484510 >,
u'mnchw lga nfp flow B': < temba_client.v2.types.Flow
at
0x7fcefb4845d0 >,
u'stockouttest': < temba_client.v2.types.Flow
at
0x7fcefb4825d0 >,
u'test': < temba_client.v2.types.Flow
at
0x7fcefb483310 >,
u'yvb': < temba_client.v2.types.Flow
at
0x7fcefb4842d0 >}

In[34]: {x.name: x for x in flows[0]}[u'IMAM Program']
Out[34]: < temba_client.v2.types.Flow
at
0x7fcefb483dd0 >

In[35]: f = {x.name: x for x in flows[0]}[u'IMAM Program']

In[36]: f.runs
Out[36]: < temba_client.v2.types.Runs
at
0x7fcefb483e10 >

In[37]: f.Runs == f.runs
Out[37]: False

In[38]: f.Runs.active
Out[38]: < temba_client.serialization.IntegerField
at
0x7fcf0c900790 >

In[39]: f.Runs.active?
Type: IntegerField
String
form: < temba_client.serialization.IntegerField
object
at
0x7fcf0c900790 >
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / serialization.py
Docstring: < no
docstring >

In[40]: f.Runs.active()
---------------------------------------------------------------------------
TypeError
Traceback(most
recent
call
last)
< ipython - input - 40 - a85b8391cabb > in < module > ()
----> 1
f.Runs.active()

TypeError: 'IntegerField'
object is not callable

In[41]: f.Runs.active
Out[41]: < temba_client.serialization.IntegerField
at
0x7fcf0c900790 >

In[42]: f.Runs.active.deserialize
Out[42]: < bound
method
IntegerField.deserialize
of < temba_client.serialization.IntegerField
object
at
0x7fcf0c900790 >>

In[43]: f.Runs.active.deserialize()
---------------------------------------------------------------------------
TypeError
Traceback(most
recent
call
last)
< ipython - input - 43 - 1
d1ca81f2917 > in < module > ()
----> 1
f.Runs.active.deserialize()

TypeError: deserialize()
takes
exactly
2
arguments(1
given)

In[44]: f.Runs.active.src

In[45]: f.Runs.active.optional
Out[45]: False

In[46]: f.Runs.active
Out[46]: < temba_client.serialization.IntegerField
at
0x7fcf0c900790 >

In[47]: f.runs.completed
Out[47]: 34784

In[48]: f.runs.active
Out[48]: 9

In[49]: f.runs.create
Out[49]: < bound
method
ABCMeta.create
of <


class 'temba_client.v2.types.Runs'>>


In[50]: a
Out[50]: < temba_client.clients.CursorIterator
at
0x7fcf080711d0 >

In[51]: client
Out[51]: < temba_client.v2.TembaClient
at
0x7fcf08081590 >

In[52]: client.get_runs
Out[52]: < bound
method
TembaClient.get_runs
of < temba_client.v2.TembaClient
object
at
0x7fcf08081590 >>

In[53]: client.get_runs?
Signature: client.get_runs(id=None, flow=None, contact=None, responded=None, before=None, after=None)
Docstring:
Gets
all
matching
flow
runs

:param
id: flow
run
id
:param
flow: flow
object or UUID
:param
contact: contact
object or UUID
:param
responded: whether
to
limit
results
to
runs
with responses
  :param
  datetime
  before: modified
  before
:param
datetime
after: modified
after
:return: flow
run
query
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / v2 / __init__.py
Type: instancemethod

In[54]: f
Out[54]: < temba_client.v2.types.Flow
at
0x7fcefb483dd0 >

In[55]: f.uuid
Out[55]: u'a9eed2f3-a92c-48dd-aa10-4f139b1171a4'

In[56]: client.get_runs(flow=f)
Out[56]: < temba_client.clients.CursorQuery
at
0x7fcf0810cbd0 >

In[57]: r = client.get_runs(flow=f).iterfetches()

In[58]: r
Out[58]: < temba_client.clients.CursorIterator
at
0x7fcf080c4690 >

In[59]: r.next()
Out[59]:
[ < temba_client.v2.types.Run
at
0x7fcf080c4c10 >,
< temba_client.v2.types.Run
at
0x7fcefa7ba9d0 >,
< temba_client.v2.types.Run
at
0x7fcefa711dd0 >,
< temba_client.v2.types.Run
at
0x7fcefa713d50 >,
< temba_client.v2.types.Run
at
0x7fcefa714990 >,
< temba_client.v2.types.Run
at
0x7fcefa716dd0 >,
< temba_client.v2.types.Run
at
0x7fcefa71d250 >,
< temba_client.v2.types.Run
at
0x7fcefa721690 >,
< temba_client.v2.types.Run
at
0x7fcefa725410 >,
< temba_client.v2.types.Run
at
0x7fcefa725810 >,
< temba_client.v2.types.Run
at
0x7fcefb389350 >,
< temba_client.v2.types.Run
at
0x7fcefb38d790 >,
< temba_client.v2.types.Run
at
0x7fcefb391bd0 >,
< temba_client.v2.types.Run
at
0x7fcefb398050 >,
< temba_client.v2.types.Run
at
0x7fcefb39c590 >,
< temba_client.v2.types.Run
at
0x7fcefb3a09d0 >,
< temba_client.v2.types.Run
at
0x7fcefb3a3e10 >,
< temba_client.v2.types.Run
at
0x7fcefb3ab310 >,
< temba_client.v2.types.Run
at
0x7fcefb3ae850 >,
< temba_client.v2.types.Run
at
0x7fcefb3b2c90 >,
< temba_client.v2.types.Run
at
0x7fcefb3b9110 >,
< temba_client.v2.types.Run
at
0x7fcefb3bd550 >,
< temba_client.v2.types.Run
at
0x7fcefb3c1990 >,
< temba_client.v2.types.Run
at
0x7fcefb3c4e50 >,
< temba_client.v2.types.Run
at
0x7fcefb34c3d0 >,
< temba_client.v2.types.Run
at
0x7fcefb350810 >,
< temba_client.v2.types.Run
at
0x7fcefb353c50 >,
< temba_client.v2.types.Run
at
0x7fcefb35b0d0 >,
< temba_client.v2.types.Run
at
0x7fcefb35e490 >,
< temba_client.v2.types.Run
at
0x7fcefb361850 >,
< temba_client.v2.types.Run
at
0x7fcefb366c90 >,
< temba_client.v2.types.Run
at
0x7fcefb36d110 >,
< temba_client.v2.types.Run
at
0x7fcefb371550 >,
< temba_client.v2.types.Run
at
0x7fcefb374990 >,
< temba_client.v2.types.Run
at
0x7fcefb378dd0 >,
< temba_client.v2.types.Run
at
0x7fcefb37f250 >,
< temba_client.v2.types.Run
at
0x7fcefb383690 >,
< temba_client.v2.types.Run
at
0x7fcefb386ad0 >,
< temba_client.v2.types.Run
at
0x7fcefb30e0d0 >,
< temba_client.v2.types.Run
at
0x7fcefb311510 >,
< temba_client.v2.types.Run
at
0x7fcefb3169d0 >,
< temba_client.v2.types.Run
at
0x7fcefb319f10 >,
< temba_client.v2.types.Run
at
0x7fcefb321390 >,
< temba_client.v2.types.Run
at
0x7fcefb3247d0 >,
< temba_client.v2.types.Run
at
0x7fcefb328c10 >,
< temba_client.v2.types.Run
at
0x7fcefb32f110 >,
< temba_client.v2.types.Run
at
0x7fcefb333650 >,
< temba_client.v2.types.Run
at
0x7fcefb336a90 >,
< temba_client.v2.types.Run
at
0x7fcefb33e110 >,
< temba_client.v2.types.Run
at
0x7fcefb341650 >,
< temba_client.v2.types.Run
at
0x7fcefb346a90 >,
< temba_client.v2.types.Run
at
0x7fcefb2c9ed0 >,
< temba_client.v2.types.Run
at
0x7fcefb2d1350 >,
< temba_client.v2.types.Run
at
0x7fcefb2d4790 >,
< temba_client.v2.types.Run
at
0x7fcefb2d78d0 >,
< temba_client.v2.types.Run
at
0x7fcefb2db810 >,
< temba_client.v2.types.Run
at
0x7fcefb2dfc50 >,
< temba_client.v2.types.Run
at
0x7fcefb2e60d0 >,
< temba_client.v2.types.Run
at
0x7fcefb2ea510 >,
< temba_client.v2.types.Run
at
0x7fcefb2ee4d0 >,
< temba_client.v2.types.Run
at
0x7fcefb2f1110 >,
< temba_client.v2.types.Run
at
0x7fcefb2f5550 >,
< temba_client.v2.types.Run
at
0x7fcefb2f9990 >,
< temba_client.v2.types.Run
at
0x7fcefb2fcdd0 >,
< temba_client.v2.types.Run
at
0x7fcefb304250 >,
< temba_client.v2.types.Run
at
0x7fcefb307710 >,
< temba_client.v2.types.Run
at
0x7fcefb28bc50 >,
< temba_client.v2.types.Run
at
0x7fcefb2920d0 >,
< temba_client.v2.types.Run
at
0x7fcefb296510 >,
< temba_client.v2.types.Run
at
0x7fcefb29aad0 >,
< temba_client.v2.types.Run
at
0x7fcefb2a1050 >,
< temba_client.v2.types.Run
at
0x7fcefb2a5490 >,
< temba_client.v2.types.Run
at
0x7fcefb2a98d0 >,
< temba_client.v2.types.Run
at
0x7fcefb2acd10 >,
< temba_client.v2.types.Run
at
0x7fcefb2b4190 >,
< temba_client.v2.types.Run
at
0x7fcefb2b7290 >,
< temba_client.v2.types.Run
at
0x7fcefb2bc150 >,
< temba_client.v2.types.Run
at
0x7fcefb2bf510 >,
< temba_client.v2.types.Run
at
0x7fcefb2c2950 >,
< temba_client.v2.types.Run
at
0x7fcefb2c6d90 >,
< temba_client.v2.types.Run
at
0x7fcefb24d290 >,
< temba_client.v2.types.Run
at
0x7fcefb2512d0 >,
< temba_client.v2.types.Run
at
0x7fcefb251dd0 >,
< temba_client.v2.types.Run
at
0x7fcefb259250 >,
< temba_client.v2.types.Run
at
0x7fcefb25c710 >,
< temba_client.v2.types.Run
at
0x7fcefb260c50 >,
< temba_client.v2.types.Run
at
0x7fcefb2670d0 >,
< temba_client.v2.types.Run
at
0x7fcefb26b610 >,
< temba_client.v2.types.Run
at
0x7fcefb26fb50 >,
< temba_client.v2.types.Run
at
0x7fcefb272f90 >,
< temba_client.v2.types.Run
at
0x7fcefb27a410 >,
< temba_client.v2.types.Run
at
0x7fcefb27d310 >,
< temba_client.v2.types.Run
at
0x7fcefb27de10 >,
< temba_client.v2.types.Run
at
0x7fcefb285290 >,
< temba_client.v2.types.Run
at
0x7fcefb2086d0 >,
< temba_client.v2.types.Run
at
0x7fcefb20cb10 >,
< temba_client.v2.types.Run
at
0x7fcefb210f50 >,
< temba_client.v2.types.Run
at
0x7fcefb214ed0 >,
< temba_client.v2.types.Run
at
0x7fcefb217b10 >,
< temba_client.v2.types.Run
at
0x7fcefb21f090 >,
< temba_client.v2.types.Run
at
0x7fcefb222550 >,
< temba_client.v2.types.Run
at
0x7fcefb226a90 >,
< temba_client.v2.types.Run
at
0x7fcefb22aed0 >,
< temba_client.v2.types.Run
at
0x7fcefb232350 >,
< temba_client.v2.types.Run
at
0x7fcefb235790 >,
< temba_client.v2.types.Run
at
0x7fcefb238bd0 >,
< temba_client.v2.types.Run
at
0x7fcefb240050 >,
< temba_client.v2.types.Run
at
0x7fcefb243490 >,
< temba_client.v2.types.Run
at
0x7fcefb2478d0 >,
< temba_client.v2.types.Run
at
0x7fcefb1cbd10 >,
< temba_client.v2.types.Run
at
0x7fcefb1d2190 >,
< temba_client.v2.types.Run
at
0x7fcefb1d65d0 >,
< temba_client.v2.types.Run
at
0x7fcefb1daa10 >,
< temba_client.v2.types.Run
at
0x7fcefb1dde50 >,
< temba_client.v2.types.Run
at
0x7fcefb1e54d0 >,
< temba_client.v2.types.Run
at
0x7fcefb1e8810 >,
< temba_client.v2.types.Run
at
0x7fcefb1ec750 >,
< temba_client.v2.types.Run
at
0x7fcefb1f0b90 >,
< temba_client.v2.types.Run
at
0x7fcefb1f3fd0 >,
< temba_client.v2.types.Run
at
0x7fcefb1f7f10 >,
< temba_client.v2.types.Run
at
0x7fcefb1fbad0 >,
< temba_client.v2.types.Run
at
0x7fcefb1fef90 >,
< temba_client.v2.types.Run
at
0x7fcefb206510 >,
< temba_client.v2.types.Run
at
0x7fcefb18a950 >,
< temba_client.v2.types.Run
at
0x7fcefb18df10 >,
< temba_client.v2.types.Run
at
0x7fcefb195390 >,
< temba_client.v2.types.Run
at
0x7fcefb198850 >,
< temba_client.v2.types.Run
at
0x7fcefb19bd90 >,
< temba_client.v2.types.Run
at
0x7fcefb1a3210 >,
< temba_client.v2.types.Run
at
0x7fcefb1a76d0 >,
< temba_client.v2.types.Run
at
0x7fcefb1abc10 >,
< temba_client.v2.types.Run
at
0x7fcefb1b2190 >,
< temba_client.v2.types.Run
at
0x7fcefb1b6650 >,
< temba_client.v2.types.Run
at
0x7fcefb1b9c10 >,
< temba_client.v2.types.Run
at
0x7fcefb1bdad0 >,
< temba_client.v2.types.Run
at
0x7fcefb1c1490 >,
< temba_client.v2.types.Run
at
0x7fcefb1c59d0 >,
< temba_client.v2.types.Run
at
0x7fcefb148e10 >,
< temba_client.v2.types.Run
at
0x7fcefb150290 >,
< temba_client.v2.types.Run
at
0x7fcefb1536d0 >,
< temba_client.v2.types.Run
at
0x7fcefb156b10 >,
< temba_client.v2.types.Run
at
0x7fcefb15bf50 >,
< temba_client.v2.types.Run
at
0x7fcefb1623d0 >,
< temba_client.v2.types.Run
at
0x7fcefb166810 >,
< temba_client.v2.types.Run
at
0x7fcefb169c50 >,
< temba_client.v2.types.Run
at
0x7fcefb171150 >,
< temba_client.v2.types.Run
at
0x7fcefb174690 >,
< temba_client.v2.types.Run
at
0x7fcefb178ad0 >,
< temba_client.v2.types.Run
at
0x7fcefb17bf10 >,
< temba_client.v2.types.Run
at
0x7fcefb183390 >,
< temba_client.v2.types.Run
at
0x7fcefb1867d0 >,
< temba_client.v2.types.Run
at
0x7fcefb10bc90 >,
< temba_client.v2.types.Run
at
0x7fcefb111210 >,
< temba_client.v2.types.Run
at
0x7fcefb116650 >,
< temba_client.v2.types.Run
at
0x7fcefb119a90 >,
< temba_client.v2.types.Run
at
0x7fcefb11ded0 >,
< temba_client.v2.types.Run
at
0x7fcefb124350 >,
< temba_client.v2.types.Run
at
0x7fcefb128790 >,
< temba_client.v2.types.Run
at
0x7fcefb12bc50 >,
< temba_client.v2.types.Run
at
0x7fcefb1331d0 >,
< temba_client.v2.types.Run
at
0x7fcefb136610 >,
< temba_client.v2.types.Run
at
0x7fcefb13bad0 >,
< temba_client.v2.types.Run
at
0x7fcefb141050 >,
< temba_client.v2.types.Run
at
0x7fcefb141d90 >,
< temba_client.v2.types.Run
at
0x7fcefb146750 >,
< temba_client.v2.types.Run
at
0x7fcefb0c9c90 >,
< temba_client.v2.types.Run
at
0x7fcefb0d1110 >,
< temba_client.v2.types.Run
at
0x7fcefb0d4550 >,
< temba_client.v2.types.Run
at
0x7fcefb0d8990 >,
< temba_client.v2.types.Run
at
0x7fcefb0dbdd0 >,
< temba_client.v2.types.Run
at
0x7fcefb0e3250 >,
< temba_client.v2.types.Run
at
0x7fcefb0e7690 >,
< temba_client.v2.types.Run
at
0x7fcefb0eaad0 >,
< temba_client.v2.types.Run
at
0x7fcefb0ee990 >,
< temba_client.v2.types.Run
at
0x7fcefb0f14d0 >,
< temba_client.v2.types.Run
at
0x7fcefb0f6a10 >,
< temba_client.v2.types.Run
at
0x7fcefb0f9b10 >,
< temba_client.v2.types.Run
at
0x7fcefb0fca50 >,
< temba_client.v2.types.Run
at
0x7fcefb101f90 >,
< temba_client.v2.types.Run
at
0x7fcefb104f90 >,
< temba_client.v2.types.Run
at
0x7fcefb107c50 >,
< temba_client.v2.types.Run
at
0x7fcefb08f0d0 >,
< temba_client.v2.types.Run
at
0x7fcefb093510 >,
< temba_client.v2.types.Run
at
0x7fcefb097950 >,
< temba_client.v2.types.Run
at
0x7fcefb09ae10 >,
< temba_client.v2.types.Run
at
0x7fcefb0a2390 >,
< temba_client.v2.types.Run
at
0x7fcefb0a5850 >,
< temba_client.v2.types.Run
at
0x7fcefb0a9d90 >,
< temba_client.v2.types.Run
at
0x7fcefb0b1210 >,
< temba_client.v2.types.Run
at
0x7fcefb0b4650 >,
< temba_client.v2.types.Run
at
0x7fcefb0b7a90 >,
< temba_client.v2.types.Run
at
0x7fcefb0bced0 >,
< temba_client.v2.types.Run
at
0x7fcefb0c2350 >,
< temba_client.v2.types.Run
at
0x7fcefb0c6790 >,
< temba_client.v2.types.Run
at
0x7fcefb04abd0 >,
< temba_client.v2.types.Run
at
0x7fcefb052050 >,
< temba_client.v2.types.Run
at
0x7fcefb055490 >,
< temba_client.v2.types.Run
at
0x7fcefb0598d0 >,
< temba_client.v2.types.Run
at
0x7fcefb05cd10 >,
< temba_client.v2.types.Run
at
0x7fcefb064190 >,
< temba_client.v2.types.Run
at
0x7fcefb067550 >,
< temba_client.v2.types.Run
at
0x7fcefb06c910 >,
< temba_client.v2.types.Run
at
0x7fcefb06fd50 >,
< temba_client.v2.types.Run
at
0x7fcefb077090 >,
< temba_client.v2.types.Run
at
0x7fcefb07a3d0 >,
< temba_client.v2.types.Run
at
0x7fcefb07d810 >,
< temba_client.v2.types.Run
at
0x7fcefb0819d0 >,
< temba_client.v2.types.Run
at
0x7fcefb085a10 >,
< temba_client.v2.types.Run
at
0x7fcefb009ed0 >,
< temba_client.v2.types.Run
at
0x7fcefb010450 >,
< temba_client.v2.types.Run
at
0x7fcefb014890 >,
< temba_client.v2.types.Run
at
0x7fcefb017cd0 >,
< temba_client.v2.types.Run
at
0x7fcefb01f150 >,
< temba_client.v2.types.Run
at
0x7fcefb01ffd0 >,
< temba_client.v2.types.Run
at
0x7fcefb022510 >,
< temba_client.v2.types.Run
at
0x7fcefb027050 >,
< temba_client.v2.types.Run
at
0x7fcefb02a490 >,
< temba_client.v2.types.Run
at
0x7fcefb02d550 >,
< temba_client.v2.types.Run
at
0x7fcefb032390 >,
< temba_client.v2.types.Run
at
0x7fcefb0357d0 >,
< temba_client.v2.types.Run
at
0x7fcefb038c10 >,
< temba_client.v2.types.Run
at
0x7fcefb040090 >,
< temba_client.v2.types.Run
at
0x7fcefb0444d0 >,
< temba_client.v2.types.Run
at
0x7fcefb047910 >,
< temba_client.v2.types.Run
at
0x7fcefafcb6d0 >,
< temba_client.v2.types.Run
at
0x7fcefafcbfd0 >,
< temba_client.v2.types.Run
at
0x7fcefafd34d0 >,
< temba_client.v2.types.Run
at
0x7fcefafd6510 >,
< temba_client.v2.types.Run
at
0x7fcefafda050 >,
< temba_client.v2.types.Run
at
0x7fcefafdd490 >,
< temba_client.v2.types.Run
at
0x7fcefafe28d0 >,
< temba_client.v2.types.Run
at
0x7fcefafe5d90 >,
< temba_client.v2.types.Run
at
0x7fcefafed310 >,
< temba_client.v2.types.Run
at
0x7fcefaff0750 >,
< temba_client.v2.types.Run
at
0x7fcefaff3b90 >,
< temba_client.v2.types.Run
at
0x7fcefaff8fd0 >,
< temba_client.v2.types.Run
at
0x7fcefafff450 >,
< temba_client.v2.types.Run
at
0x7fcefb002890 >,
< temba_client.v2.types.Run
at
0x7fcefb006cd0 >,
< temba_client.v2.types.Run
at
0x7fcefaf8d150 >,
< temba_client.v2.types.Run
at
0x7fcefaf91590 >,
< temba_client.v2.types.Run
at
0x7fcefaf959d0 >,
< temba_client.v2.types.Run
at
0x7fcefaf98e10 >,
< temba_client.v2.types.Run
at
0x7fcefafa0290 >,
< temba_client.v2.types.Run
at
0x7fcefafa36d0 >,
< temba_client.v2.types.Run
at
0x7fcefafa7a90 >,
< temba_client.v2.types.Run
at
0x7fcefafabe50 >,
< temba_client.v2.types.Run
at
0x7fcefafb32d0 >,
< temba_client.v2.types.Run
at
0x7fcefafb6690 >,
< temba_client.v2.types.Run
at
0x7fcefafbab50 >]

In[60]: runs = _

In[61]: run = runs[0]

In[62]: run
Out[62]: < temba_client.v2.types.Run
at
0x7fcf080c4c10 >

In[63]: run.values()
---------------------------------------------------------------------------
TypeError
Traceback(most
recent
call
last)
< ipython - input - 63 - 7
fdfce13bb22 > in < module > ()
----> 1
run.values()

TypeError: 'dict'
object is not callable

In[64]: run.values
Out[64]:
{u'amar_o': < temba_client.v2.types.Value
at
0x7fcefb43c590 >,
u'beg_o': < temba_client.v2.types.Value
at
0x7fcefb43c4d0 >,
u'confirm': < temba_client.v2.types.Value
at
0x7fcf080c2c50 >,
u'dcur_o': < temba_client.v2.types.Value
at
0x7fcefb43c5d0 >,
u'dead_o': < temba_client.v2.types.Value
at
0x7fcefb43c490 >,
u'defu_o': < temba_client.v2.types.Value
at
0x7fcf080c2250 >,
u'dmed_o': < temba_client.v2.types.Value
at
0x7fcefa7ba890 >,
u'msg_routing': < temba_client.v2.types.Value
at
0x7fcefa7ba910 >,
u'role': < temba_client.v2.types.Value
at
0x7fcefb43c450 >,
u'tin_o': < temba_client.v2.types.Value
at
0x7fcefb43c350 >,
u'tout_o': < temba_client.v2.types.Value
at
0x7fcf080c29d0 >,
u'type': < temba_client.v2.types.Value
at
0x7fcefa7ba810 >,
u'weeknum': < temba_client.v2.types.Value
at
0x7fcefb43c110 >}

In[65]: run.contact
Out[65]: < temba_client.v2.types.ObjectRef
at
0x7fcf080c4190 >

In[66]: run.contact.uuid
Out[66]: u'e39d3459-2e1e-40c3-b9c4-1c5df51d937f'

In[67]:

In[67]: run
Out[67]: < temba_client.v2.types.Run
at
0x7fcf080c4c10 >

In[68]: run.path
Out[68]:
[ < temba_client.v2.types.Step
at
0x7fcefa7baa10 >,
< temba_client.v2.types.Step
at
0x7fcefa7baa90 >,
< temba_client.v2.types.Step
at
0x7fcefa7bab10 >,
< temba_client.v2.types.Step
at
0x7fcefa7bab90 >,
< temba_client.v2.types.Step
at
0x7fcefa7bac10 >,
< temba_client.v2.types.Step
at
0x7fcefa7bac90 >,
< temba_client.v2.types.Step
at
0x7fcefa7bad10 >,
< temba_client.v2.types.Step
at
0x7fcefa7bad90 >,
< temba_client.v2.types.Step
at
0x7fcefa7bae10 >,
< temba_client.v2.types.Step
at
0x7fcefa7bae90 >,
< temba_client.v2.types.Step
at
0x7fcefa7baf10 >,
< temba_client.v2.types.Step
at
0x7fcefa7baf90 >,
< temba_client.v2.types.Step
at
0x7fcefa711050 >,
< temba_client.v2.types.Step
at
0x7fcefa7110d0 >,
< temba_client.v2.types.Step
at
0x7fcefa711150 >,
< temba_client.v2.types.Step
at
0x7fcefa7111d0 >,
< temba_client.v2.types.Step
at
0x7fcefa711250 >,
< temba_client.v2.types.Step
at
0x7fcefa7112d0 >,
< temba_client.v2.types.Step
at
0x7fcefa711350 >,
< temba_client.v2.types.Step
at
0x7fcefa7113d0 >,
< temba_client.v2.types.Step
at
0x7fcefa711450 >,
< temba_client.v2.types.Step
at
0x7fcefa7114d0 >,
< temba_client.v2.types.Step
at
0x7fcefa711550 >,
< temba_client.v2.types.Step
at
0x7fcefa7115d0 >]

In[69]: run.responded
Out[69]: True

In[70]: run.Value
Out[70]: temba_client.v2.types.Value

In[71]: run.Value.category
Out[71]: < temba_client.serialization.SimpleField
at
0x7fcf08191ad0 >

In[72]: run[]
File
"<ipython-input-72-5d42cca09709>", line
1
run[]
^
SyntaxError: invalid
syntax

In[73]: run['']
---------------------------------------------------------------------------
TypeError
Traceback(most
recent
call
last)
< ipython - input - 73 - 40
a63f52b260 > in < module > ()
----> 1
run['']

TypeError: 'Run'
object
has
no
attribute
'__getitem__'

In[74]: run.values
Out[74]:
{u'amar_o': < temba_client.v2.types.Value
at
0x7fcefb43c590 >,
u'beg_o': < temba_client.v2.types.Value
at
0x7fcefb43c4d0 >,
u'confirm': < temba_client.v2.types.Value
at
0x7fcf080c2c50 >,
u'dcur_o': < temba_client.v2.types.Value
at
0x7fcefb43c5d0 >,
u'dead_o': < temba_client.v2.types.Value
at
0x7fcefb43c490 >,
u'defu_o': < temba_client.v2.types.Value
at
0x7fcf080c2250 >,
u'dmed_o': < temba_client.v2.types.Value
at
0x7fcefa7ba890 >,
u'msg_routing': < temba_client.v2.types.Value
at
0x7fcefa7ba910 >,
u'role': < temba_client.v2.types.Value
at
0x7fcefb43c450 >,
u'tin_o': < temba_client.v2.types.Value
at
0x7fcefb43c350 >,
u'tout_o': < temba_client.v2.types.Value
at
0x7fcf080c29d0 >,
u'type': < temba_client.v2.types.Value
at
0x7fcefa7ba810 >,
u'weeknum': < temba_client.v2.types.Value
at
0x7fcefb43c110 >}

In[75]: run.values['amar_o']
Out[75]: < temba_client.v2.types.Value
at
0x7fcefb43c590 >

In[76]: amar = run.values['amar_o']

In[77]: amar.value
Out[77]: 0.0

In[78]: amar.category
Out[78]: u'0 - 9999'

In[79]: amar.node
Out[79]: u'e7d96279-b9fb-4ed6-8d0f-85fca4ed272d'

In[80]: amar.deserialize
Out[80]: < bound
method
ABCMeta.deserialize
of <


class 'temba_client.v2.types.Value'>>


In[81]: amar.deserialize?
Signature: amar.deserialize(item)
Docstring: < no
docstring >
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / serialization.py
Type: instancemethod

In[82]: amar.time
Out[82]: datetime.datetime(2017, 4, 10, 13, 7, 18, 683588, tzinfo= < UTC >)

In[83]: run.exit_type
Out[83]: u'completed'

In[84]: run.contact
Out[84]: < temba_client.v2.types.ObjectRef
at
0x7fcf080c4190 >

In[85]: client.get_contacts()
Out[85]: < temba_client.clients.CursorQuery
at
0x7fcefa7baad0 >

In[86]: client.get_contacts(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True).next()
Out[86]:
[ < temba_client.v2.types.Contact
at
0x7fcefa713310 >,
< temba_client.v2.types.Contact
at
0x7fcf080c4a10 >,
< temba_client.v2.types.Contact
at
0x7fcefa714110 >,
< temba_client.v2.types.Contact
at
0x7fcefa714e90 >,
< temba_client.v2.types.Contact
at
0x7fcefb32b890 >,
< temba_client.v2.types.Contact
at
0x7fcefb3339d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb333e50 >,
< temba_client.v2.types.Contact
at
0x7fcefb3333d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb333050 >,
< temba_client.v2.types.Contact
at
0x7fcefb32f410 >,
< temba_client.v2.types.Contact
at
0x7fcefb32f890 >,
< temba_client.v2.types.Contact
at
0x7fcefb32fc10 >,
< temba_client.v2.types.Contact
at
0x7fcefb32fe50 >,
< temba_client.v2.types.Contact
at
0x7fcefb336c90 >,
< temba_client.v2.types.Contact
at
0x7fcefb336f90 >,
< temba_client.v2.types.Contact
at
0x7fcefb336790 >,
< temba_client.v2.types.Contact
at
0x7fcefb336350 >,
< temba_client.v2.types.Contact
at
0x7fcefb33a350 >,
< temba_client.v2.types.Contact
at
0x7fcefb33a750 >,
< temba_client.v2.types.Contact
at
0x7fcefb33ad50 >,
< temba_client.v2.types.Contact
at
0x7fcefb33a910 >,
< temba_client.v2.types.Contact
at
0x7fcefb341950 >,
< temba_client.v2.types.Contact
at
0x7fcefb341dd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb3414d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb3410d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb33e490 >,
< temba_client.v2.types.Contact
at
0x7fcefb33e910 >,
< temba_client.v2.types.Contact
at
0x7fcefb33ed10 >,
< temba_client.v2.types.Contact
at
0x7fcefb346090 >,
< temba_client.v2.types.Contact
at
0x7fcefb346c10 >,
< temba_client.v2.types.Contact
at
0x7fcefb346f90 >,
< temba_client.v2.types.Contact
at
0x7fcefb346710 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c90d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c95d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c9d50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c9950 >,
< temba_client.v2.types.Contact
at
0x7fcefb2cc290 >,
< temba_client.v2.types.Contact
at
0x7fcefb2cc690 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ccb10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ccbd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d4b90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d4e10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d4610 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d4210 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d15d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d19d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d1dd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d11d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d71d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d7ad0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d7ed0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2d76d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2dba10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2dbe90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2db590 >,
< temba_client.v2.types.Contact
at
0x7fcefb2db190 >,
< temba_client.v2.types.Contact
at
0x7fcefb2df250 >,
< temba_client.v2.types.Contact
at
0x7fcefb2dfed0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2df950 >,
< temba_client.v2.types.Contact
at
0x7fcefb2df5d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e3390 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e3810 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e3d10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e38d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ea910 >,
< temba_client.v2.types.Contact
at
0x7fcefb2eae10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ea310 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ea090 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e6550 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e69d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2e6fd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ee150 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ee8d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2eefd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2eeb50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f5750 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f5b50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f5f50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f51d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f1410 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f1790 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f1b10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f10d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f9110 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f9d10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f9810 >,
< temba_client.v2.types.Contact
at
0x7fcefb2f9390 >,
< temba_client.v2.types.Contact
at
0x7fcefb2fc250 >,
< temba_client.v2.types.Contact
at
0x7fcefb2fce50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2fcbd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2fc850 >,
< temba_client.v2.types.Contact
at
0x7fcefb301190 >,
< temba_client.v2.types.Contact
at
0x7fcefb301610 >,
< temba_client.v2.types.Contact
at
0x7fcefb301f90 >,
< temba_client.v2.types.Contact
at
0x7fcefb301c10 >,
< temba_client.v2.types.Contact
at
0x7fcefb307a10 >,
< temba_client.v2.types.Contact
at
0x7fcefb307c10 >,
< temba_client.v2.types.Contact
at
0x7fcefb3076d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb307290 >,
< temba_client.v2.types.Contact
at
0x7fcefb3044d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb3048d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb304cd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb304fd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb28b2d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb28bf50 >,
< temba_client.v2.types.Contact
at
0x7fcefb28b9d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb28b5d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb28f310 >,
< temba_client.v2.types.Contact
at
0x7fcefb28f810 >,
< temba_client.v2.types.Contact
at
0x7fcefb28fe10 >,
< temba_client.v2.types.Contact
at
0x7fcefb28fb90 >,
< temba_client.v2.types.Contact
at
0x7fcefb296690 >,
< temba_client.v2.types.Contact
at
0x7fcefb296a90 >,
< temba_client.v2.types.Contact
at
0x7fcefb296d10 >,
< temba_client.v2.types.Contact
at
0x7fcefb296410 >,
< temba_client.v2.types.Contact
at
0x7fcefb2921d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb292650 >,
< temba_client.v2.types.Contact
at
0x7fcefb292ad0 >,
< temba_client.v2.types.Contact
at
0x7fcefb292ed0 >,
< temba_client.v2.types.Contact
at
0x7fcefb29a250 >,
< temba_client.v2.types.Contact
at
0x7fcefb29ae50 >,
< temba_client.v2.types.Contact
at
0x7fcefb29aa90 >,
< temba_client.v2.types.Contact
at
0x7fcefb29a650 >,
< temba_client.v2.types.Contact
at
0x7fcefb29e110 >,
< temba_client.v2.types.Contact
at
0x7fcefb29e590 >,
< temba_client.v2.types.Contact
at
0x7fcefb29e810 >,
< temba_client.v2.types.Contact
at
0x7fcefb29ed10 >,
< temba_client.v2.types.Contact
at
0x7fcefb29e8d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a5810 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a5b90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a5450 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a5090 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a14d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a18d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a1ed0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a9a50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a9e50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a96d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2a9250 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ac310 >,
< temba_client.v2.types.Contact
at
0x7fcefb2acf90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ac990 >,
< temba_client.v2.types.Contact
at
0x7fcefb2ac550 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b03d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b07d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b0dd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b4210 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b4510 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b4990 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b4c90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b4ed0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b7690 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b7210 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b7e10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2b79d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bfa10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bfd90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bf290 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bc350 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bc7d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bccd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2bcd10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c2c50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c28d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c2450 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c6210 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c6e90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c6a90 >,
< temba_client.v2.types.Contact
at
0x7fcefb2c65d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb24a4d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb24a950 >,
< temba_client.v2.types.Contact
at
0x7fcefb24ac50 >,
< temba_client.v2.types.Contact
at
0x7fcefb24d610 >,
< temba_client.v2.types.Contact
at
0x7fcefb24da90 >,
< temba_client.v2.types.Contact
at
0x7fcefb24df10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2513d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb251090 >,
< temba_client.v2.types.Contact
at
0x7fcefb251c50 >,
< temba_client.v2.types.Contact
at
0x7fcefb2517d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb255310 >,
< temba_client.v2.types.Contact
at
0x7fcefb255710 >,
< temba_client.v2.types.Contact
at
0x7fcefb255e10 >,
< temba_client.v2.types.Contact
at
0x7fcefb25c790 >,
< temba_client.v2.types.Contact
at
0x7fcefb25cb90 >,
< temba_client.v2.types.Contact
at
0x7fcefb25cf90 >,
< temba_client.v2.types.Contact
at
0x7fcefb25c390 >,
< temba_client.v2.types.Contact
at
0x7fcefb2593d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2597d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb259bd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2590d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2601d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb260dd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb260950 >,
< temba_client.v2.types.Contact
at
0x7fcefb260510 >,
< temba_client.v2.types.Contact
at
0x7fcefb264390 >,
< temba_client.v2.types.Contact
at
0x7fcefb264790 >,
< temba_client.v2.types.Contact
at
0x7fcefb264d10 >,
< temba_client.v2.types.Contact
at
0x7fcefb2648d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb26ba10 >,
< temba_client.v2.types.Contact
at
0x7fcefb26be10 >,
< temba_client.v2.types.Contact
at
0x7fcefb26b410 >,
< temba_client.v2.types.Contact
at
0x7fcefb267150 >,
< temba_client.v2.types.Contact
at
0x7fcefb267550 >,
< temba_client.v2.types.Contact
at
0x7fcefb267950 >,
< temba_client.v2.types.Contact
at
0x7fcefb267d50 >,
< temba_client.v2.types.Contact
at
0x7fcefb26f050 >,
< temba_client.v2.types.Contact
at
0x7fcefb26fdd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb26f9d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb26f5d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb272390 >,
< temba_client.v2.types.Contact
at
0x7fcefb272f50 >,
< temba_client.v2.types.Contact
at
0x7fcefb272b10 >,
< temba_client.v2.types.Contact
at
0x7fcefb27a510 >,
< temba_client.v2.types.Contact
at
0x7fcefb27a910 >,
< temba_client.v2.types.Contact
at
0x7fcefb27ad90 >,
< temba_client.v2.types.Contact
at
0x7fcefb27a210 >,
< temba_client.v2.types.Contact
at
0x7fcefb2773d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb277850 >,
< temba_client.v2.types.Contact
at
0x7fcefb277f50 >,
< temba_client.v2.types.Contact
at
0x7fcefb27d410 >,
< temba_client.v2.types.Contact
at
0x7fcefb27d0d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb27db90 >,
< temba_client.v2.types.Contact
at
0x7fcefb27d6d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb2813d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb281850 >,
< temba_client.v2.types.Contact
at
0x7fcefb281dd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb208850 >,
< temba_client.v2.types.Contact
at
0x7fcefb208cd0 >,
< temba_client.v2.types.Contact
at
0x7fcefb208650 >,
< temba_client.v2.types.Contact
at
0x7fcefb208250 >,
< temba_client.v2.types.Contact
at
0x7fcefb285510 >,
< temba_client.v2.types.Contact
at
0x7fcefb285910 >,
< temba_client.v2.types.Contact
at
0x7fcefb285d90 >,
< temba_client.v2.types.Contact
at
0x7fcefb285ed0 >,
< temba_client.v2.types.Contact
at
0x7fcefb20cc90 >,
< temba_client.v2.types.Contact
at
0x7fcefb20ca10 >,
< temba_client.v2.types.Contact
at
0x7fcefb20c590 >,
< temba_client.v2.types.Contact
at
0x7fcefb210250 >,
< temba_client.v2.types.Contact
at
0x7fcefb2106d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb210c50 >,
< temba_client.v2.types.Contact
at
0x7fcefb210810 >,
< temba_client.v2.types.Contact
at
0x7fcefb214410 >,
< temba_client.v2.types.Contact
at
0x7fcefb214890 >,
< temba_client.v2.types.Contact
at
0x7fcefb214e90 >,
< temba_client.v2.types.Contact
at
0x7fcefb217190 >,
< temba_client.v2.types.Contact
at
0x7fcefb217e10 >,
< temba_client.v2.types.Contact
at
0x7fcefb217790 >,
< temba_client.v2.types.Contact
at
0x7fcefb217350 >,
< temba_client.v2.types.Contact
at
0x7fcefb21b3d0 >,
< temba_client.v2.types.Contact
at
0x7fcefb21b850 >]

In[87]: contacts = _

In[88]: contact = contacts[0]

In[89]: contact.fields
Out[89]:
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In[90]: contact.fields
Out[90]:
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In[91]: contact.uuid
Out[91]: u'c80583bd-5aff-4bc8-b309-0e8ac9d12479'

In[92]: contact.urns
Out[92]: [u'tel:+2347032791311']

In[93]: contact.name
Out[93]: u'Hassana Tijjani.'

In[94]: contact.groups
Out[94]:
[ < temba_client.v2.types.ObjectRef
at
0x7fcefa713cd0 >,
< temba_client.v2.types.ObjectRef
at
0x7fcf080c42d0 >,
< temba_client.v2.types.ObjectRef
at
0x7fcf080c4f50 >,
< temba_client.v2.types.ObjectRef
at
0x7fcf080c4f10 >,
< temba_client.v2.types.ObjectRef
at
0x7fcf080c4290 >]

In[95]: contact.groups[0].name
Out[95]: u'Imam Supervision 3'

In[96]: [x.name for x in contact.groups]
Out[96]:
[u'Imam Supervision 3',
 u'Imam Supervision 2',
 u'Imam Supervision',
 u'Nut Personnel',
 u'No_Email']

In[97]: contact.fields
Out[97]:
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In[98]: contact['siteid']
---------------------------------------------------------------------------
TypeError
Traceback(most
recent
call
last)
< ipython - input - 98 - 9
f055b55025f > in < module > ()
----> 1
contact['siteid']

TypeError: 'Contact'
object
has
no
attribute
'__getitem__'

In[99]: contact.modified_on
Out[99]: datetime.datetime(2017, 4, 10, 13, 29, 34, 733325, tzinfo= < UTC >)

In[100]: contact.blocked
Out[100]: False

In[101]: contact.created_on
Out[101]: datetime.datetime(2016, 10, 18, 10, 14, 22, 965210, tzinfo= < UTC >)

In[102]: contact.stopped
Out[102]: False

In[103]: [x.modified_on for x in contacts]
Out[103]:
[datetime.datetime(2017, 4, 10, 13, 29, 34, 733325, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 24, 39, 22642, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 23, 28, 157967, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 12, 13, 20334, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 8, 11, 246011, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 5, 31, 313794, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 5, 26, 130577, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 13, 2, 41, 403071, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 59, 24, 52737, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 54, 7, 389953, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 53, 26, 967967, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 45, 10, 956355, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 39, 0, 990799, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 34, 42, 879732, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 32, 29, 73858, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 30, 19, 619353, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 24, 43, 632993, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 19, 24, 798648, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 18, 31, 406092, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 9, 48, 226495, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 8, 39, 595412, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 7, 38, 35129, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 3, 51, 107139, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 12, 1, 2, 41705, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 58, 24, 493700, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 55, 56, 897560, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 55, 33, 516567, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 55, 31, 471392, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 46, 41, 749246, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 39, 45, 913606, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 34, 47, 262971, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 24, 3, 127398, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 23, 11, 245200, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 19, 17, 672190, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 12, 47, 195803, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 10, 19, 327148, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 9, 12, 424374, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 8, 41, 990604, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 8, 34, 969558, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 8, 20, 523525, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 5, 29, 45381, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 4, 59, 209844, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 3, 5, 560585, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 11, 3, 3, 778499, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 55, 57, 15334, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 50, 52, 686095, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 49, 51, 933727, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 49, 45, 778843, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 45, 50, 755188, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 43, 43, 606150, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 42, 8, 590985, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 40, 30, 985430, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 39, 11, 520445, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 35, 37, 297469, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 33, 12, 760354, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 33, 4, 998651, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 32, 11, 641670, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 30, 59, 735248, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 30, 50, 73395, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 30, 14, 46197, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 27, 43, 322779, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 21, 24, 883254, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 20, 57, 627703, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 18, 26, 544643, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 18, 17, 584914, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 11, 39, 789778, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 9, 6, 397865, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 9, 4, 888180, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 4, 32, 760361, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 3, 5, 315849, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 10, 0, 12, 732777, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 57, 29, 490055, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 54, 41, 7634, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 52, 9, 127164, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 51, 18, 798206, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 48, 5, 615075, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 45, 11, 782595, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 45, 9, 114235, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 43, 9, 14614, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 42, 21, 468033, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 40, 10, 346754, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 38, 59, 106838, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 38, 37, 250580, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 38, 2, 765500, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 35, 40, 172423, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 25, 34, 332909, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 25, 18, 673591, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 20, 48, 24292, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 20, 47, 60903, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 17, 47, 133589, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 8, 22, 37633, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 7, 32, 986512, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 4, 21, 944437, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 2, 50, 754904, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 9, 1, 38, 621827, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 59, 48, 110759, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 57, 27, 858135, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 55, 50, 825616, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 53, 51, 581696, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 53, 34, 667468, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 47, 7, 553334, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 47, 2, 71216, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 46, 14, 654694, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 45, 47, 230964, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 44, 50, 662894, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 43, 35, 350784, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 43, 12, 439249, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 43, 2, 829054, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 35, 4, 171866, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 32, 14, 134969, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 29, 3, 97238, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 28, 54, 573151, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 25, 33, 276962, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 24, 57, 250852, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 23, 44, 345818, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 20, 54, 350480, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 16, 15, 36531, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 15, 47, 285109, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 14, 57, 458684, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 13, 26, 767955, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 8, 10, 765436, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 8, 8, 676282, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 8, 0, 35, 216908, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 56, 48, 504629, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 55, 23, 715347, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 47, 31, 692825, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 46, 45, 144148, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 46, 32, 705010, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 45, 22, 652171, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 43, 53, 413971, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 43, 38, 153906, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 42, 40, 415121, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 42, 6, 529720, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 39, 6, 627174, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 37, 18, 875238, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 37, 5, 993362, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 34, 9, 203517, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 33, 23, 872978, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 29, 11, 941046, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 26, 8, 462349, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 25, 16, 319443, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 24, 43, 177741, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 23, 58, 776444, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 21, 43, 134846, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 21, 13, 234952, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 21, 4, 528832, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 19, 58, 5956, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 18, 26, 126834, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 18, 3, 757301, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 17, 59, 870291, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 17, 27, 65542, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 17, 20, 758320, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 16, 51, 6589, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 14, 15, 54254, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 14, 2, 899179, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 13, 37, 265466, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 12, 58, 321380, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 12, 22, 969622, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 12, 8, 621526, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 11, 17, 221421, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 57, 363217, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 56, 966955, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 56, 578649, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 56, 186560, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 55, 734180, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 55, 314767, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 54, 893626, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 54, 438539, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 53, 974102, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 53, 558753, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 53, 133586, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 52, 706024, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 52, 259585, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 51, 833960, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 51, 22952, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 50, 591972, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 50, 180044, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 49, 734170, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 49, 292573, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 48, 845548, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 48, 24259, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 47, 623641, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 47, 252853, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 46, 853165, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 46, 452201, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 46, 37672, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 45, 263415, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 44, 832950, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 44, 440459, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 44, 79124, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 43, 719060, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 43, 377551, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 43, 41515, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 42, 653992, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 42, 307254, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 41, 960441, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 41, 624434, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 41, 279888, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 40, 890721, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 40, 521337, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 40, 156620, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 39, 794800, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 39, 57439, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 38, 691737, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 38, 322579, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 37, 944877, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 37, 548028, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 37, 152318, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 36, 765609, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 36, 376909, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 35, 242258, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 34, 823014, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 34, 362452, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 33, 597438, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 33, 187567, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 32, 791591, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 32, 404515, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 31, 978100, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 31, 596969, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 31, 205290, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 30, 768318, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 30, 336367, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 29, 906100, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 29, 532664, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 28, 298495, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 27, 911607, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 27, 69840, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 26, 242759, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 25, 861918, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 25, 466123, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 25, 84413, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 24, 720629, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 24, 323318, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 23, 930925, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 23, 563498, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 23, 196903, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 22, 815309, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 22, 394346, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 22, 10046, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 21, 596527, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 20, 936375, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 20, 406766, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 19, 983933, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 19, 604938, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 19, 202415, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 18, 453483, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 17, 336536, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 16, 981366, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 16, 611103, tzinfo= < UTC >),
datetime.datetime(2017, 4, 10, 7, 10, 16, 151054, tzinfo= < UTC >)]

In[104]: contact.created_on
Out[104]: datetime.datetime(2016, 10, 18, 10, 14, 22, 965210, tzinfo= < UTC >)

In[105]: contact.fields
Out[105]:
{u'child_name': None,
 u'chw_number': None,
 u'date_last_program_report': None,
 u'date_last_stock_report': None,
 u'delivery_date': None,
 u'last_menses': None,
 u'level': u'Site',
 u'lga': u'Konduga',
 u'lga1mail': u'Hadiza Achi.',
 u'lga1name': u'Hadiza Achi.',
 u'lga1num': u'+2348029437389',
 u'mail': u'No.',
 u'mnp_designation': None,
 u'mnp_facility_lga': None,
 u'mnp_facility_name': None,
 u'mnp_facility_ward': None,
 u'mnp_fully_registered_date': None,
 u'mnp_hworker_state': None,
 u'mnp_low_stock': None,
 u'mnp_nfp_lga_name': None,
 u'mnp_state': None,
 u'mnp_stock_reg': None,
 u'mnp_subscription': None,
 u'mnps': None,
 u'phonesup': None,
 u'post': u'Community Health Officer',
 u'promiss': u'13',
 u'registration_date': u'18-10-2016',
 u'siteid': u'816110030',
 u'sitename': u'Gubio IDP Camp',
 u'sno1mail': u'no',
 u'sno1name': u'Hassana Suleiman Jibrin.',
 u'sno1num': u'+2348065476174',
 u'sno2mail': u'abdullahimadi@gmail.com',
 u'sno2name': u'Abdullahi Alhaji Madi.',
 u'sno2num': u'+2349090154070',
 u'sno3mail': u'ausman@unicef.org',
 u'sno3name': u'Aminu Usman Danzomo.',
 u'sno3num': u'+2348064275868',
 u'state': u'Borno',
 u'stock_out_item': None,
 u'stomiss': u'13',
 u'timer': None,
 u'type': u'OTP'}

In[106]:
from uuid import UUID

In[107]: contact.uuid
Out[107]: u'c80583bd-5aff-4bc8-b309-0e8ac9d12479'

In[108]: UUID(contact.uuid)
Out[108]: UUID('c80583bd-5aff-4bc8-b309-0e8ac9d12479')

In[109]: len(contact.uuid)
Out[109]: 36

In[110]: client.get_contacts(group='Nut Personnel')
Out[110]: < temba_client.clients.CursorQuery
at
0x7fcefb346d10 >

In[111]: client.get_contacts(group='Nut Personnel').count
---------------------------------------------------------------------------
AttributeError
Traceback(most
recent
call
last)
< ipython - input - 111 - f5131037d408 > in < module > ()
----> 1
client.get_contacts(group='Nut Personnel').count

AttributeError: 'CursorQuery'
object
has
no
attribute
'count'

In[112]: z = client.get_contacts(group='Nut Personnel')

In[113]: z.params
Out[113]: {'group': 'Nut Personnel'}

In[114]: z.url
Out[114]: u'https://rapidpro.io/api/v2/contacts.json'

In[115]: run
Out[115]: < temba_client.v2.types.Run
at
0x7fcf080c4c10 >

In[116]: run.fields
---------------------------------------------------------------------------
AttributeError
Traceback(most
recent
call
last)
< ipython - input - 116 - 8
cc90d7ac291 > in < module > ()
----> 1
run.fields

AttributeError: 'Run'
object
has
no
attribute
'fields'

In[117]: run.value
---------------------------------------------------------------------------
AttributeError
Traceback(most
recent
call
last)
< ipython - input - 117 - 4
aae7a3d1fa8 > in < module > ()
----> 1
run.value

AttributeError: 'Run'
object
has
no
attribute
'value'

In[118]: run.values
Out[118]:
{u'amar_o': < temba_client.v2.types.Value
at
0x7fcefb43c590 >,
u'beg_o': < temba_client.v2.types.Value
at
0x7fcefb43c4d0 >,
u'confirm': < temba_client.v2.types.Value
at
0x7fcf080c2c50 >,
u'dcur_o': < temba_client.v2.types.Value
at
0x7fcefb43c5d0 >,
u'dead_o': < temba_client.v2.types.Value
at
0x7fcefb43c490 >,
u'defu_o': < temba_client.v2.types.Value
at
0x7fcf080c2250 >,
u'dmed_o': < temba_client.v2.types.Value
at
0x7fcefa7ba890 >,
u'msg_routing': < temba_client.v2.types.Value
at
0x7fcefa7ba910 >,
u'role': < temba_client.v2.types.Value
at
0x7fcefb43c450 >,
u'tin_o': < temba_client.v2.types.Value
at
0x7fcefb43c350 >,
u'tout_o': < temba_client.v2.types.Value
at
0x7fcf080c29d0 >,
u'type': < temba_client.v2.types.Value
at
0x7fcefa7ba810 >,
u'weeknum': < temba_client.v2.types.Value
at
0x7fcefb43c110 >}


[1] + Stopped
ipython
(ve)
robert @ flybird: ~ / PycharmProjects / IMAM$ python
manage.py
inspectdb
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
  name = models.CharField(unique=True, max_length=80)

  class Meta:
    managed = False
    db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
  group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
  permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'auth_group_permissions'
    unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
  name = models.CharField(max_length=255)
  content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
  codename = models.CharField(max_length=100)

  class Meta:
    managed = False
    db_table = 'auth_permission'
    unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
  password = models.CharField(max_length=128)
  last_login = models.DateTimeField(blank=True, null=True)
  is_superuser = models.BooleanField()
  username = models.CharField(unique=True, max_length=150)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.CharField(max_length=254)
  is_staff = models.BooleanField()
  is_active = models.BooleanField()
  date_joined = models.DateTimeField()

  class Meta:
    managed = False
    db_table = 'auth_user'


class AuthUserGroups(models.Model):
  user = models.ForeignKey(AuthUser, models.DO_NOTHING)
  group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'auth_user_groups'
    unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
  user = models.ForeignKey(AuthUser, models.DO_NOTHING)
  permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'auth_user_user_permissions'
    unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
  action_time = models.DateTimeField()
  object_id = models.TextField(blank=True, null=True)
  object_repr = models.CharField(max_length=200)
  action_flag = models.SmallIntegerField()
  change_message = models.TextField()
  content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
  user = models.ForeignKey(AuthUser, models.DO_NOTHING)

  class Meta:
    managed = False
    db_table = 'django_admin_log'


class DjangoContentType(models.Model):
  app_label = models.CharField(max_length=100)
  model = models.CharField(max_length=100)

  class Meta:
    managed = False
    db_table = 'django_content_type'
    unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
  app = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  applied = models.DateTimeField()

  class Meta:
    managed = False
    db_table = 'django_migrations'


class DjangoSession(models.Model):
  session_key = models.CharField(primary_key=True, max_length=40)
  session_data = models.TextField()
  expire_date = models.DateTimeField()

  class Meta:
    managed = False
    db_table = 'django_session'


class FirstAdmin(models.Model):
  index = models.BigIntegerField(blank=True, null=True)
  state_num = models.BigIntegerField(primary_key=True)
  state = models.TextField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'first_admin'


class Program(models.Model):
  index = models.BigIntegerField(blank=True, null=True)
  contact_uuid = models.TextField(blank=True, null=True)
  urn = models.BigIntegerField()
  name = models.TextField(blank=True, null=True)
  groups = models.TextField(blank=True, null=True)
  siteid = models.BigIntegerField(blank=True, null=True)
  first_seen = models.DateTimeField()
  last_seen = models.DateTimeField(blank=True, null=True)
  weeknum = models.BigIntegerField(blank=True, null=True)
  role = models.TextField(blank=True, null=True)
  type = models.TextField(blank=True, null=True)
  age_group = models.TextField(blank=True, null=True)
  beg = models.TextField(blank=True, null=True)
  amar = models.BigIntegerField(blank=True, null=True)
  tin = models.TextField(blank=True, null=True)
  dcur = models.BigIntegerField(blank=True, null=True)
  dead = models.BigIntegerField(blank=True, null=True)
  defu = models.BigIntegerField(blank=True, null=True)
  dmed = models.BigIntegerField(blank=True, null=True)
  tout = models.BigIntegerField(blank=True, null=True)
  confirm = models.TextField(blank=True, null=True)
  siteid_lgt = models.BigIntegerField(blank=True, null=True)
  state_num = models.BigIntegerField(blank=True, null=True)
  lga_num = models.BigIntegerField(blank=True, null=True)
  year = models.BigIntegerField(blank=True, null=True)
  last_seen_weeknum = models.BigIntegerField(blank=True, null=True)
  rep_year_wn = models.TextField(blank=True, null=True)
  rep_weeknum = models.BigIntegerField(blank=True, null=True)
  last_seen_dotw = models.BigIntegerField(blank=True, null=True)
  last_seen_hour = models.BigIntegerField(blank=True, null=True)
  year_weeknum = models.TextField(blank=True, null=True)
  iso_rep_year_wn = models.TextField(blank=True, null=True)
  iso_year_weeknum = models.TextField(blank=True, null=True)
  iso_diff = models.BigIntegerField(blank=True, null=True)
  since_x_weeks = models.BigIntegerField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'program'
    unique_together = (('urn', 'first_seen'),)


class Registration(models.Model):
  index = models.BigIntegerField(blank=True, null=True)
  contact_uuid = models.TextField(blank=True, null=True)
  urn = models.TextField()
  name = models.TextField(blank=True, null=True)
  groups = models.TextField(blank=True, null=True)
  siteid = models.TextField(blank=True, null=True)
  type = models.TextField(blank=True, null=True)
  first_seen = models.DateTimeField(blank=True, null=True)
  last_seen = models.DateTimeField(blank=True, null=True)
  post = models.TextField(blank=True, null=True)
  mail = models.TextField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'registration'


class SecondAdmin(models.Model):
  index = models.BigIntegerField(blank=True, null=True)
  lga_num = models.BigIntegerField(primary_key=True)
  lga = models.TextField(blank=True, null=True)
  state_num = models.TextField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'second_admin'


class Site(models.Model):
  index = models.BigIntegerField(blank=True, null=True)
  siteid = models.BigIntegerField(primary_key=True)
  sitename = models.TextField(blank=True, null=True)
  state_num = models.TextField(blank=True, null=True)
  lga_num = models.TextField(blank=True, null=True)
  ward = models.TextField(blank=True, null=True)
  x_long = models.FloatField(blank=True, null=True)
  y_lat = models.FloatField(blank=True, null=True)
  notes = models.TextField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'site'


class Stock(models.Model):
  index = models.BigIntegerField(blank=True, null=True)
  contact_uuid = models.TextField(blank=True, null=True)
  urn = models.BigIntegerField()
  name = models.TextField(blank=True, null=True)
  groups = models.TextField(blank=True, null=True)
  siteid = models.BigIntegerField(blank=True, null=True)
  first_seen = models.DateTimeField()
  last_seen = models.DateTimeField(blank=True, null=True)
  weeknum = models.BigIntegerField(blank=True, null=True)
  level = models.TextField(blank=True, null=True)
  self_report = models.FloatField(blank=True, null=True)
  sto_siteid = models.FloatField(blank=True, null=True)
  sto_type = models.FloatField(blank=True, null=True)
  type = models.TextField(blank=True, null=True)
  rutf_in = models.TextField(blank=True, null=True)
  rutf_used_carton = models.TextField(blank=True, null=True)
  rutf_used_sachet = models.TextField(blank=True, null=True)
  rutf_bal_carton = models.BigIntegerField(blank=True, null=True)
  rutf_bal_sachet = models.BigIntegerField(blank=True, null=True)
  rutf_out = models.FloatField(blank=True, null=True)
  rutf_bal = models.FloatField(blank=True, null=True)
  f75_bal_carton = models.FloatField(blank=True, null=True)
  f75_bal_sachet = models.FloatField(blank=True, null=True)
  f100_bal_carton = models.FloatField(blank=True, null=True)
  f100_bal_sachet = models.FloatField(blank=True, null=True)
  confirm = models.TextField(blank=True, null=True)
  unique = models.FloatField(blank=True, null=True)
  siteid_lgt = models.BigIntegerField(blank=True, null=True)
  state_num = models.BigIntegerField(blank=True, null=True)
  lga_num = models.BigIntegerField(blank=True, null=True)
  year = models.BigIntegerField(blank=True, null=True)
  last_seen_weeknum = models.BigIntegerField(blank=True, null=True)
  rep_year_wn = models.TextField(blank=True, null=True)
  rep_weeknum = models.BigIntegerField(blank=True, null=True)
  last_seen_dotw = models.BigIntegerField(blank=True, null=True)
  last_seen_hour = models.BigIntegerField(blank=True, null=True)
  year_weeknum = models.TextField(blank=True, null=True)
  iso_rep_year_wn = models.TextField(blank=True, null=True)
  iso_year_weeknum = models.TextField(blank=True, null=True)
  iso_diff = models.BigIntegerField(blank=True, null=True)
  since_x_weeks = models.BigIntegerField(blank=True, null=True)

  class Meta:
    managed = False
    db_table = 'stock'
    unique_together = (('urn', 'first_seen'),)


(ve)
robert @ flybird: ~ / PycharmProjects / IMAM$ git
diff
:...
skipping...
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
:...
skipping...
diff - -git
a /.gitignore
b /.gitignore
index
290
a8cd.
.4
bf9447
100644
--- a /.gitignore
+++ b /.gitignore


@ @


-9, 3 + 9, 4 @ @ home / migrations / 0002
_auto_20170129_1727.py
posts_by_type
venv /
ve /
+token
diff - -git
a / home / management / commands / import_contacts.py
b / home / management / commands / import_contacts.py
index
e69de29.
.63
d106d
100644
--- a / home / management / commands / import_contacts.py
+++ b / home / management / commands / import_contacts.py


@ @


-0, 0 + 1, 39 @ @
+
from django.core.management.base import BaseCommand

+
from django.conf import settings

+
from temba_client.v2 import TembaClient

+
+
from home.models import Registration

+
+
from uuid import UUID

+
+  # to run python manage.py load_data
+
+  # STOCKS DATA
+
+


class Command(BaseCommand):
  +    help = 'Loads data to SQL for IMAM website'


+
+  # A command must define handle
+


def handle(self, *args, **options):
  +        client = TembaClient('rapidpro.io', open('token').read().strip())


+
+        a = 0
+
for contact_batch in client.get_contacts(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True):
  +
  for contact in contact_batch:
    +
  if Registration.objects.filter(contact_uuid=UUID(contact.uuid)).exists():
    +                    contact_in_db = Registration.objects.get(contact_uuid=UUID(contact.uuid))
+                else:
+                    contact_in_db = Registration()
+
+                contact_in_db.urn = contact.urns[0]
+                contact_in_db.name = contact.name
+                contact_in_db.siteid = contact.fields['siteid']
+                contact_in_db.type = contact.fields['type']
+                contact_in_db.last_seen = contact.modified_on
+                contact_in_db.post = contact.fields['post']
+                contact_in_db.mail = contact.fields['mail']
+
+                contact_in_db.save()
+
+                a += 1
+                print(a)
diff - -git
a / home / models.py
b / home / models.py
index
69
a1542..aee7de3
100644
--- a / home / models.py
+++ b / home / models.py


@ @


-10, 15 + 10, 16 @ @
from django.db import models


# Registration
class Registration(models.Model):
  index = models.BigIntegerField(primary_key=True)


-    contact_uuid = models.UUIDField(editable=False)
+  # contact_uuid = models.UUIDField(editable=False)
+    contact_uuid = models.CharField(editable=False, max_length=36, unique=True)
# problem to add phone number field to tools
# urn = models.PhoneNumberField()
-    urn = models.IntegerField(primary_key=True)
+    urn = models.CharField(max_length=50)
name = models.CharField(max_length=100)
groups = models.CharField(max_length=100)
siteid = models.IntegerField()
type = models.CharField(max_length=20)
-    first_seen = models.DateTimeField()
+    first_seen = models.DateTimeField(null=True, blank=True)
last_seen = models.DateTimeField()
post = models.CharField(max_length=30)
mail = models.EmailField()


@ @


-35, 40 + 36, 49 @ @


class Registration(models.Model):
  # Program data
  class Program(models.Model):


-    index = models.BigIntegerField(primary_key=True)
-    contact_uuid = models.UUIDField(editable=False)
-  # problem to add phone number field to tools
:
+                contact_in_db.name = contact.name
+                contact_in_db.siteid = contact.fields['siteid']
+                contact_in_db.type = contact.fields['type']
+                contact_in_db.last_seen = contact.modified_on
+                contact_in_db.post = contact.fields['post']
+                contact_in_db.mail = contact.fields['mail']
+
+                contact_in_db.save()
+
+                a += 1
+                print(a)
diff - -git
a / home / models.py
b / home / models.py
index
69
a1542..aee7de3
100644
--- a / home / models.py
+++ b / home / models.py


@ @


-10, 15 + 10, 16 @ @
from django.db import models


# Registration
class Registration(models.Model):
  index = models.BigIntegerField(primary_key=True)


-    contact_uuid = models.UUIDField(editable=False)
+  # contact_uuid = models.UUIDField(editable=False)
+    contact_uuid = models.CharField(editable=False, max_length=36, unique=True)
# problem to add phone number field to tools
# urn = models.PhoneNumberField()
-    urn = models.IntegerField(primary_key=True)
+    urn = models.CharField(max_length=50)
name = models.CharField(max_length=100)
groups = models.CharField(max_length=100)
siteid = models.IntegerField()
type = models.CharField(max_length=20)
-    first_seen = models.DateTimeField()
+    first_seen = models.DateTimeField(null=True, blank=True)
last_seen = models.DateTimeField()
post = models.CharField(max_length=30)
mail = models.EmailField()


@ @


-35, 40 + 36, 49 @ @


class Registration(models.Model):
  # Program data
  class Program(models.Model):


-    index = models.BigIntegerField(primary_key=True)
-    contact_uuid = models.UUIDField(editable=False)
:
diff - -git
a /.gitignore
b /.gitignore
index
290
a8cd.
.4
bf9447
100644
--- a /.gitignore
+++ b /.gitignore


@ @


-9, 3 + 9, 4 @ @ home / migrations / 0002
_auto_20170129_1727.py
posts_by_type
venv /
ve /
+token
diff - -git
a / home / management / commands / import_contacts.py
b / home / management / commands / import_contacts.py
index
e69de29.
.63
d106d
100644
--- a / home / management / commands / import_contacts.py
+++ b / home / management / commands / import_contacts.py


@ @


-0, 0 + 1, 39 @ @
+
from django.core.management.base import BaseCommand

+
from django.conf import settings

+
from temba_client.v2 import TembaClient

+
+
from home.models import Registration

+
+
from uuid import UUID

+
+  # to run python manage.py load_data
+
+  # STOCKS DATA
+
+


class Command(BaseCommand):
  +    help = 'Loads data to SQL for IMAM website'


+
+  # A command must define handle
+


def handle(self, *args, **options):
  +        client = TembaClient('rapidpro.io', open('token').read().strip())


+
+        a = 0
+
for contact_batch in client.get_contacts(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True):
  +
  for contact in contact_batch:
    +
  if Registration.objects.filter(contact_uuid=UUID(contact.uuid)).exists():
    +                    contact_in_db = Registration.objects.get(contact_uuid=UUID(contact.uuid))
+                else:
+                    contact_in_db = Registration()
+
+                contact_in_db.urn = contact.urns[0]
+                contact_in_db.name = contact.name
+                contact_in_db.siteid = contact.fields['siteid']
+                contact_in_db.type = contact.fields['type']
+                contact_in_db.last_seen = contact.modified_on
+                contact_in_db.post = contact.fields['post']
+                contact_in_db.mail = contact.fields['mail']
+
+                contact_in_db.save()
+
+                a += 1
+                print(a)
diff - -git
a / home / models.py
b / home / models.py
index
69
a1542..aee7de3
100644
--- a / home / models.py
+++ b / home / models.py


@ @


-10, 15 + 10, 16 @ @
from django.db import models


# Registration
class Registration(models.Model):
  index = models.BigIntegerField(primary_key=True)


-    contact_uuid = models.UUIDField(editable=False)
+  # contact_uuid = models.UUIDField(editable=False)
+    contact_uuid = models.CharField(editable=False, max_length=36, unique=True)
# problem to add phone number field to tools
# urn = models.PhoneNumberField()
-    urn = models.IntegerField(primary_key=True)
+    urn = models.CharField(max_length=50)
name = models.CharField(max_length=100)
groups = models.CharField(max_length=100)
siteid = models.IntegerField()
type = models.CharField(max_length=20)
-    first_seen = models.DateTimeField()
+    first_seen = models.DateTimeField(null=True, blank=True)
last_seen = models.DateTimeField()
post = models.CharField(max_length=30)
mail = models.EmailField()


@ @


-35, 40 + 36, 49 @ @


class Registration(models.Model):
  # Program data
  class Program(models.Model):


-    index = models.BigIntegerField(primary_key=True)
-    contact_uuid = models.UUIDField(editable=False)
-  # problem to add phone number field to tools
-  # urn = models.PhoneNumberField()
-    urn = models.IntegerField()
-    name = models.CharField(max_length=100)
-    groups = models.CharField(max_length=100)
-  # if supervisor enters the data than take SiteID from proSiteID
-    siteid = models.IntegerField()
+    index = models.BigIntegerField(blank=True, null=True)
+    contact_uuid = models.TextField(blank=True, null=True)
+    urn = models.BigIntegerField()
+    name = models.TextField(blank=True, null=True)
+    groups = models.TextField(blank=True, null=True)
+    siteid = models.BigIntegerField(blank=True, null=True)
first_seen = models.DateTimeField()
-    last_seen = models.DateTimeField()
-    weeknum = models.IntegerField()
-    role = models.CharField(max_length=20)
-  # if supervisor enters the data then take Type from proType
-    type = models.CharField(max_length=20)
-    age_group = models.CharField(max_length=20)
-  # Admissions and Exits
-  # if data entry is from SC then don't forget to add
-    beg = models.IntegerField()
-    amar = models.IntegerField()
-    tin = models.IntegerField()
-    tout = models.IntegerField()
-    dcur = models.IntegerField()
-    dead = models.IntegerField()
-    defu = models.IntegerField()
-    dmed = models.IntegerField()
-    confirm = models.CharField(max_length=20)
-  # if supervisor enters the data then take Type from proType
+    name = models.TextField(blank=True, null=True)
+    groups = models.TextField(blank=True, null=True)
+    siteid = models.BigIntegerField(blank=True, null=True)
first_seen = models.DateTimeField()
-    last_seen = models.DateTimeField()
-    weeknum = models.IntegerField()
-    role = models.CharField(max_length=20)
-  # if supervisor enters the data then take Type from proType


@ @


-10, 15 + 10, 16 @ @
from django.db import models


# Registration
class Registration(models.Model):
  index = models.BigIntegerField(primary_key=True)


-    contact_uuid = models.UUIDField(editable=False)
+  # contact_uuid = models.UUIDField(editable=False)
+    contact_uuid = models.CharField(editable=False, max_length=36, unique=True)
# problem to add phone number field to tools
# urn = models.PhoneNumberField()
-    urn = models.IntegerField(primary_key=True)
+    urn = models.CharField(max_length=50)
name = models.CharField(max_length=100)
groups = models.CharField(max_length=100)
siteid = models.IntegerField()
type = models.CharField(max_length=20)
-    first_seen = models.DateTimeField()
+    first_seen = models.DateTimeField(null=True, blank=True)
last_seen = models.DateTimeField()
post = models.CharField(max_length=30)
mail = models.EmailField()


@ @


-35, 40 + 36, 49 @ @


class Registration(models.Model):
  # Program data
  class Program(models.Model):


-    index = models.BigIntegerField(primary_key=True)
-    contact_uuid = models.UUIDField(editable=False)
-  # problem to add phone number field to tools
-  # urn = models.PhoneNumberField()
-    urn = models.IntegerField()
-    name = models.CharField(max_length=100)
-    groups = models.CharField(max_length=100)
-  # if supervisor enters the data than take SiteID from proSiteID
-    siteid = models.IntegerField()
+    index = models.BigIntegerField(blank=True, null=True)
+    contact_uuid = models.TextField(blank=True, null=True)
+    urn = models.BigIntegerField()
+    name = models.TextField(blank=True, null=True)
+    groups = models.TextField(blank=True, null=True)
+    siteid = models.BigIntegerField(blank=True, null=True)
first_seen = models.DateTimeField()
-    last_seen = models.DateTimeField()
-    weeknum = models.IntegerField()
(ve)
robert @ flybird: ~ / PycharmProjects / IMAM$ fg
ipython
In[119]:

In[119]: run.values
Out[119]:
{u'amar_o': < temba_client.v2.types.Value
at
0x7fcefb43c590 >,
u'beg_o': < temba_client.v2.types.Value
at
0x7fcefb43c4d0 >,
u'confirm': < temba_client.v2.types.Value
at
0x7fcf080c2c50 >,
u'dcur_o': < temba_client.v2.types.Value
at
0x7fcefb43c5d0 >,
u'dead_o': < temba_client.v2.types.Value
at
0x7fcefb43c490 >,
u'defu_o': < temba_client.v2.types.Value
at
0x7fcf080c2250 >,
u'dmed_o': < temba_client.v2.types.Value
at
0x7fcefa7ba890 >,
u'msg_routing': < temba_client.v2.types.Value
at
0x7fcefa7ba910 >,
u'role': < temba_client.v2.types.Value
at
0x7fcefb43c450 >,
u'tin_o': < temba_client.v2.types.Value
at
0x7fcefb43c350 >,
u'tout_o': < temba_client.v2.types.Value
at
0x7fcf080c29d0 >,
u'type': < temba_client.v2.types.Value
at
0x7fcefa7ba810 >,
u'weeknum': < temba_client.v2.types.Value
at
0x7fcefb43c110 >}

In[120]: run.values['amar_o']
Out[120]: < temba_client.v2.types.Value
at
0x7fcefb43c590 >

In[121]: w = run.values['amar_o']

In[122]: w.value
Out[122]: 0.0

In[123]: w.category
Out[123]: u'0 - 9999'

In[124]: w.value
Out[124]: 0.0

In[125]: w.deserialize?
Signature: w.deserialize(item)
Docstring: < no
docstring >
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / serialization.py
Type: instancemethod

In[126]: w??
Type: Value
String
form: < temba_client.v2.types.Value
object
at
0x7fcefb43c590 >
File: ~ / PycharmProjects / IMAM / ve / local / lib / python2
.7 / site - packages / temba_client / v2 / types.py
Source:


class Value(TembaObject):
  value = SimpleField()
  category = SimpleField()
  node = SimpleField()
  time = DatetimeField()


In[127]: w.value
Out[127]: 0.0

In[128]: w.time
Out[128]: datetime.datetime(2017, 4, 10, 13, 7, 18, 683588, tzinfo= < UTC >)


# Data cleaning
In [132]: '232!!1OOO'.replace('!', '1')
Out[132]: '232111OOO'

In [133]: '232!!1OOO'.replace('!', '1').replace('O', '0')
Out[133]: '232111000'

