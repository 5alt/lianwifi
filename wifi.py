# -*- coding: utf-8 -*-
#!/usr/bin/env python
#author md5_salt

import md5
from Crypto.Cipher import AES
import requests
import random
import re
from flask import Flask
from flask import request,redirect,url_for
app = Flask(__name__)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class wifi:
	aesKey = 'k%7Ve#8Ie!5Fb&8E'
	aesIV = 'y!0Oe#2Wj#6Pw!3V'
	aesMode = AES.MODE_CBC

	dhid = ''
	mac = ''
	ii = ''

	salt = ''#from server

	def __init__(self):
		self.RegisterNewDevice()

	def __sign(self, data, salt):
		request_str = ''
		for key in sorted(data):
			request_str += data[key]
		return md5.md5(request_str + salt).hexdigest().upper()

	def __decrypt(self, ciphertext):
		#[length][password][timestamp]
		decryptor = AES.new(self.aesKey, self.aesMode, IV=self.aesIV)
		return decryptor.decrypt(ciphertext.decode('hex')).strip()[3:-13]

	def RegisterNewDevice(self):
		salt = '1Hf%5Yh&7Og$1Wh!6Vr&7Rs!3Nj#1Aa$'
		data = {}
		data['appid'] = '0008'
		data['chanid'] = 'gw'
		data['ii'] = md5.md5(str(random.randint(1,10000))).hexdigest()
		data['imei'] = data['ii']
		data['lang'] = 'cn'
		data['mac'] = data['ii'][:12]#md5.md5(str(random.randint(1,10000))).hexdigest()[:12]
		data['manuf'] = 'Apple'
		data['method'] = 'getTouristSwitch'
		data['misc'] = 'Mac OS'
		data['model'] = '10.10.3'
		data['os'] = 'Mac OS'
		data['osver'] = '10.10.3'
		data['osvercd'] = '10.10.3'
		data['pid'] = 'initdev:commonswitch'
		data['scrl'] = '813'
		data['scrs'] = '1440'
		data['wkver'] = '324'
		data['st'] = 'm'
		data['v'] = '324'
		data['sign'] = self.__sign(data, salt)

		url = 'http://wifiapi02.51y5.net/wifiapi/fa.cmd'

		useragent = 'WiFiMasterKey/1.1.0 (Mac OS X Version 10.10.3 (Build 14D136))'
		headers = {'User-Agent': useragent}

		r = requests.post(url, data=data, headers=headers).json()

		if r['retCd'] == '0' and r['initdev']['retCd'] == '0':
			self.imei = data['imei']
			self.ii = data['ii']
			self.mac = data['mac']
			self.dhid = r['initdev']['dhid']
			self.salt = salt
			return True
		else:
			return False

	def __query(self, ssid, bssid):
		data = {}
		data['appid'] = '0008'
		data['bssid'] = ','.join(bssid)
		data['chanid'] = 'gw'
		data['dhid'] = self.dhid
		data['ii'] = self.ii
		data['lang'] = 'cn'
		data['mac'] = self.mac
		data['method'] = 'getSecurityCheckSwitch'
		data['pid'] = 'qryapwithoutpwd:commonswitch'
		data['ssid'] = ','.join(ssid)
		data['st'] = 'm'
		data['uhid'] = 'a0000000000000000000000000000001'
		data['v'] = '324'
		data['sign'] = self.__sign(data, self.salt)

		url = 'http://wifiapi02.51y5.net/wifiapi/fa.cmd'

		useragent = 'WiFiMasterKey/1.1.0 (Mac OS X Version 10.10.3 (Build 14D136))'
		headers = {'User-Agent': useragent}

		r = requests.post(url, data=data, headers=headers).json()

		self.salt = r['retSn']

		if r['retCd'] == '-1111':
			return self.__request(ssid, bssid)#maybe some problem

		ret = {}
		ret['flag'] = False
		ret['ssid'] = []
		ret['bssid'] = []

		if r['retCd'] == '0':
			if r['qryapwithoutpwd']['retCd'] == '0':
				for d in r['qryapwithoutpwd']['psws']:
					wifi = r['qryapwithoutpwd']['psws'][d]
					ret['ssid'].append(wifi['ssid'])
					ret['bssid'].append(wifi['bssid'])
				ret['flag'] = True
			else:
				ret['msg'] = r['qryapwithoutpwd']['retMsg']
		else:
			ret['msg'] = r['retMsg']

		return ret


	def query(self, ssid, bssid):
		wifi = self.__query(ssid, bssid)
		if wifi['flag']:
			ret = '='*10 + '<br>'
			for i in xrange(len(wifi['ssid'])):
				rsp = self.__request(wifi['ssid'][i], wifi['bssid'][i])
				if rsp['flag']:
					del rsp['flag']
					del rsp['msg']
					ret += '<br>'.join([x + ' : ' + str(rsp[x]) for x in rsp])
					ret += '<br>' + '='*10 + '<br>'
				else:
					del rsp['flag']
					ret += '<br>'.join([x + ' : ' + str(rsp[x]) for x in rsp])
					ret += '<br>' + '='*10 + '<br>'
			return ret
		else:
			return wifi['msg']


	def __request(self, ssid, bssid):
		data = {}
		data['appid'] = '0008'
		data['bssid'] = bssid
		data['chanid'] = 'gw'
		data['dhid'] = self.dhid
		data['ii'] = self.ii
		data['lang'] = 'cn'
		data['mac'] = self.mac
		data['method'] = 'getDeepSecChkSwitch'
		data['pid'] = 'qryapwd:commonswitch'
		data['ssid'] = ssid
		data['st'] = 'm'
		data['uhid'] = 'a0000000000000000000000000000001'
		data['v'] = '324'
		data['sign'] = self.__sign(data, self.salt)

		url = 'http://wifiapi02.51y5.net/wifiapi/fa.cmd'

		useragent = 'WiFiMasterKey/1.1.0 (Mac OS X Version 10.10.3 (Build 14D136))'
		headers = {'User-Agent': useragent}

		r = requests.post(url, data=data, headers=headers).json()

		self.salt = r['retSn']

		if r['retCd'] == '-1111':
			return self.__request(ssid, bssid)#maybe some problem

		ret = {}
		ret['flag'] = False
		ret['msg'] = 'empty'
		ret['ssid'] = ssid
		ret['bssid'] = bssid
		if r['retCd'] == '0':
			if r['qryapwd']['retCd'] == '0':
				for d in r['qryapwd']['psws']:
					wifi = r['qryapwd']['psws'][d]
					if wifi['pwd']:
						ret['pwd'] = self.__decrypt(wifi['pwd'])
						ret['flag'] = True
					if wifi['xUser']:
						ret['xUser'] = wifi['xUser']
						ret['xPwd'] = ['xPwd']
						ret['flag'] = True
			else:
				ret['msg'] = r['qryapwd']['retCd'] + ': ' + r['qryapwd']['retMsg']
		else:
			ret['msg'] = r['retCd'] + ': ' + r['retMsg']

		return ret

	def request(self, ssid, bssid):
		wifi = self.__request(ssid, bssid)
		if wifi['flag']:
			del wifi['flag']
			del wifi['msg']
			ret = '='*10 + '<br>'
			ret += '<br>'.join([x + ' : ' + str(wifi[x]) for x in wifi])
			ret += '<br>' + '='*10 + '<br>'
			return ret
		else:
			return wifi['msg']

