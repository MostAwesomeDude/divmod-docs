============
Unit Testing
============


**Note: Much of this page documents the current development version of Nevow's
testing features, not the current release version.  Make sure you are using the
right version of the code if you attempt to make use of this documentation.**

Divmod uses the stand-alone JavaScript interpreter `SpiderMonkey
<http://www.mozilla.org/js/spidermonkey/>`_ to run unit tests on some portions
of our !JavaScript sources.  You can find `several
<browser:trunk/Nevow/nevow/test/test_object.js>`_ `examples
<browser:trunk/Nevow/nevow/test/test_deferred.js>`_ in the Divmod repository.

These unit tests are valuable: they reveal simple errors, provide a kind of
documentation as to the purpose of various functions, and ensure that the code
is exercised in as much isolation as is possible.  However, they are not
all-encompassing.  After all, they aren't even executed by the same runtime that
will be used by **any** user to execute them.

``nit`` can also be used for unit testing (see below).



Functional Testing
==================


To account for this, Nevow provides ``nit``, a runner for tests which are
designed to be run by an actual browser.  Nit tests are placed in Python source
files named with the ``livetest_`` prefix.  There are `several
<browser:trunk/Nevow/nevow/test/livetest_athena.py>`_ `examples
<browser:trunk/Mantissa/xmantissa/test/livetest_forms.py>`_ `of this
<browser:trunk/Mantissa/xmantissa/test/livetest_people.py>`_ kind of test in the
Divmod repository as well.

If you are familiar with `XUnit <http://en.wikipedia.org/wiki/XUnit>`_, the API
presented by nit should present few surprises.  The primary interface of
interest to test developers is the ``TestCase`` class, which is subclassed and
extended to define new tests.



Server Side
===========


``nevow.livetrial.testcase.TestCase`` is the base class for the server-side
implementation of test methods.  Subclasses of ``TestCase`` define the
JavaScript class which will implement the client-side portion of test methods as
well as the document which will be used to render them.  ``TestCase`` is a
``nevow.athena.LiveFragment`` subclass, so it can also define methods which are
exposed to the client.

A TestCase might be no more complex than the following:



.. code-block:: python

    from nevow.livetrial.testcase import TestCase
    from nevow.athena import expose

    class AdditionTestCase(TestCase):
        jsClass = 'Examples.Tests.AdditionTestCase'




Client Side
===========


On the JavaScript side, test authors subclass ``Nevow.Athena.Test.TestCase`` and
define actual test methods on it.  These methods may return Deferreds if they
are testing asynchronous APIs.  Test methods which return a Deferred which
eventually errbacks are treated as failing; those which return a Deferred which
eventually callbacks are treated as succeeding.  Tests which return anything
other than a Deferred are also treated as succeeding, and tests which throw any
error are treated as failing.

The JavaScript half of the above example might look like this:



.. code-block:: js


    // import Nevow.Athena.Test

    Examples.Tests.AdditionTestCase = Nevow.Athena.Test.TestCase.subclass('Examples.Tests.AdditionTestCase');
    Examples.Tests.methods(
        function test_integerAddition(self) {
            self.assertEqual(1 + 1, 2);
        },

        function test_stringAddition(self) {
            self.assertEqual('a' + 'a', 'aa');
        });




Command Line
============

Tests are collected into a suite automatically by the nit command line.  For
example, ``nit nevow`` will launch a server which runs all of Nevow's nits.  The
server listens on http://localhost:8080/ by default.  To run the tests, visit
that URL with a browser and click the ``Run Tests`` button.



External Links
==============

You might want to look at this walkthrough on `how to write tests for Athena
<http://blackjml.livejournal.com/21602.html>`_.
