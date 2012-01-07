===============
Getting started
===============

.. note:: This is incomplete documentation in progress.


Getting Started: A basic page
=============================


Currently the `nevow.rend` module contains the Page class which should be
subclassed to create new pages. A page is the added as a child of the root page,
or it's instantiation can be defined in a `childFactory` or `child_` special
method.  `rend.Page` contains the context which is slowly being removed and will
soon be replaced by `page.Page` which should be easily adaptable.

We will construct a page that returns 'Hello world!', and propose some
structural alternatives.


.. code-block:: python

    from nevow import rend, loaders, tags

    class APage(rend.Page):
        docFactory = loaders.stan(tags.html[
            tags.head[
                tags.title['Hello World Example']
            ],
            tags.body[
                tags.div(id='hello', _class='helloicator')['Hello World!']
            ]
        ])

This page uses Stan to construct an object-like representation which is
flattened into XHTML.

Rendering can also dispatch methods inside the page class known as render
specials.



.. code-block:: python

    from nevow import rend, loaders, tags

    class APage(rend.Page):
        docFactory = loaders.stan(tags.html[
            tags.head[
                tags.title['Hello World Example']
            ],
            tags.body[
                tags.div(render=tags.directive('hi'))
            ]
        ])

        def render_hi(self, ctx, data):
            return ctx.tag[ tags.div(id='hello', _class='helloicator')['Hello World']]




Putting it together
===================

To put it together as a deployable application all we really need is an
application servlet.

A compact example of a boiler plate Nevow application could look like this


.. code-block:: python

    # Page modules
    from nevow import rend, loaders, tags

    # Deployment modules
    from nevow import appserver
    from twisted.application import service, internet

    class APage(rend.Page):
        addSlash = True

        docFactory = loaders.stan(tags.html[
            tags.head[
                tags.title['Hello World Example']
            ],
            tags.body[
                tags.div(render=tags.directive('hi'))
            ]
        ])

        def render_hi(self, ctx, data):
            return ctx.tag[ tags.div(id='hello', _class='helloicator')['Hello World']]


    siteRoot = APage() # Set our page as the site root
    site = appserver.NevowSite(siteRoot)

    demo = internet.TCPServer(8080, site)

    application = service.Application('demo')
    demo.setServiceParent(application)


It's common to encapsulate the specific service in a deployment function as
follows

.. code-block:: python

    # Page modules
    from nevow import rend, loaders, tags

    # Deployment modules
    from nevow import appserver
    from twisted.application import service, internet

    class APage(rend.Page):
        addSlash = True

        docFactory = loaders.stan(tags.html[
            tags.head[
                tags.title['Hello World Example']
            ],
            tags.body[
                tags.div(render=tags.directive('hi'))
            ]
        ])

        def render_hi(self, ctx, data):
            return ctx.tag[ tags.div(id='hello', _class='helloicator')['Hello World']]

    def deployApp():
        siteRoot = APage() # Set our page as the site root
        site = appserver.NevowSite(siteRoot)
        return site

    demo = internet.TCPServer(8080, deployApp())

    application = service.Application('demo')
    demo.setServiceParent(application)


The server can be started by issuing the command ``twistd -ny simple.py``.

.. note:: It is possible to attach multiple sites and protocol servers to a
    single service parent.
