
# this function is taken from httpscreenshot, it checks if the URL supports connection with SSL 

def autodetectRequest(url, timeout, vhosts=False, urlQueue=None, subs=None, extraHosts=None,proxy=None):
	'''Takes a URL, ignores the scheme. Detect if the host/port is actually an HTTP or HTTPS
	server'''
	resp = None
	host = urlparse(url[0]).hostname
	port = urlparse(url[0]).port

	if(port is None):
		if('https' in url[0]):
			port = 443
		else:
			port = 80

	try:
		#cert = ssl.get_server_certificate((host,port))
		
		cert = timeoutFn(ssl.get_server_certificate,kwargs={'addr':(host,port),'ssl_version':ssl.PROTOCOL_SSLv23},timeout_duration=3)

		if(cert is not None):
			if('https' not in url[0]):
				url[0] = url[0].replace('http','https')
				#print 'Got cert, changing to HTTPS '+url[0]

		else:
			url[0] = url[0].replace('https','http')
			#print 'Changing to HTTP '+url[0]


	except Exception as e:
		url[0] = url[0].replace('https','http')
		#print 'Changing to HTTP '+url[0]
	try:
		resp = doGet(url,verify=False, timeout=timeout, vhosts=vhosts, urlQueue=urlQueue, subs=subs, extraHosts=extraHosts, proxy=proxy)
	except Exception as e:
		print 'HTTP GET Error: '+str(e)
		print url[0]

	return [resp,url]
