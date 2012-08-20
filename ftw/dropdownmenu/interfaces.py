from zope.interface import Interface
from zope import schema


class IProductLayer(Interface):
    """A layer specific to this product
    """


class IDropdownMenuSettings(Interface):
    """
    """
    columns = schema.Int(
        title=u"Number of Columns",
        default=3,
    )

    # depth = schema.Int(
    #     title=u"Depth",
    #     default=2,
    # )

    enable_caching = schema.Bool(
        title = u'Enable Caching',
        description = u'',
        required = False,
        default = False,
    )