=================
Divmod Combinator
=================

Combinator is a tool that Divmod Python programmers use to manage multiple
branches of our software. It integrates with Subversion.

It can be used to manage any number of branches with any number of projects.
It sets up your Python sys.path to point at the appropriate directories for
the set of branches you are currently working on. It also sets up your
``PATH`` environment variable so that you can access any scripts that come
along with those projects.

It is mainly of interest if you are checking code out of SVN: users of installed versions of Divmod software can probably ignore this project (for now).

.. _note: Combinator does not currently work with SVN version 1.2 due to
   changes in the way SVN stores its local repository. See #2144 for details.

Rationale
=========

Subversion is a nice development system, but some tasks are unnecessarily
difficult. In particular, as we migrated from CVS to SVN, we discovered that
there are some operations which were impractically difficult in CVS but simple
in SVN, such as creating branches, but while the implementation of managing
and merging branches was adequate, there were too much flexibility, and too
many ways to subtly incorrectly merge a branch.

As one example of such a problem, in SVN one must always pass the revision
where the branch was created on trunk as an argument to the merge command, and
determining that number involves reading the output of another long-running
command. Some branches cannot be merged in this manner, depending on where the
branch was originally created from.

We developed some idioms for avoiding common errors during merge and encoded
them in a set of shell scripts. Then we discovered another set of common
problems: often developers working on a branch would do a bunch of work, and
then find themselves mystified that their changes did not seem to be taking
effect, due to a mismatch between the environment of their development tools
and the shells where test commands were being run.

Combinator began as a set of idioms and shell scripts and has evolved into a
set of Python tools which enforce a simple workflow for using SVN and Python
together to work on projects that use branches to gather changes together
while eliminating common errors.

Download
========

Combinator is in the Divmod repository.

If you want to use it without the rest of the Divmod projects, see the
CombinatorTutorial.

Use
===

Start with [source:trunk/Combinator/README.txt README.txt] to get your
environment set up.

.. _note: If you follow the UNIX setup instructions and an exception is raised
   along the lines of `OSError: [Errno 2] No such file or directory:
   '/home/YOURNAME/.local/lib/python2.4/site-packages'`, you should update to
   the latest trunk revision of Combinator - this bug has been fixed!

CombinatorTutorial is a guide to typical Combinator use including setting up
an SVN repository to play with.

Reading about [wiki:UltimateQualityDevelopmentSystem our development process]
is likely to give you some insight into how it's intended to be used.

chbranch
========

**chbranch** is the tool for switching to a different branch. Provide
``chbranch`` with a *project name* and *branch name* and it will modify all
Combinator-enabled environments so that Python imports are satisfied from that
branch of the project. If necessary, the branch will be checked out.

mkbranch
========

**mkbranch** is the tool for creating new branches. Provide ``mkbranch`` with
a *project name* and *branch name* and it will create a new branch with that
name, switch a copy of trunk to it, and do the equivalent of a ``chbranch`` to
the new branch.

unbranch
========

**unbranch** is the tool for merging a branch's changes into trunk. First, use
``chbranch`` to change to the branch to be merged. Then, make sure that the
trunk working copy either contains no changes or contains only changes which
you want included in the merge (note: it is strongly, strongly recommended
that if the merge will be committed that the trunk working copy contain no
changes). Finally, run ``unbranch`` with the *project name* and the changes
from the branch will be merged into the trunk working copy. They will not be
committed automatically.
