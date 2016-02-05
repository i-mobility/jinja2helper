import datetime
from dateutil import parser
from jinja2.ext import Extension


def timestampformat(value, format='%A, %d.%m.%Y'):
    ts_s = value / 1000
    return datetime.datetime.fromtimestamp(ts_s).strftime(format)


def datestringformat(value, format='%d.%m.%Y'):
    date = parser.parse(value)
    return date.strftime(format)


def cent(value, format=u'{0:,.2f} \u20ac'):
    return format.format(value / 100.0).replace('.', ',')


class Filters(Extension):
    """ Extension to register custom filters
    """

    def __init__(self, env):
        env.filters['timestampformat'] = timestampformat
        env.filters['datestringformat'] = datestringformat
        env.filters['cent'] = cent
