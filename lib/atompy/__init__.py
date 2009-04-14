# -*- coding: utf-8 -*-

import urllib2

class AtomPy:
	"""Grab Atom feed and process."""
	
	USER_AGENT	= "AtomPy/1.0 +http://nefariousdesigns.co.uk/"
	etag		= {}
	last_mod 	= {}
	
	# Private methods
	
	def __anonymous_get( self, url, params=None ):
		if params:
			if params.has_key( "etag" ):
				etag = params[ "etag" ]
		
		request = self.__build_request( url, etag=etag )
		return self.__verify_request( request )
	
	def __build_request( self, url, etag=None ):
		request = urllib2.Request( url )
			
		if etag != None:
			etag = etag.get( url )
			request.add_header( "If-None-Match", etag )
		
		request.add_header( "User-Agent", self.USER_AGENT )
		
		return request
	
	def __verify_request( self, request, return_bool=False ):
		try:
			response = urllib2.urlopen( request )
			results = response.read()
		except urllib2.HTTPError, error:
			if error.code == 304:
				return None
			elif error.code == 401 or error.code == 403:
				raise UserNotAuthorised, "This user is not authorised for this action ( %s )" % error.code
			elif error.code == 400:
				raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
			else:
				raise HTTPError, "HTTP Error: %s ( %s )" % ( error.msg, error.code )
		else:
			self.etag[ request.get_full_url() ]		= response.headers.get( 'Etag' )
			self.last_mod[ request.get_full_url() ]	= response.headers.get( 'Last-modified' )
			if return_bool:
				return True
			else:
				return results
	
	# Public methods
	
	def get_feed( self, url, etag=None ):
		response = self.__anonymous_get( url, {
			"etag": etag,
		} )
		
		if response:
			print response