Global Profile Site
===================

This is my global internet profile site at timhuegdon.com. It will be a hub for various rel="me" links, hopefully building a web of links from the various profiles I have on sites such as Twitter and Flickr etc.

The code
--------

The back-end will be constructed in Python -- served via mod_wsgi in Apache -- to aide my education of said language.

On the front-end I hope to disassemble [Stubbornella's Object Oriented CSS proposal](http://www.stubbornella.org/content/2009/02/28/object-oriented-css-grids-on-github/) and create something I think is more applicable, since I'm of the opinion that the concept is sound.

The file layout
---------------

I'll be using [http://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard](FHS) style structure:

* /etc -- will contain configuration files.
* /lib -- will contain extra scripts. At the moment, a Twitter API abstraction.
* /static -- will contain static files such as CSS and JS
* /templates -- does exactly what it says on the tin
* /wsgi-scripts -- the core Python code as accessed by mod_wsgi