===============
Divmod Mantissa
===============

Mantissa is an application server. It provides integration between the
:doc:`../axiom/index` 'smart' object database, the :doc:`../nevow/index` web
templating/AJAX/COMET framework and the `Twisted`_ framework.

Read more about Mantissa's philosophy and motivation:
:doc:`mantissa-is-the-target`.

The goal of Mantissa is to provide a common platform that open-source
contributors can use to help us build customized additions to the Divmod
service.  Divmod is going to offer a variety of different services, and if you
want to write something that hooks into our network, Mantissa is how you do
it.

.. _`Twisted`: http://twistedmatrix.com/

Download
========

 * Stable: [http://divmod.org/trac/attachment/wiki/SoftwareReleases/Mantissa-0.7.0.tar.gz?format=raw Get the most recent release - 0.7.0!] ([source:/tags/releases/Mantissa-0.7.0/NEWS.txt Release Notes])
 * Trunk: svn co http://divmod.org/svn/Divmod/trunk/Mantissa Mantissa (See the dependencies here: [source:trunk/Mantissa/DEPS.txt DEPS.txt])

Tutorials
=========

 * [wiki:DivmodAxiom/AxiomTutorial Exarkun's Axiom and Mantissa tutorial]: Short, sharp Axiom/Mantissa tips and tricks.
 * [wiki:MantissaWikiTutorial Mantissa Wiki Tutorial] A bit short on explanations, but complete
 * [wiki:MantissaBlogTutorial Mantissa Blog Tutorial] 
 * [wiki:MantissaHowTo An example of how to build a Mantissa application (incomplete)]

See Also
========

 * ''Development'' version of the [http://buildbot.divmod.org/apidocs/xmantissa.html Mantissa API docs]
 * Several of the Axiom docs on the DivmodAxiom page are also Mantissa docs.
 * [wiki:DivmodMantissa/Sharing /Sharing]: description of sharing functionality
 * [wiki:DivmodMantissa/Concepts /Concepts]: other concepts with which Mantissa users should be familiar

Index
=====

.. toctree::
    :maxdepth: 2
    :glob:

    mantissa-is-the-target
