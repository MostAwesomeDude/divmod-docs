=====================
Transition mini-HOWTO
=====================


Notes
=====

A few bullet points with stuff to do transitioning from pre-dependency code to the new API(s).

* ``axiom.item.InstallableMixin`` has been removed since it is unnecessary, as
  is the ``installedOn`` attribute that was on subclasses thereof.
  ``powerup.installedOn()`` is now spelled
  ``axiom.dependency.installedOn(powerup)``.
* ``powerup.installOn(target)`` is now spelled
  ``axiom.dependency.installOn(powerup, target)``. See also
  ``axiom.dependency.uninstallFrom(powerup, target)``.
* Instead of explicitly powering the target up in ``installOn``, set the
  ``powerupInterfaces`` class attribute to a sequence of interfaces, or of
  ``(interface, priority)`` tuples.
* If you are implementing ``INavigableElement``, you need something like:


.. code-block:: python

    privateApplication = dependsOn(PrivateApplication)

* Declare other dependencies of your powerups as appropriate.
* Get rid of your ``Benefactor`` / ``BenefactorFactory`` classes, and instead
  pass an ``installablePowerups`` sequence when constructing your offering. For
  example:


.. code-block:: python

    installablePowerups = [
        (u'Operator admin', u'Operator administration', OperatorAdmin),
        (u'Reports', u'Data reporting functionality', Reports),
        ]

* TODO: writing upgraders


Example
=======

``xmantissa.webapp`` was migrated as `part of this change
<http://divmod.org/trac/changeset/10877#file115>`_. That serves as a good
example, and will be (incompletely) presented below as a demonstration. The
examples below elide most of the code and focus just on the changes. Please
refer to the different file versions themselves for a complete representation.

Before (`reference`__):

__ http://divmod.org/trac/browser/trunk/Mantissa/xmantissa/webapp.py?rev=10508#L432

::


    class PrivateApplication(Item, PrefixURLMixin):
        ...
        implements(ISiteRootPlugin, IWebTranslator)
        ...
        installedOn = reference()
        ...
        def installOn(self, other):
            super(PrivateApplication, self).installOn(other)
            other.powerUp(self, IWebTranslator)

            def findOrCreate(*a, **k):
                return other.store.findOrCreate(*a, **k)

            findOrCreate(StaticRedirect,
                         sessioned=True,
                         sessionless=False,
                         prefixURL=u'',
                         targetURL=u'/'+self.prefixURL).installOn(other, -1)

            findOrCreate(CustomizedPublicPage).installOn(other)

            findOrCreate(AuthenticationApplication)
            findOrCreate(PreferenceAggregator).installOn(other)
            findOrCreate(DefaultPreferenceCollection).installOn(other)
            findOrCreate(SearchAggregator).installOn(other)
        ...




After (`reference`__):

__ http://divmod.org/trac/browser/trunk/Mantissa/xmantissa/webapp.py?rev=10877#L433

::

    class PrivateApplication(Item, PrefixURLMixin):
        ...
        implements(ISiteRootPlugin, IWebTranslator)
        ...
        powerupInterfaces = (IWebTranslator,)
        ...
        customizedPublicPage = dependsOn(CustomizedPublicPage)
        authenticationApplication = dependsOn(AuthenticationApplication)
        preferenceAggregator = dependsOn(PreferenceAggregator)
        defaultPreferenceCollection = dependsOn(DefaultPreferenceCollection)
        searchAggregator = dependsOn(SearchAggregator)
