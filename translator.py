#!/usr/bin/env python

import urllib as ul
import urllib2 as ul2
import json


class Translator(object):
	'''
	Makes use of Apertium REST API http://wiki.apertium.org/wiki/Apertium_web_service
	You can provide your own apikey
	'''
	def __init__(self, apikey=None):
		self.url = "http://api.apertium.org/json/"
		self.key = apikey
		self.pairsCache = "ro|es,es|fr,en|gl,oc|es,es|ro,es|ca_valencia,mk|bg,fr|es,oc_aran|ca,pt|gl,en|ca,an|es,eu|es,es|ca,fr|eo,es|gl,ca|pt,nb|nn_a,mk|en,ca|en_US,pt|ca,is|en,fr|ca,gl|en,gl|es,ca|oc_aran,nn|nb,ca|oc,en|es,es|pt,oc_aran|es,es|eo,oc|ca,cy|en,es|en,ca|fr,br|fr,en|eo,bg|mk,ca|eo,ca|en,es|oc_aran,sv|da,nn|nn_a,pt|es,es|pt_BR,es|oc,es|an,da|sv,it|ca,gl|pt,eo|en,ca|es,es|en_US,nn_a|nn,nb|nn"

	def translate(self, phrase, langpair):
		self.service = "translate"
		self.params = {"q": phrase, "langpair": langpair, "markUnknown": "no"}
		resp = self.sendRequest()
		if not resp:
			return resp
		return resp['translatedText']

	def listPairs(self):
		# pairs = [tuple(pair.split('|')) for pair in self.pairsCache.split(',')]
		# return pairs
		self.service = "listPairs"
		self.params = {}
		resp = self.sendRequest()
		return [(e['sourceLanguage'], e['targetLanguage']) for e in resp]

	def sendRequest(self):
		if self.key:
			self.params['key'] = self.key
		data = ul.urlencode(self.params)
		req = ul2.Request(self.url + self.service, data)
		resp = None
		try:
			resp = ul2.urlopen(req)
		except Exception, e:
			if hasattr('reason'): print "Server couldn't respond. Reason:", e.reason
			elif hasattr('code'): print "Server couldn't handle request. Error code:", e.code
		else:
			if resp.code != 200:
				print "Http Code:", resp.code
			else:
				pobj = json.loads(resp.read())
				status = pobj['responseStatus']
				if status != 200:
					print "Unexpected response status:", status
					print "Details:", pobj['responseDetails']
				else:
					return pobj['responseData']
		return None


def main():
	t = Translator()
	# allpairs = t.listPairs()
	# pairs = [(src + '|' + tgt) for src, tgt in allpairs if src == 'en']
	# print "AllPairs:", ", ".join((src+'|'+trgt) for src, trgt in allpairs)
	phrase = "hello world"
	e = 'en|es'
	e2 = 'es|fr'
	trans = t.translate(phrase, e)
	trans2 = t.translate(trans, e2)
	print e, "->", trans.encode('utf-8')
	print e2, "->", trans2.encode('utf-8')


if __name__ == '__main__':
	main()


# translate = "translate"
# listPairs = "listPairs"
# apikey = ""
#
# query = "house"
# langpair = "en|es"
# service = "translate"
# params = {"q": query, "langpair": langpair}
# params["key"] = apikey
# data = ul.urlencode(params)
# req = ul2.Request(url + service, data)
# try:
# 	resp = ul2.urlopen(req)
# except Exception, e:
# 	print e.reason
# httpcode = resp.code
# if httpcode != 200:
# 	print "http code:", httpcode
# else:
# 	jsobj = resp.read()
# 	# print "JSON:", jsobj
# 	pobj = json.loads(jsobj)
# 	# print "DATA:",  pobj
# 	status = pobj["responseStatus"]
# 	if status != 200:
# 		print "Response status:", status, pobj["responseDetails"]
# 	else:
# 		print langpair + ": " + query +" -> " + pobj["responseData"]['translatedText']
