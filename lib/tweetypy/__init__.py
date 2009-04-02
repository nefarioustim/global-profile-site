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

class TweetyPy:
	""" Abstraction for Twitter API """
	
	logged_in	= False
	username	= None
	password	= None
	auth_string = ""
	
	# Special methods
	
	def __init__( self, username=None, password=None ):
		self.username	= username
		self.password	= password
		
		if self.username and self.password:
			self.logged_in = self.__verify_login()
	
	# Private methods
	
	def __verify_login( self ):
		request				= urllib2.Request( "http://twitter.com/account/verify_credentials.xml" )
		self.auth_string	= base64.encodestring( "%s:%s" % ( self.username, self.password ) )
		request.add_header( "Authorization", "Basic %s" % self.auth_string )
		request.add_header( "User-Agent", "TweetyPy/1.0 +http://nefariousdesigns.co.uk/" )
		
		try:
			results = urllib2.urlopen( request ).read()
		except urllib2.HTTPError, error:
			if error.code == 401 or error.code == 403:
				raise LoginNotValid
			elif error.code == 400:
				raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
			else:
				raise HTTPError, "HTTP Error: %s ( %s )" % ( error.msg, error.code )
		else:
			return True
	
	def __authorised_get( self, url, params=None ):
		if not self.logged_in:
			raise NotLoggedIn
		
		if params:
			if url.find('?') != -1:
				url = url + urllib.urlencode( params )
			else:
				url = url + '?' + urllib.urlencode( params )
		
		request = urllib2.Request( url )
		request.add_header( "Authorization", "Basic %s" % self.auth_string )
		request.add_header( "User-Agent", "TweetyPy/1.0 +http://nefariousdesigns.co.uk/" )
		
		try:
			results = urllib2.urlopen( request ).read()
		except urllib2.HTTPError, error:
			if error.code == 401 or error.code == 403:
				raise UserNotAuthorised, "This user is not authorised for this action ( %s )" % error.code
			elif error.code == 400:
				raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
			else:
				raise HTTPError, "HTTP Error: %s ( %s )" % ( error.msg, error.code )
		else:
			return results
	
	def __anonymous_get( self, url, params=None ):
		if params:
			if url.find('?') != -1:
				url = url + urllib.urlencode( params )
			else:
				url = url + '?' + urllib.urlencode( params )
		
		request = urllib2.Request( url )
		request.add_header( "User-Agent", "TweetyPy/1.0 +http://nefariousdesigns.co.uk/" )
		
		try:
			results = urllib2.urlopen( request ).read()
		except urllib2.HTTPError, error:
			if error.code == 400:
				raise RateLimitExceeded, "The rate limit has been exceeded. Please try again later"
			else:
				raise HTTPError, "HTTP Error: %s ( %s )" % ( error.msg, error.code )
		else:
			return results
	
	def __parse_date(self, date):
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
	
	def __parse_messages( self, messages ):
		try:
			node = minidom.parseString( messages )
		except:
			raise MalformedXML
		else:
			return [ self.__parse_message( message.toxml( "utf-8" ) ) for message in node.getElementsByTagName( "status" ) ]
	
	def __parse_message( self, message ):
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
	
	def __parse_user( self, user ):
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
	
	def __get_tag_data( self, tag, node ):
		return node.getElementsByTagName( tag )[0].firstChild and node.getElementsByTagName( tag )[0].firstChild.data
	
	def __is_valid_count( self, count ):
		if count != None:
			try:
				count = int( count )
			except:
				raise CountNotValid
			else:
				if count < 1:
					raise CountNotValid
		
		return True
	
	# Public Methods
	
	def get_public_timeline( self, count=None ):
		if self.__is_valid_count( count ):
			response = self.__anonymous_get( "http://twitter.com/statuses/public_timeline.xml", { "count": count } )
			return self.__parse_messages( response )
	
	def get_user_timeline( self, count=None ):
		if self.__is_valid_count( count ):
			response = self.__authorised_get( "http://twitter.com/statuses/user_timeline.xml", { "count": count }  )
			return self.__parse_messages( response )
	
	def get_friends_timeline( self, count=None ):
		if self.__is_valid_count( count ):
			response = self.__authorised_get( "http://twitter.com/statuses/friends_timeline.xml", { "count": count }  )
			return self.__parse_messages( response )
	
	def get_replies_to_user( self, count=None ):
		if self.__is_valid_count( count ):
			response = self.__authorised_get( "http://twitter.com/statuses/replies.xml", { "count": count }	 )
			return self.__parse_messages( response )