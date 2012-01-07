=============
Divmod Athena
=============


Athena is a two-way communication channel for Nevow applications.  Peruse `the
examples <browser:trunk/Nevow/examples/athenademo>`_.  Or make this page better.

:doc:`nevow-and-athena-faq`

=======
History
=======


Athena is the best-of-breed approach to developing interactive javascript (AJAX
/ Comet) applications with DivmodNevow.  It should be noted that it *supersedes*
previous solutions, such as livepage.  These prior solutions should not be used
with Athena development.  Before using Athena, you may want to check out the
:doc:`getting-started`.

.. todo:: this last link should point towards Nevow tutorial

=======================
Development Environment
=======================


If you haven't developed with JavaScript before, you may wish to set up your
development environment before beginning with Athena.  Some tips may be
available, depending on your preferred tools:

 * :doc:`nevow-athena-emacs`
 * `Firebug <http://www.getfirebug.com/>`_ - Firefox based javascript debugger



Simple LiveElement demo
=======================


Subclass ``nevow.athena.LiveElement`` and provide a ``docFactory`` which uses
the ``liveElement`` renderer:



.. code-block:: python

    from nevow import athena, loaders, tags as T

    class MyElement(athena.LiveElement):
        docFactory = loaders.stan(T.div(render=T.directive('liveElement')))


Put the result onto a ``nevow.athena.LivePage`` somehow:



.. code-block:: python

    class MyPage(athena.LivePage):
        docFactory = loaders.stan(T.html[
            T.head(render=T.directive('liveglue')),
            T.body(render=T.directive('myElement'))])

        def render_myElement(self, ctx, data):
            f = MyElement()
            f.setFragmentParent(self)
            return ctx.tag[f]

        def child_(self, ctx):
            return MyPage()


Put the page into a ``nevow.appserver.NevowSite`` somehow:



.. code-block:: python

    from nevow import appserver
    site = appserver.NevowSite(MyPage())


Hook the site up to the internet:



.. code-block:: python

    from twisted.application import service, internet

    application = service.Application('Athena Demo')
    webService = internet.TCPServer(8080, site)
    webService.setServiceParent(application)


Put it all into a ``.tac`` file and run it:



.. code-block:: sh

    twistd -noy myelement.tac


And hit http://localhost:8080/.  You now have an extremely simple Athena page.



Customizing Behavior
====================

Add a Twisted plugin which maps your module name onto your JavaScript source
file:



.. code-block:: python

    from nevow import athena

    myPackage = athena.JSPackage({
        'MyModule': '/absolute/path/to/mymodule.js',
        })


Place this Python source file into ``nevow/plugins/`` (`the Twisted plugin
documentation
<http://twistedmatrix.com/projects/core/documentation/howto/plugin.html>`_
describes where else you can put it, with the exception that Nevow plugins
should be placed beneath a ``nevow`` directory as opposed to a ``twisted``
directory).


In the JavaScript source file (in this case, ``mymodule.js``), import ``Nevow.Athena``:



.. code-block:: js

    // import Nevow.Athena


Next, subclass the JavaScript ``Nevow.Athena.Widget`` class (notice the module
name that was defined in the plugin file):



.. code-block:: js

    MyModule.MyWidget = Nevow.Athena.Widget.subclass('MyModule.MyWidget');


Now, add a method to your newly defined class:



.. code-block:: js

    MyModule.MyWidget.methods(
        function echo(self, argument) {
            alert('Echoing ' + argument);
            return argument;
        });


Define the JavaScript class which will correspond to your ``LiveElement``
subclass:



.. code-block:: python

    from nevow import athena, loaders, tags as T

    class MyElement(athena.LiveElement):
        jsClass = u'MyModule.MyWidget'
        docFactory = loaders.stan(T.div(render=T.directive('liveElement')))




Invoking Code in the Browser
============================


Add some kind of event source (in this case, a timer, but this is incidental)
which will cause the server to call a method in the browser:



.. code-block:: python

    from twisted.internet import reactor

    from nevow import athena, loaders, tags as T

    class MyElement(athena.LiveElement):
        jsClass = u'MyModule.MyWidget'
        docFactory = loaders.stan(T.div(render=T.directive('liveElement')))

        def __init__(self, *a, **kw):
            super(MyElement, self).__init__(*a, **kw)
            reactor.callLater(5, self.myEvent)

        def myEvent(self):
            print 'My Event Firing'
            self.callRemote('echo', 12345)


Start up the server again and revisit <http://localhost:8080>.



Invoking Code on the Server
===========================


Add an event source (in this case, a user-interface element, but this is
incidental) which will cause the browser to call a method on the server:



.. code-block:: python

    class MyElement(athena.LiveElement):
        docFactory = loaders.stan(T.div(render=T.directive('liveElement'))[
            T.input(type='submit', value='Push me',
                onclick='Nevow.Athena.Widget.get(this).clicked()')])
        ...


Update the JavaScript definition of ``MyModule.MyWidget`` to handle this event
and actually call the server method:



.. code-block:: js

    MyModule.MyWidget.method(
        'clicked',
        function(self) {
            self.callRemote('echo', 'hello, world');
        });


Add a method to ``MyElement`` which the browser will call, and expose it to the
browser:



.. code-block:: python

    class MyElement(athena.LiveElement):
        ...

        def echo(self, argument):
            print 'Echoing', argument
            return argument
        athena.expose(echo)


Start up the server again and revisit <http://localhost:8080>.



Download the files for this tutorial:
=====================================


 * `myelement.tac
   <http://divmod.org/trac/attachment/wiki/DivmodNevow/Athena/Files/myelement.tac?format=raw>`_
 * `mymodule.js
   <http://divmod.org/trac/attachment/wiki/DivmodNevow/Athena/Files/mymodule.js?format=raw>`_
 * `mymodule_pkg.py
   <http://divmod.org/trac/attachment/wiki/DivmodNevow/Athena/Files/mymodule_pkg.py?format=raw>`_



Testing
=======


Visit the :doc:`athena-testing` or `Test Driven Development with Athena
<http://blackjml.livejournal.com/21602.html>`_

==============
Implementation
==============


Though Divmod's use of it predates the term by several years, Athena uses what
some have come to call Comet.  Athena's JavaScript half makes an HTTP request
before it actually needs to retrieve information from the server.  The server
does not respond to this request until it has something to tell the browser.  In
this way, the server can push events to the browser instantly.

=======
Tickets
=======

See open tickets for Athena `here
<http://divmod.org/trac/query?status=new&status=assigned&status=reopened&component=Nevow&keywords=%7Eathena&order=priority>`_.
