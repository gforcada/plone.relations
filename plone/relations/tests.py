import unittest

from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite
from zope.app.testing import placelesssetup
from Testing import ZopeTestCase as ztc

# these are used by setup
from five.intid.site import add_intids
from five.intid.lsm import USE_LSM
from OFS.SimpleItem import SimpleItem

class Demo(SimpleItem):
    def __init__(self, obid):
        self.id = obid
    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.id)

def contentSetUp(app):
    for i in range(30):
        obid = 'ob%d' % i
        ob_object = Demo(obid)
        app._setObject(obid, ob_object)

def ChinatownSetUp(app):
    characters = ['jake', 'evelyn', 'noah', 'hollis', 'katherine',
                  'the past', 'investigation']
    for c in characters:
        app._setObject(c, Demo(c))

def setUp(app):
    # turn on all needed zcml
    placelesssetup.setUp()
    import Products.Five
    from Products.Five import zcml
    from plone import relations
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('permissions.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', relations)
    # Make a site, turn on the local site hooks, add the five.intid utility
    from zope.app.component.hooks import setSite, setHooks
    if not USE_LSM:
        from collective.testing.utils import monkeyAppAsSite
        monkeyAppAsSite()
    add_intids(app)
    setSite(app)
    setHooks()
    contentSetUp(app)

def tearDown():
    placelesssetup.tearDown()

optionflags = doctest.ELLIPSIS
def test_suite():
    # Zope 2 + Five Integration tests that use ZopeTestCase
    integration = ztc.FunctionalDocFileSuite('container.txt',
                                             optionflags=optionflags,
                                             package='plone.relations')
    readme = ztc.FunctionalDocFileSuite('README.txt',
                                        optionflags=optionflags,
                                        package='plone.relations')


    lazy = DocTestSuite('plone.relations.lazylist')

    return unittest.TestSuite((lazy, integration, readme))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
