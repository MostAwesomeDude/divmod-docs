==============
Dynamic Typing
==============


Reference to Any
================

A column in your schema may contain a reference to any row in the database.


Schema Migration: Automatic Upgrades
====================================

Axiom defines a comprehensive API for upgrading from one version of a schema to
the next, both writing upgraders, and scheduling them to be run.


Transaction Management and Consistency
======================================

While it is definitely possible to run in autocommit mode, axiom provides a
'transact' method to manage transactions for you.  Transactions are reverted
when an exception crosses the transaction boundary, so errors will generally not
affect the state of your persistent data.  When transactions are reverted, they
are reverted **all the way**: objects in memory are restored to the state they
were in before the transaction began, both in memory and on disk.  Axiom also
takes care to keep Python identity consistent with database identity within a
process; if you load an object twice, and change one of its attributes, the
attribute will therefore be changed in both places, making it safe to share
references between different areas of code.

This is a critical feature for financial applications that is missing from other
popular Python database tools, such as SQLObject and SQLAlchemy.


Multi-Database
==============

Items stored in an Axiom database keep an explicit reference to the Store that
they are a part of, rather than keeping an implicit store on the stack or in a
process-global location.  'Explicit is better than implicit'.  Again, other
popular tools make it difficult to share data between different databases.
