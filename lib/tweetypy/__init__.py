# -*- coding: utf-8 -*-

import urllib, urllib2, base64, re, time, datetime
from xml.dom import minidom

# Define exceptions

class TweetyPyError( Exception ):
	"""Generic parent class for exceptions"""
	pass

class TwitterNotAvailable( TweetyPyError ):
	"""Raised when Twitter is down"""
	pass

class RateLimitExceeded( TweetyPyError ):
	"""Raised when API rate limit is exceeded"""
	pass

class LoginNotValid( TweetyPyError ):
	"""Raised when invalid login information is provided"""
	pass

class UserNotAuthorised( TweetyPyError ):
	"""Raised when user is not authorised to perform the action"""
	pass

class NotLoggedIn( TweetyPyError ):
	"""Raised when user isn"t logged in"""
	pass

class CountNotValid( TweetyPyError ):
	"""Invalid value was passed as count"""
	pass

class MalformedXML( TweetyPyError ):
	"""Raised when malformed XML is returned"""
	pass

class MalformedDate( TweetyPyError ):
	"""Raised when a malformed date is returned"""
	pass

class HTTPError( TweetyPyError ):
	"""Raised for other HTTPLib errors"""
	pass

# Main abstraction class
#----------------------------------------
class TweetyPy( object ):
#----------------------------------------
	""" Abstraction for Twitter API """
	
	logged_in	= False
	username	= None
	password	= None
	auth_string = ""
	user_agent	= "TweetyPy/1.0 +http://github.com/nefarioustim/TweetyPy/"
	etag		= {}
	
	# Special methods
	
	#----------------------------------------
	def __init__( self, username=None, password=None ):
	#----------------------------------------
		self.username	= username
		self.password	= password
		
		if self.username and self.password:
			self.logged_in = self.__get_valid_login()
	
	# Private methods
	
	#----------------------------------------
	def __anonymous_get( self, url, params=None ):
	#----------------------------------------
		"""Performs an anonymous HTTP GET to url with params.
		
		Returns result XML from Twitter."""
		
		if params:
			if params.has_key( "etag" ):
				etag = params[ "etag" ]
				del params[ "etag" ]
			url = self.__get_url_with_params( url, params )
		
		request = self.__get_request( url, etag=etag )
		return self.__get_valid_response( request )
	
	#----------------------------------------
	def __authorised_get( self, url, params=None ):
	#----------------------------------------
		"""Performs an authorised HTTP GET to url with params.
		
		Returns result XML from Twitter."""
		
		if not self.logged_in:
			raise NotLoggedIn

		if params:
			if params.has_key( "etag" ):
				etag = params[ "etag" ]
				del params[ "etag" ]
			url = self.__get_url_with_params( url, params )
		
		request = self.__get_request( url, auth=True, etag=etag )
		return self.__get_valid_response( request )
	
	#----------------------------------------
	def __get_all_messages( self, response_xml ):
	#----------------------------------------
		"""Returns all parsed messages from Twitter XML as a list."""
		
		try:
			node = minidom.parseString( response_xml )
		except:
			raise MalformedXML
		else:
			return [ self.__parse_message( message.toxml( "utf-8" ) ) for message in node.getElementsByTagName( "status" ) ]
	
	#----------------------------------------
	def __get_request( self, url, auth=False, etag=None ):
	#----------------------------------------
		"""Returns a valid Request object with authorization, etag, and user-agent headers."""
		
		request = urllib2.Request( url )
		
		if auth:
			request.add_header( "Authorization", "Basic %s" % self.auth_string )
		
		if etag != None:
			etag = etag.get( url )
			request.add_header( "If-None-Match", etag )
			
		request.add_header( "User-Agent", self.user_agent )
		
		return request
	
	#----------------------------------------
	def __get_url_with_params( self, url, params ):
	#----------------------------------------
		"""Returns a url with encoded parameters."""
		
		if url.find('?') != -1:
			url = url + urllib.urlencode( params )
		else:
			url = url + '?' + urllib.urlencode( params )

		return url
	
	#----------------------------------------
	def __get_tag_data( self, tag, node ):
	#----------------------------------------
		"""Returns tag contents if the tag exists."""
		
		return node.getElementsByTagName( tag )[0].firstChild and node.getElementsByTagName( tag )[0].firstChild.data
	
	#----------------------------------------
	def __get_valid_login( self ):
	#----------------------------------------
		"""Returns a result as long as class login credentials are verified."""
		
		url 				= "http://twitter.com/account/verify_credentials.xml"
		self.auth_string	= base64.encodestring( "%s:%s" % ( self.username, self.password ) )

		request = self.__get_request( url, auth=True )

		try:
			results = self.__get_valid_response( request, return_bool=True )
		except UserNotAuthorised:
			raise LoginNotValid
		else:
			return results
	
	#----------------------------------------
	def __get_valid_response( self, request, return_bool=False ):
	#----------------------------------------
		"""Returns response results when request is valid."""
		
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
			self.etag[ request.get_full_url() ] = response.headers.get( 'Etag' )
			if return_bool:
				return True
			else:
				return results
	
	#----------------------------------------
	def __is_valid_count( self, count ):
	#----------------------------------------
		"""Validates count."""
		if count != None:
			try:
				count = int( count )
			except:
				raise CountNotValid
			else:
				if count < 1:
					raise CountNotValid
		
		return True
	
	#----------------------------------------
	def __parse_date(self, date):
	#----------------------------------------
		"""parse out non-standard date format used by Twitter
		
		Usually in the form: Sun Jul 13 12:44:07 +0000 2008
		Should return: datetime.datetime(2008, 06, 13, 12, 44, 07)
		"""
		date_regex = re.compile( r"""
			^
			(?P<day_name>[a-zA-Z]+)
			\s+
			(?P<month_name>[a-zA-Z]+)
			\s+
			(?P<day>\d+)
			\s+
			(?P<hours>\d+)
			:
			(?P<minutes>\d+)
			:
			(?P<seconds>\d+)
			\s+
			\+\d+
			\s+
			(?P<year>\d+)
			$
		""", re.VERBOSE )
		
		if date_regex.match( date ):
			date_string = date_regex.sub( r"\g<year> \g<month_name> \g<day> \g<hours>:\g<minutes>:\g<seconds>", date )
			date_struct = time.strptime( date_string, '%Y %b %d %H:%M:%S' )
			return datetime.datetime( *date_struct[:6] )
		else:
			raise MalformedDate
	
	#----------------------------------------
	def __parse_message( self, message ):
	#----------------------------------------
		"""Parses message XML and returns a dictionary."""
		
		try:
			node = minidom.parseString( message )
		except:
			raise MalformedXML
		else:
			result = {
				"id" : self.__get_tag_data( "id", node ),
				"created_at_raw" : self.__get_tag_data( "created_at", node ),
				"created_at" : self.__parse_date( self.__get_tag_data( "created_at", node ) ),
				"text" : self.__get_tag_data( "text", node ),
				"user" : self.__parse_user( node.getElementsByTagName( "user" )[0].toxml( "utf-8" ) )
			}
			
			return result
	
	#----------------------------------------
	def __parse_user( self, user ):
	#----------------------------------------
		"""Parses user XML and returns a dictionary."""
		
		try:
			node = minidom.parseString( user )
		except:
			raise MalformedXML
		else:
			result = {
				"id" : self.__get_tag_data( "id", node ),
				"name" : self.__get_tag_data( "name", node ),
				"screen_name" : self.__get_tag_data( "screen_name", node ),
				"location" : self.__get_tag_data( "location", node ),
				"description" : self.__get_tag_data( "description", node ),
				"profile_image_url" : self.__get_tag_data( "profile_image_url", node ),
				"url" : self.__get_tag_data( "url", node ),
			}
			
			return result
	
	# Public Methods
	
	#----------------------------------------
	def get_public_timeline( self, count=None, etag=None ):
	#----------------------------------------
		if self.__is_valid_count( count ):
			response = self.__anonymous_get( "http://twitter.com/statuses/public_timeline.xml", {
				"count": count,
				"etag": etag,
			} )
			if response:
				return self.__get_all_messages( response )
			else:
				return []
	
	#----------------------------------------
	def get_user_timeline( self, count=None, etag=None ):
	#----------------------------------------
		if self.__is_valid_count( count ):
			response = self.__authorised_get( "http://twitter.com/statuses/user_timeline.xml", {
				"count": count,
				"etag": etag,
			} )
			if response:
				return self.__get_all_messages( response )
			else:
				return []
	
	#----------------------------------------
	def get_friends_timeline( self, count=None, etag=None ):
	#----------------------------------------
		if self.__is_valid_count( count ):
			response = self.__authorised_get( "http://twitter.com/statuses/friends_timeline.xml", {
				"count": count,
				"etag": etag,
			} )
			if response:
				return self.__get_all_messages( response )
			else:
				return []
	
	#----------------------------------------
	def get_replies_to_user( self, count=None, etag=None ):
	#----------------------------------------
		if self.__is_valid_count( count ):
			response = self.__authorised_get( "http://twitter.com/statuses/replies.xml", {
				"count": count,
				"etag": etag,
			} )
			if response:
				return self.__get_all_messages( response )
			else:
				return []