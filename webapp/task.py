# -*- coding: utf-8 -*-
#!/usr/bin/env python
#author md5_salt
from celery import Celery
import wifi as wifilib
import json

# Initialize Celery
config={}
config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery('wifi', broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

@celery.task(bind=True)
def query_task(self, ssid, bssid):
	'''
	err:0, data:[{'ssid':xx, 'bssid':xx}, ...]
	'''
	w = wifilib.wifi()
	data = []

	total = len(ssid)
	for i in xrange(total):
		self.update_state(state='REQUEST',
						  meta={'ssid':ssid[i], 'bssid':bssid[i], 'index':i, 'total':total})
		rsp = w.request(ssid[i], bssid[i])
		if rsp['flag']:
			del rsp['flag']
			del rsp['msg']
			data.append(rsp)
	return {'err':0,'total':len(data),'data':data, 'index':len(data)}

@celery.task(bind=True)
def request_task(self, ssid, bssid):
	w = wifilib.wifi()
	self.update_state(state='REQUEST',
						  meta={'ssid':ssid, 'bssid':bssid})
	rsp = w.request(ssid, bssid)
	if rsp['flag']:
		del rsp['flag']
		del rsp['msg']
		return rsp
	else:
		return rsp
