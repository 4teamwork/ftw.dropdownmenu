from Acquisition import aq_inner
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from Products.CMFPlone.browser.navtree import SitemapQueryBuilder
from Products.CMFPlone.browser.interfaces import ISiteMap
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from ftw.dropdownmenu.interfaces import IDropdownMenuSettings


def render_cachekey(method, self):
    """A cache key consisting of the viewlet name,
       the username and the current section.
    """
    context = aq_inner(self.context)
    portal_state = getMultiAdapter((context, self.request),
                                    name=u'plone_portal_state')
    navroot = portal_state.navigation_root()
    content_path = context.getPhysicalPath()[len(navroot.getPhysicalPath()):]
    section = content_path and content_path[0] or ''
    return '%s-%s-%s' % (self.__name__, portal_state.member(), section)


class DropdownMenuViewlet(common.GlobalSectionsViewlet):
    """
    """
    implements(ISiteMap)

    _template = ViewPageTemplateFile('dropdown.pt')
    recurse = ViewPageTemplateFile('dropdown_recurse.pt')

    def update(self):
        super(DropdownMenuViewlet, self).update()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IDropdownMenuSettings)
        self.columns_count = settings.columns
        self.enable_caching = settings.enable_caching
        self.properties = getToolByName(self.context, 'portal_properties').navtree_properties

    def createSubMenu(self, tab_id):
        sitemap = self.siteMap()
        sitemap_tabs = [item['id'] for item in sitemap['children']]
        try:
            sindex = sitemap_tabs.index(tab_id)
        except ValueError:
            return
        data = sitemap['children'][sindex]

        bottomLevel = self.properties.getProperty('bottomLevel', 0)

        return self.recurse(children=data.get('children', []), level=1, bottomLevel=bottomLevel)

    @memoize
    def siteMap(self):
        context = aq_inner(self.context)
        queryBuilder = SitemapQueryBuilder(context)
        query = queryBuilder()
        strategy = getMultiAdapter((context, self), INavtreeStrategy)
        strategy.showAllParents = False
        return buildFolderTree(context, obj=context, query=query, strategy=strategy)

    def render(self):
        if self.enable_caching:
            return self.cached_render()
        else:
            return xhtml_compress(self._template())

    @ram.cache(render_cachekey)
    def cached_render(self):
        return xhtml_compress(self._template())
    