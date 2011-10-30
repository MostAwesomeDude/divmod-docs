= What Happens When A Browser Requests a Web Page From Mantissa =

This is a step-by-step guide explaining which classes are involved and what they do, with a heavy emphasis on how they interact with application code and plugins.  I'm tired of working this out from scratch every time I'm trying to maintain the system - hopefully this will become simpler over time.

== Wrappers at the Root ==

We start at what the port is bound to: the object that comes back from `xmantissa.web.SiteConfiguration.getFactory`.

This is a `SecuringWrapper` wrapped around an `UnguardedWrapper` wrapped around a `PersistentSessionWrapper`, which ultimately wraps the portal provided by the store, an axiom `LoginSystem`.  One step at a time:

`xmantissa.web.SecuringWrapper` has the job of redirecting to HTTPS if the ultimate target resource stipulates that it is a requirement.  This inspects the (almost entirely undocumented) `needsSecure` attribute on the `IResource` which is ultimately looked up, by wrapping each intermediary `locateChild` result in a `_SecureWrapper`.  For most purposes you can ignore this.

== Sessionless Plugins ==

`xmantissa.web.UnguardedWrapper` is responsible for providing access to resources which do not require a session.  This statically provides the URL hierarchies under `/Mantissa`, `/__jsmodule__`, and `/static`.  It will also do a powerup query for `ISessionlessSiteRootPlugin` on the site store.  If there are any sessionless plugins, they will always take priority, since this is the first foray that the resource lookup makes into application code.  However, by default, no sessionless plugins are installed.  You can verify this by running `axiomatic web --list` on your mantissa database and looking at the 'Sessionless plugins:' section.

== Sessions and Authentication ==

Next, the `PersistentSessionWrapper` gets involved.  This is in charge of sessions and authentication.  This has a lot of internal behavior regarding setting up a session and redirecting the user; this means that for any path except the three mentioned above (`/Mantissa`, `/__jsmodule__`, `static`) your browser will be redirected if it doesn't have a cookie.  (This needs to be fixed somehow so that we can provide access to APIs like XMLRPC or data like RSS for dumb user-agents that can't handle cookies, authentication, or maybe even redirects.)

Internally the `PersistentSessionWrapper` has only one code path: it logs in the user using some set of credentials, and then presents the root resource as the avatar that was retrieved for those credentials.  However, given that all sessions begin by presenting credentials that say 'I'm anonymous', there are effectively two things that it can do: show you the anonymous site or show you a logged-in site.  This relies on the fact that when `axiom.userbase.LoginSystem` is presented with anonymous credentials, the avatar that it returns is the site store.

== Anonymous Sessions (the public site) ==

The anonymous `IResource` root, which is to say the site store's `IResource` powerup, as installed by `axiom.plugins.baseoff`, is `xmantissa.publicweb.AnonymousSite`.  It uses powerup indirection to provide an in-memory avatar, `xmantissa.website.VirtualHostWrapper`, which provides per-user subdomain dispatch; i.e. http://youruser.mantissa.example.com/ will resolve to the same resource as http://mantissa.example.com/users/youruser/.

Continuing down anonymous resource lookup, `AnonymousSite` statically provides 3 features itself: `/login`, `/resetPassword`, and `/users`.

`/users/` is handled by `xmantissa.websharing.UserIndexPage`, which wraps a `xmantissa.websharing.SharingIndex` around each users' store, exposing the items that they have shared.  When viewed by anonymous users, shared items are (somewhat obviously) retrieved using the role returned by `getEveryoneRole`.  See below for customization.

It also does a powerup query for `ISiteRootPlugin`; i.e. sessioned site root plugins.  By default, Mantissa installs one site root plugin powerup: `xmantissa.publicweb.FrontPage`.  `FrontPage` handles just that, the display of the front page which appears at <http://mantissa.example.com/>.  Normally it renders a Divmod logo and a list of installed offerings, but it can be configured to render the front page of one particular offering by way of the `axiomatic offering frontpage` plugin.  `PublicFrontPage` also looks up each offering in turn, providing a URL hierarchy under that offering's name by providing a sharing index.  For example, if the `Quotient` offering has shared an item called `divisor`, `PublicFrontPage` is the object that returns it to show up at <http://mantissa.example.com/Quotient/divisor>.

== Authenticated Sessions ==

Starting once again inside `PersistentSessionWrapper`, i.e. after `ISessionlessSiteRootPlugin` objects on the site store have been looked up, we begin at `xmantissa.website.WebSite`, which is the authenticated version of `xmantissa.publicweb.AnonymousSite`.  It also implements `IResource`, and similarly indirects via `VirtualHostWrapper` to support username subdomains.  (Note: `SiteRootMixin`'s docstring is completely wrong, it's only used for the private hierarchy now, there's only the one subclass and no tests or other usages anywhere.)  `WebSite` has its own implementation of `/resetPassword`, which attempts to redirect to the user's settings page.  (This is broken, as per #2358.)

`WebSite` then makes a query for `ISiteRootPlugin` in the ''user'' store of the user who is viewing it.  There are two plugins which are typically found: `xmantissa.webapp.PrivateApplication`, and `xmantissa.publicweb.CustomizedPublicPage`, which it depends on.

`PrivateApplication` is responsible for rendering the hierarchy under `/private` for logged-in users.  These URLs are all opaque, but can be accessed by clicking on the tabs that are installed by various applications.  Also, `PrivateApplication` provides a redirect from `/private` to the object indicated by the first 'tab' that the navigation system can find.  (The navigation system is out of scope here, see `xmantissa.ixmantissa.INavigableElement` and `xmantissa.webnav`.)

`PrivateApplication` maps an opaque identifier to a storeID, looks up the item with that storeID, first adapts it to `IResource`, or if no `IResource` is found, then it adapts the item to `INavigableElement`.

Finally, the thing that allows a user to see the pieces of the public site described above - the `/users/` hierarchy, app store pages at `/NameOfApplication`, and sessioned plugins on the site, is `CustomizedPublicPage`.

The content which is normally available to the public might look different once you're logged in.  For example, content shared through the [wiki:DivmodMantissa/Sharing sharing system] needs to know which role is viewing it.  `CustomizedPublicPage` does this by looking up the `IResource` provider of the parent store, then wrapping each returned resource in a `_CustomizingResource`.


