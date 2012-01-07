============
Divmod Nevow
============

[[PageOutline(2-3,Contents)]]

[[Image(http://divmod.org/tracdocs/nevow_whtbck.png, left)]]

*Nevow* - Pronounced as the French 'nouveau', or 'noo-voh', Nevow is a web
application construction kit written in Python. It is designed to allow the
programmer to express as much of the view logic as desired in Python, and
includes a pure Python XML expression syntax named stan to facilitate this.
However it also provides rich support for designer-edited templates, using a
very small XML attribute language to provide bi-directional template
manipulation capability.

Nevow also includes :doc:`formless`, a declarative syntax for specifying the types of
method parameters and exposing these methods to the web. Forms can be rendered
automatically, and form posts will be validated and input coerced, rendering
error pages if appropriate. Once a form post has validated successfully, the
method will be called with the coerced values.

*Athena* - Finally, Nevow includes :doc:`athena-tutorial`, a two-way bridge
between Javascript in a browser and Python on the server. :doc:`athena-tutorial`
is compatible with  Mozilla, Firefox, Windows Internet Explorer 6, Opera 9 and
Camino (:doc:`../../misc/fan-club`). Event handlers can be written in pure
Python and Javascript implementation details are hidden from the programmer,
with Nevow taking care of routing data to and from the server using
`XmlHttpRequest <http://www.google.com/search?q=xmlhttprequest>`_.  Athena
supports a widget authoring framework that simplifies the authoring and
management of client side widgets that need to communicate with the server.
Multiple widgets can be hosted on an Athena page without interfering with each
other.  Athena supports automatic event binding so that that a DHTML event
(onclick,onkeypress,etc) is mapped to the appropriate javascript handler (which
in turn may call the server).


Download
========

 * Stable: `Latest release - 0.9.31
   <http://divmod.org/trac/attachment/wiki/SoftwareReleases/Nevow-0.9.31.tar.gz?format=raw>`_
 * Trunk: svn co http://divmod.org/svn/Divmod/trunk/Nevow/ Nevow


Features
========

 * *XHTML templates*: contain no programming logic, only nodes tagged with nevow
   attributes
 * *data/render methods*: simplify the task of separating data from presentation
   and writing view logic
 * *stan*: An s-expression-like syntax for expressing xml in pure python
 * *Athena*: Cross-browser JavaScript library for sending client side events to
   the server and server side events to the client after the page has loaded,
   without causing the entire page to refresh
 * *formless*: (take a look at `formal <http://forms-project.pollenation.net>`_
   for an alternate form library) For describing the types of objects which may
   be passed to methods of your
   classes, validating and coercing string input from either web or command-line
   sources, and calling your methods automatically once validation passes.
 * *webform*: For rendering web forms based on formless type descriptions,
   accepting form posts and passing them to formless validators, and rendering
   error forms in the event validation fails


Documentation
=============


 * `The Nevow Guide <http://divmod.org/trac/browser/trunk/Nevow/doc/>`_ An
   introductory guide covering Nevow basics (Getting Started, Object Traversal,
   Object Publishing, XML Templates, Deploying Nevow Applications)
 * `Nevow API <http://starship.python.net/crew/mwh/nevowapi/>`_
 * `Meet Stan <http://www.kieranholland.com/code/documentation/nevow-stan/>`_: An
   excellent tutorial on the Nevow Document Object Model by
   Kieran Holland
 * `Twisted Components
   <http://twistedmatrix.com/projects/core/documentation/howto/components.html>`_:
   If you are unfamiliar with Interfaces and Adapters
   then Nevow may not make much sense. This is essential reading.
 * :doc:`error-handling`: How to create custom error (404 and 500) pages
 * :doc:`form-handling`
   * `JavaScript WYSIWYG
   Editors <http://forms-project.pollenation.net/cgi-bin/trac.cgi/wiki/WYSIWYGTextArea>`_
   integration with Nevow/formal
 * :doc:`deployment`
 * :doc:`emacs`
 * :doc:`apache-proxy`
 * Using Nevow with Genshi templates:
   `original <http://oubiwann.blogspot.com/2007/03/genshi-templates-in-nevow.html>`_
   and
   `dynamic <http://oubiwann.blogspot.com/2008/03/genshi-on-nevow-revisited.html>`_
 * :doc:`storm-and-nevow`
 * :doc:`nevow-and-athena-faq`

 *Bleeding Docs* -
 **SURGEON GENERAL’S WARNING**: Reading the docs listed below pertain to code
 that has not yet been released and may cause Lung Cancer, Heart Disease,
 Emphysema, and Pregnancy complications.

   * :doc:`context-removal` - Conversion steps for moving from
     ``context``-based Nevow code to ``context``-less code.

Examples
========

To run the examples yourself (Source in [source:trunk/Nevow/examples]):

.. code-block:: sh

    richard@lazar:/tmp$ cd Nevow/examples/
    richard@lazar:/tmp/Nevow/examples$ twistd -noy examples.tac
    2005/11/02 15:18 GMT [-] Log opened.
    2005/11/02 15:18 GMT [-] twistd SVN-Trunk (/usr/bin/python 2.4.2) starting up
    2005/11/02 15:18 GMT [-] reactor class: twisted.internet.selectreactor.SelectReactor
    2005/11/02 15:18 GMT [-] Loading examples.tac...
    2005/11/02 15:18 GMT [-] Loaded.
    2005/11/02 15:18 GMT [-] nevow.appserver.NevowSite starting on 8080
    2005/11/02 15:18 GMT [-] Starting factory <nevow.appserver.NevowSite instance at 0xb6c8110c>

... visit http://localhost:8080 and you'll begin to appreciate the possibilities!


Help / Support
==============

You will find plenty of experts on the mailing lists and in the chatrooms who
will happily help you, but *please* make sure you *read all the documentation*,
*study all the examples* and *search the mailing list archives* first. The
chances are that your question has already been answered.

 * *Mailing list*: The `twisted-web
   <http://twistedmatrix.com/cgi-bin/mailman/listinfo/twisted-web>`_ and
   `divmod-dev </users/mailman.twistd/listinfo/divmod-dev>`_  mailing list pages
   have subscription instructions and links to the web based archives.
 * *IRC*: Nevow developers and users can be found on `Freenode
   <http://freenode.net>`_ in
   #twisted.web
 * *Blogs*: `dialtone <http://vvolonghi.blogspot.com>`_, `fzZzy
   <http://ulaluma.com/pyx/>`_, `Tv <http://tv.debian.net/blog/>`_
 * `Tickets
   <query:?status=new&status=assigned&status=reopened&component=Nevow&order=priority>`_
   (`More tickets <http://divmod.org/users/roundup.twistd/nevow/>`_)


Related Projects
================

 * `Eocmanage <http://www.inoi.fi/open/trac/eocmanage>`_: An alternative to
   Mailman built with Twisted and Nevow.
 * `Pollenation's Formal Project
   <http://forms-project.pollenation.net/cgi-bin/trac.cgi>`_: A fresh take on
   automatic form generation for Nevow, with a simpler interface and more input
   types than Formless.  This project was formerly known as 'forms'.
 * :doc:`../../products/mantissa`: An extensible, multi-protocol, multi-user,
   interactive application server built on top of Axiom and Nevow.
 * `Stiq <http://test.stiq.it>`_: A web news system built using Nevow
 * `WubWubWub <http://www.inoi.fi/open/trac/wubwubwub>`_: 'Making Twisted.Web
   look like Apache since 2002' A fully featured Twisted based webserver for
   serving multiple twisted.web and Nevow apps.



Index
=====

.. toctree::
   :maxdepth: 2

   getting-started
   tutorial
   error-handling
   form-handling
   formless
   authentication-and-authorization
   context-removal
   guard
   unit-testing

   apache-proxy
   reverse-proxy

   athena
   athena-tutorial
   athena-faq
   nevow-and-athena-faq

   demo-newsedit
   demo-results

   storm-and-nevow
   storm-approach
