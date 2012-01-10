===============
Demo: news edit
===============

.. code-block:: python

    from twisted.application import service, strports
    from nevow import appserver, loaders, rend, static, url

    class NewsEditPage(rend.Page):
        docFactory = loaders.xmlstr('''
    <!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN'
               'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
    <html xmlns:n='http://nevow.com/ns/nevow/0.1'>
        <head>
            <title>Example 1: A News Item Editor</title>
            <link rel='stylesheet' href='form_css' type='text/css' />
        </head>
        <body>
            <h1>Example 1: A News Item Editor</h1>
            <fieldset>
                <legend>Add / Edit News Item</legend>
                <p>Form Goes Here</p>
            </fieldset>

            <ol n:render='sequence' n:data='newsItems'>
                <li n:pattern='item' n:render='mapping'>
                    <strong><n:slot name='title' /></strong>: <n:slot name='description' />
                </li>
            </ol>
        </body>
    </html>
    ''')

        def __init__(self, *args, **kwargs):
            self.store = kwargs.pop('store')

        def saveNewsItem(self, newsItemData):
            self.store.append(newsItemData)
            return url.here.click('confirmation')

        def data_newsItems(self, ctx, name):
            return self.store

    class ConfirmationPage(rend.Page):
        docFactory = loaders.xmlstr('''
    <!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN'
               'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
    <html>
        <body>
            <h1>Your item has been saved</h1>
            <ul>
                <li><a href='./'>Go back</a></li>
            </ul>
        </body>
    </html>
    ''')

    # A place to store news items. A list of dicts in this simple case.
    store = [dict(title='Lorum Ipsum', description='''
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Sed sed enim mollis
    nulla faucibus aliquet. Praesent nec nibh. Nam eget pede. Nam tincidunt purus id
    lorem. Vestibulum lectus nisl, molestie vitae, feugiat egestas, sodales et,
    tellus. Vivamus eu libero. Nulla facilisi. Nullam nec dolor. Proin ac diam at
    neque auctor pulvinar. Maecenas eros nibh, fermentum at, eleifend at, malesuada
    eu, nunc. Sed posuere felis eu ipsum. In volutpat. Phasellus viverra. Quisque
    dignissim mattis turpis. Maecenas accumsan ipsum vel orci. Cras ac lectus. Sed
    nec nisl. Integer iaculis elit scelerisque sapien. Curabitur ac diam.
    ''')]

    rootResource = NewsEditPage(store=store)
    rootResource.putChild('confirmation', ConfirmationPage())

    application = service.Application('News item editor')
    strports.service('8080', appserver.NevowSite(rootResource)).setServiceParent(application)
