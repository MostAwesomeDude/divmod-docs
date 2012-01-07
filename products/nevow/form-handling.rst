===========================================================
Form Handling (A summary of Nevow form handling techniques)
===========================================================


There is more than one way to correctly handle forms in Nevow. This short
tutorial demonstrates three Nevow form handling techniques. It includes some
real world problems and (hopefully) demonstrates the most appropriate form
handling recipe to use in each case.

Examples are included on separate wiki pages for clarity and to make it easy for
the reader to download and run them. Where example files end in .tac.py, the
example should be run as twistd -noy Example.tac.py. Some screenshots are
provided so that you can quickly see the output of the examples.



Automatic Form Generation and Handling
======================================

Form handling is one of the most tedious parts of developing a web application.
Fortunately there are two sophisticated form handling libraries available for
Nevow; :doc:`formless` and `Pollenation Forms
<http://forms-project.pollenation.net/>`_. Both offer automatic form generation,
validation and type coercion.

Formless is older and comes bundled with Nevow but can be confusing for
beginners and frustrating for more experienced users. That said, it is highly
customisable and allows html coder to precisely layout the form while still
taking advantage of the automatic validation and type coercion.

Pollenation Forms is both simpler for the beginner and offers powerful features
for the experienced user. It is the recommended form handling library for those
who do not need precise customisation of the form layout in the document
template.



The Simplest Form - Example 1: A News Item Editor Page
======================================================

The following example demonstrates and compares the simplest use of Formless /
Pollenation Forms.  We start with a `basic tac file (src)
<attachment:Example1.0.tac>`_ containing everything but the form:

 * the rend.Page subclass and docFactory
 * a simple list to store news items
 * a data_* method to expose the list of stories to the template
 * a method to save new items to the database which redirects to a completion
   page on success

 * `Formless Recipe (src): <attachment:Example1.1.tac.py>`_ To expose the
   method (saveNewsItem) in our web page with Formless we:

   * import `annotate <source:trunk/Nevow/formless/annotate.py>`_ and
     `webform <source:trunk/Nevow/formless/webform.py>`_
   * update the template to include form layout css and a placeholder
     (<n:invisible />) for our form renderer
   * add the Formless standard css file as a `static.File
     <source:trunk/Nevow/nevow/static.py#L144>`_ child resource * define a
     corresponding bind_saveNewsItem method whose job is to return a description
     of the saveNewsItem method arguments
   * define a custom renderer which adds the results of webform.renderForms() to
     the page output.

* *`Pollenation Forms Recipe (src): <attachment:Example1.2.tac.py>`_* With
  Pollenation Forms we:

   * import
     `forms <http://forms-project.pollenation.net/cgi-bin/trac.cgi/browser/trunk/forms/__init__.py>`_
   * mixin the `forms.ResourceMixin
     <http://forms-project.pollenation.net/cgi-bin/trac.cgi/browser/trunk/forms/form.py#L303>`_
     to our rend.Page subclass.
   * update the template to include form layout css and a placeholder for our
     form renderer (forms.ResourceMixin defines its own render_form method so we
     use that)
   * update our saveNewsItem method to accommodate the extra args that forms
     will pass to it.
   * define a special form_* method which builds and returns the form.

A comparison of the two recipes:
 * Pollenation Forms API is more transparent (subjective of course, but
   generally accepted).
 * Pollenation Forms generates cleaner html.
 * Pollenation Forms form interface is more usable and provides clearer feedback
   messages. (ie 'Submit' button rather than the Formless 'Call'. Why?
   Especially when the new Formless bind_* methods make it such a rigmarole to
   customise the button...but more on that later.)
 * Pollenation Forms default rendered form looks prettier (again subjective)
   though in both cases, the generated html is sprinkled generously with class
   and id attributes so that by adding your own CSS you can transform the way
   the form looks.

So that looks like a pretty ringing endoresment of Pollenation Forms, but it
must be remembered that this is a comparison of what the two libraries produce
by default in very simple case. Equally important is how they can be extended
and customised to fit your application, and that's what we start looking at
next.

 * :doc:`nevow-form-handling-formless`
 * :doc:`nevow-form-handling-pollenation-forms`



Manual Form Handling
====================

Sometimes a form is so simple that it is easiest to write the form html by hand
and handle the result manually. The following code demonstrates a  form with
which the user can choose his preferred number of items per page in a datagrid.

.. todo:: find ManualFormHandlingExample.tac.py file

.. .. include:: ManualFormHandlingExample.tac.py

The <select> tag has a javascript onchange handler to automatically submit its
parent form and is presented inline with the content of its parent <p> tag. To
achieve this automatically using webform.renderForms() would have required
defining a custom form template with custom patterns etc (see later example).

(It should be noted that Formless or Pollenation Forms could be used here for
automatic coercion and validation of the form variables without employing their
form rendering machinery. An example of this may be added later.)
