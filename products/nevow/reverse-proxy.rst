=============
Reverse Proxy
=============

A Reverse Proxy forwards the requests it receives from the internet to one or
more slave webservers. Lighttpd and Apache both provide reverse proxy modules.
Any absolute urls in the response will contain the `scheme
<http://en.wikipedia.org/wiki/URL#URL_scheme>`_ (possibly the hostname) and port
number on which the slave is running. These must be rewritten before being
returned to the client. In Nevow this can be handled by
`vhost.VHostMonsterResource <source:trunk/Nevow/nevow/vhost.py>`_.


Example 1
=========

You have an existing webserver running on port 80, doing `name based virtual
hosting <http://httpd.apache.org/docs/2.0/vhosts/name-based.html>`_ of several
existing websites and want to run a Nevow based site alongside them on the same
IP.


Solution
========

Forward all requests at this virtual host to the Nevow slave server.


Sample Nevow App
================



.. code-block:: python

    from zope.interface import implements
    from twisted.application import service, strports
    from nevow import appserver, inevow, loaders, rend, url, vhost

    class MyPage(rend.Page):
        '''
        I am a simple resource for demo purposes only. I will return a 'MyPage'
        for any child you ask me to locate. I display the current url as calculated
        nevow.url.
        '''
        addSlash = True
        docFactory = loaders.xmlstr('''
    <html xmlns:n='http://nevow.com/ns/nevow/0.1'>
        <head>
            <title n:render='urlpath'></title>
        </head>
        <body>
            <h1 n:render='urlpath'></h1>
        </body>
    </html>
    ''')
        
        def render_urlpath(self, ctx, data):
            return ctx.tag[url.here]
        
        def locateChild(self, ctx, segments):
            return MyPage(), segments[1:]

    class VhostFakeRoot:
        '''
        I am a wrapper to be used at site root when you want to combine 
        vhost.VHostMonsterResource with nevow.guard. If you are using guard, you 
        will pass me a guard.SessionWrapper resource.
        '''
        implements(inevow.IResource)
        def __init__(self, wrapped):
            self.wrapped = wrapped
        
        def renderHTTP(self, ctx):
            return self.wrapped.renderHTTP(ctx)
            
        def locateChild(self, ctx, segments):
            '''Returns a VHostMonster if the first segment is 'vhost'. Otherwise
            delegates to the wrapped resource.'''
            if segments[0] == 'vhost':
                return vhost.VHostMonsterResource(), segments[1:]
            else:
                return self.wrapped.locateChild(ctx, segments)

    siteRoot = VhostFakeRoot(MyPage())
    application = service.Application('reverse proxy / vhost example')
    strports.service('8080', appserver.NevowSite(siteRoot)).setServiceParent(application)

Save as eg sample.tac and run using twistd -noy sample.tac


Sample Lighttpd Config:
=======================


::

    $HTTP['host'] =~ '^(www.example.com)$' {
            url.rewrite-once = ('^/(.*)' => '/vhost/http/%0/$1')
            # In lighttpd we alter the path manually using rewrite rule. %0
            # refers to the hostname and $1 is the path.
            proxy.server = ( '' =>
                    ( (
                    'host' => '127.0.0.1',
                    'port' => 8080
                    ) )
            )
    }



If you prefer a mixed deployment strategy where static content is served through
the faster lighttpd while dynamic content is still served by twisted you can use
the following recipe.


::

    $HTTP['host'] =~ '^(www.example.org)$' {
            url.rewrite-once = (
                    '^/static/.*' => '$0',
                    '^/(.*)' => '/vhost/http/%0/$1'
            )
            $HTTP['url'] !~ '^/static/' {
                    proxy.server = ( '' =>
                            ( (
                            'host' => '127.0.0.1',
                            'port' => 8080
                            ) )
                    )
            }
            server.document-root = '/path/to/your/project/trunk/'
    }




There are 2 assumptions in this recipe:
 * The static content is located at the /static/ subtree of the website.
 * The project root contains a 'static' directory that is used to serve static
   content.



Sample Apache Config (`Ref <http://divmod.org/users/wiki.twistd/nevow/moin.cgi/ApacheSetup>`_)
==============================================================================================


::

    <VirtualHost www.example.com>
    ProxyPass / http://localhost:8080/vhost/http/www.example.com/
    ServerName www.example.com
    </VirtualHost>





Example 2
=========

Nevow is only to be used for part of an existing static site at a non-root url


Sample Lighttpd Config:
=======================

TODO


Sample Apache Config
====================

TODO


See Also
========

 * http://lighttpd.net/documentation/proxy.html
 * http://httpd.apache.org/docs/2.0/mod/mod_proxy.html#proxypass
