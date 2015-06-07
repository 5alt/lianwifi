# -*- coding: utf-8 -*-
#!/usr/bin/env python
#author md5_salt

from flask import Flask, request, render_template, session, flash, redirect, \
	url_for, jsonify
from task import *
import wifi as wifilib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keep_it_secret'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['ssid'] and request.form['bssid']:
			task = request_task.apply_async(request.form['ssid'], request.form['bssid'])
			return jsonify({}), 202, {'Location': url_for('taskstatus',
												  task_id=task.id)}
		else:
			return redirect(url_for('index'))
	else:
		return render_template('index.htm')

@app.route('/text', methods=['GET', 'POST'])
def text():
	if request.method == 'POST':
		if request.form['text']:
			#for mac: airport -s
			pattern1 = r"\s*(.*)\s+(([0-9a-f]{2}:){5}[0-9a-f]{2})"
			#for windows: powershell or cmd -- netsh wlan show network mode=bssid
			pattern2 = r"SSID \d{1,2} : (.*)\n.*\n.*\n.*\n.*(([0-9a-f]{2}:){5}[0-9a-f]{2})"
			#order is very important!
			if  re.compile(pattern2, re.M).findall(request.form['text']):
				pattern = pattern2
			else:
				pattern = pattern1

			ssid = []
			bssid = []
			for ss, bss, dummy in re.compile(pattern, re.M).findall(request.form['text']):
				ssid.append(ss)
				bssid.append(bss)
			if len(ssid) == 0 or len(bssid) == 0:
				return redirect(url_for('index'))
			w = wifilib.wifi()
			wifi = w.query(ssid, bssid)
			if wifi['err']:
				return jsonify({'total':0, 'err':wifi['err'], 'msg':wifi['msg']})
			total = len(wifi['ssid'])
			if total == 0:
				return jsonify({'total':0, 'err':0, 'msg':'not found!'})
			task = query_task.apply_async((wifi['ssid'], wifi['bssid']))
			return jsonify({'total':total, 'err':0, 'msg':'waiting...'}), 202, {'Location': url_for('taskstatus',
												  task_id=task.id)}
	return redirect(url_for('index'))

@app.route('/status/<task_id>')
def taskstatus(task_id):
	task = query_task.AsyncResult(task_id)
	if not task or not task.info:
		return jsonify({'state':'WAITING'})
	task.info['state'] = task.state
	return jsonify(task.info)

if __name__ == '__main__':
	app.run(debug=True)