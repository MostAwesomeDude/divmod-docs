==========
Athena FAQ
==========

Q) When I reload a page, the server logs a traceback ending with
``exceptions.AssertionError: Cannot render a LivePage more than once``

A) LivePage instances maintain server-side state that corresponds to the
connection to the browser.  Because of this, each LivePage instance can only be
used to serve a single client.  When you serve LivePages, make sure that you
create a new instance for each render pass.

Here is an example(from Dominik Neumann) about using LivePage as a main page:
Wrap you Index page like:


.. code-block:: python

    class RootPage(Index):
    	'''
    	always return a new Index
    	'''
    	def child_(self, ctx):
    		return Index()





Q) I can't debug athena on Internet explorer.  what gives?

A) Athena include the livefragment javascript in the body of the document via a
script tag.  Visual studio doesn't appear to be happy with this and does not let
you set break points.  If you load the javascript in the head of the document
then you can set a break point in your athena livefragment javascript using
visual studio.  The best way I found to do this is manually include the
javacript in the header and then information athena that the livefragment
javascript is already loaded.  One way to do this is to call the 'hidden'
_shouldInclude method on the athena livepage instance, e.g
self._shouldInclude('yourjsmodule').  This will let athena know that the
javascript is already loaded and not to load it twice.

Q) Why doesn't Athena support Safari?

A) Athena supports recent versions of Safari.

Q) How can I unit-test javascript code using Athena?

A) The same way you unit-test your ordinary `Twisted
<http://twistedmatrix.com>`_ or `Divmod <http://divmod.org>`_ software: by using
`trial <http://twistedmatrix.com/trac/wiki/TwistedTrial>`_. You can find
:doc:`athena-testing`. Have a look at `nevow.test.test_javascript
<http://divmod.org/trac/browser/trunk/Nevow/nevow/test/test_javascript.py>`_ to
see, how tests are prepared and run.

Q) How can I add elements to an already rendered LivePage?

A) See `Nevow.Athena.Widget.addChildWidgetFromWidgetInfo
<http://divmod.org/trac/browser/trunk/Nevow/nevow/js/Nevow/Athena/__init__.js#L897>`_
and the :doc:`nevow-athena-tutorials-live-elements-on-fly`
