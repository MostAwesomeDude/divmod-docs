===============
Examples : Shop
===============


.. code-block:: python

    from zope.interface import Interface, implements

    from axiom.attributes import AND, OR
    from axiom import item, attributes, sequence
    from epsilon.extime import Time

    class Person(item.Item):
        '''A person here is not specific to the shopping part of the application.
        It may have been defined elsewhere eg during registration for an enquiries system.
        We can't subclass Person but we can plugin our shop specific attributes and methods using
        the Axiom powerup pattern.
        '''

        typeName = 'Person'
        schemaVersion = 1

        name = attributes.text(allowNone=False)
        dob = attributes.timestamp(allowNone=False)

        def __repr__(self):
            return '<Person name='%s' dob='%s'>' % (self.name, self.dob.asISO8601TimeAndDate())

    class IShopCustomer(Interface):
        pass

    class ShopCustomer(item.Item):
        '''A ShopCustomer is a powerup for person.'''
        implements(IShopCustomer)

        typeName = 'ShopCustomer'
        schemaVersion = 1

        installedOn = attributes.reference()

        def installOn(self, other):
            assert self.installedOn is None, 'cannot install ShopCustomer on more than one person'
            self.installedOn = other
            other.powerUp(self, IShopCustomer)

        '''Customer specific methods'''
        def getProductsOrdered(self):
            # An example of an inner join query
            return self.store.query(
                ShopProduct,
                AND(
                    ShopOrder.customer == self.installedOn,
                    ShopProductOrdered.order==ShopOrder.storeID,
                    ShopProductOrdered.product==ShopProduct.storeID
                )
            )

        def getOrders(self):
            return self.store.query(
                ShopOrder,
                ShopOrder.customer == self.installedOn
            )

    class ShopProduct(item.Item):
        typeName = 'ShopProduct'
        schemaVersion = 1

        name = attributes.text(allowNone=False)
        price = attributes.integer(allowNone=False)
        stock = attributes.integer(default=0)

        def __repr__(self):
            return '<ShopProduct name='%s' price='%d' stock='%d'>' % (self.name, self.price, self.stock)

    class ShopProductOrdered(item.Item):
        '''Links a product and quantity of product to an order.'''
        typeName = 'ShopProductOrdered'
        schemaVersion = 1

        order = attributes.reference(allowNone=False)
        product = attributes.reference(allowNone=False)
        quantity = attributes.integer(default=1)

    class ShopOrder(item.Item):
        typeName = 'ShopOrder'
        schemaVersion = 1

        customer = attributes.reference(allowNone=False)
        purchaseDate = attributes.timestamp(allowNone=False)

        def __init__(self, **kw):
            IShopCustomer(kw['customer'])
            super(ShopOrder, self).__init__(**kw)

        def addProduct(self, product, quantity=1):
            po = self.store.findOrCreate(
                ShopProductOrdered,
                order=self,
                product=product)
            po.quantity = quantity

        def getProducts(self):
            return self.store.query(ShopProductOrdered, ShopProductOrdered.order == self)

        def getTotalPrice(self):
            #XXX: Axiom will issue multiple queries here, but it could be done in one SQL query. Is there a way to issue such a query?
            total = 0
            for p in self.getProducts():
                total += p.product.price*p.quantity
            return total

        def __repr__(self):
            return '<ShopOrder customer='%s' purchaseDate='%s' items='%s'>' % (self.customer.name, self.purchaseDate.asISO8601TimeAndDate(), self.items)

    def populateStore(s):

        customerDetails = [
            (u'Joe Bloggs', '1977-05-08'),
            (u'Jane Doe', '1959-05-22'),
        ]

        for name, dob in customerDetails:
            p = Person(store=s, name=name, dob=Time.fromISO8601TimeAndDate(dob))

            # This is where we powerup the Person with additional ShopCustomer bits
            ShopCustomer(store=s).installOn(p)

        products = [
            ShopProduct(store=s, name=u'Tea Bags', price=2),
            ShopProduct(store=s, name=u'Cornflakes', price=3),
            ShopProduct(store=s, name=u'Lemonade', price=4),
            ShopProduct(store=s, name=u'Peanuts', price=5),
        ]

        quantities = [1,2,4]

        for c in s.query(ShopCustomer):
            o = ShopOrder(store=s, customer=c.installedOn, purchaseDate=Time())
            o.addProduct(random.choice(products), random.choice(quantities))
            o.addProduct(random.choice(products), random.choice(quantities))

    if __name__ == '__main__':
        import random
        from axiom import store

        s = store.Store(debug=False)
        populateStore(s)

        '''We only want a Person who is also a ShopCustomer.
        We therefore search for ShopCustomer but grab a reference to the person within (installedOn)
        When you want the person reference to behave like a shopcustomer
        adapt it to the IShopCustomer interface'''
        p = s.findFirst(ShopCustomer).installedOn

        print [x.name for x in IShopCustomer(p).getProductsOrdered()]
        print '%s has ordered the following products since registering:' % p.name

        print 'A breakdown of %s's orders' % p.name
        print ['Items: %s, Total: %d'%(['%s X %d'%(y.product.name, y.quantity) for y in x.getProducts()], x.getTotalPrice()) for x in IShopCustomer(p).getOrders()]
