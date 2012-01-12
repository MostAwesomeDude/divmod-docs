============
Divmod Axiom
============

Axiom is an object database whose primary goal is to provide an
object-oriented layer with what we consider to be the key aspects of OO, i.e.
polymorphism and message dispatch, without hindering the power of an RDBMS.
It is designed to 'feel Pythonic', without encouraging the typical ORM
behavior such as :doc:`/philosophy/potato`.

Axiom provides a full interface to the database, which strongly suggests that
you do not write any SQL of your own. Metaprogramming is difficult and
dangerous (as many, many SQL injection attacks amply demonstrate). Writing
your own SQL is still possible, however, and Axiom does have several methods
which return fragments of generated schema if you wish to use them in your own
queries.

Axiom currently supports only SQLite and does NOT have any features for dealing
with concurrency. We do plan to add some later, and perhaps also support other
databases in the future. Take a look at :doc:`axiom-concurrency-scalability` for
more information - we'll update this as the community makes progress on these
issues.

Performance
===========

How does Axiom perform?

Here are some simple third-party `benchmarks
<http://www.livejournal.com/users/william_os4y/1271.html>`_.

Download
========

* Stable: `Download the latest release - 0.6.0!
  <http://divmod.org/trac/attachment/wiki/SoftwareReleases/Axiom-0.6.0.tar.gz?format=raw>`_
  (Requires :doc:`../epsilon`) (`Release Notes <source:/tags/releases/Axiom-0.6.0/NEWS.txt>`_)
* Trunk: svn co http://divmod.org/svn/Divmod/trunk/Axiom Axiom

See Also
========

* :doc:`axiom-tutorial-linkfarm`: Short, sharp Axiom/Mantissa tips and tricks.
* :doc:`axiom-why-axiom`: Glyph writes about the advantages of Axiom over other RDBMS and ORM alternatives.
* :doc:`axiom-reference`: A reference to the Axiom public API. (Incomplete but evolving!)
* **Development** version of the `Axiom API docs <http://buildbot.divmod.org/apidocs/axiom.html>`_
* :doc:`axiom-examples`
* `Axiom tickets <query:?status=new&status=assigned&status=reopened&groupdesc=1&group=type&component=Axiom&order=priority>`_
* :doc:`axiomatic`
* :doc:`axiom-dependency-transition`: How to transition from pre-``axiom.dependency`` code.
* :doc:`axiom-powerups`
* WritingUpgradeTests: writing stubloader tests for schema upgrades.
* :doc:`axiom-files`


Index
=====

.. toctree::
    :maxdepth: 2
    :glob:

    axiom-concurrency-scalability
    axiom-tutorial-linkfarm
    axiom-why-axiom
    axiom-powerups
    axiom-reference
