===============
Divmod PyFlakes
===============

PyFlakes a Lint-like tool for Python, like `PyChecker`_ or `PyLint`_. It is
focused on identifying common errors quickly without executing Python code.

Its primary advantage over PyChecker is that it is *fast*. You don't have to
sit around for minutes waiting for the checker to run; it runs on most large
projects in only a few seconds.

The two primary categories of defects reported by PyFlakes are:

* Names which are used but not defined or used before they are defined
* Names which are redefined without having been used

These can each take many forms. For example, PyFlakes will tell you when you
have forgotten an import, mistyped a variable name, defined two functions with
the same name, shadowed a variable from another scope, imported a module
twice, or two different modules with the same name, and so on.

Download
========

* `0.5.0 Release <http://pypi.python.org/packages/source/p/pyflakes/pyflakes-0.5.0.tar.gz#md5=568dab27c42e5822787aa8a603898672>`_
  (`Release Notes <http://bazaar.launchpad.net/~divmod-dev/divmod.org/trunk/view/2681.1.2/Pyflakes/NEWS.txt>`_)
  or ``pip install pyflakes``
* Trunk: ``bzr branch lp:divmod.org && cd divmod.org/PyFlakes``
  (`Browse <http://bazaar.launchpad.net/~divmod-dev/divmod.org/trunk/view/head:/Pyflakes/>`_)

Exits
=====

* `PyFlakes on PyPI <http://pypi.python.org/pypi/pyflakes>`_
* `PyFlakes on Launchpad <https://launchpad.net/pyflakes>`_
* `PyFlakes on SWiK <http://www.swik.net/pyflakes>`_

.. _PyChecker: http://pychecker.sourceforge.net
.. _PyLint: http://pypi.python.org/pypi/pylint