def show_query_form():
	data = '''
<form action="/wifi" method="post">
  ssid:  <input type="text" name="ssid"><br>
  bssid: <input type="text" name="bssid">(mac address)<br>
  <input type="submit" value="Submit">
</form>
<br><br>
	'''
	return data

def show_text_form():
	data = '''
<form action="/text" method="post">
  data:<br><textarea name="text" cols=60 rows=4>
CMCC-EDU 06:11:b5:25:87:b6 0    11      Y  -- NONE
CMCC-WEB 00:11:b5:25:87:b6 0    11      Y  -- NONE
  </textarea><br>
  <input type="submit" value="Submit">
<br>
Note:<br>
* ssid and its bssid in one line<br>
* ssid before bssid, seperated by whitespaces<br>
* sample data is in the textarea, replace it with your own
<br>
	'''
	return data

w = wifi()

@app.route('/wifi', methods=['GET', 'POST'])
def index():
	global w
	if request.method == 'POST':
		if request.form['ssid'] and request.form['bssid']:
			return show_query_form() + w.request(request.form['ssid'], request.form['bssid'])
		else:
			return redirect(url_for('wifi'))
	else:
		return show_query_form()

@app.route('/text', methods=['GET', 'POST'])
def text():
	global w
	if request.method == 'POST':
		if request.form['text']:
			pattern = r"\s*(.*)\s+(([0-9a-f]{2}:){5}[0-9a-f]{2})"
			ssid = []
			bssid = []
			for ss, bss, dummy in re.compile(pattern, re.M).findall(request.form['text']):
				ssid.append(ss)
				bssid.append(bss)
			return show_text_form() + w.query(ssid, bssid)
		else:
			return redirect(url_for('text'))
	else:
		return show_text_form()

@app.route('/refresh')
def refresh():
	global w
	w.RegisterNewDevice()
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)    
