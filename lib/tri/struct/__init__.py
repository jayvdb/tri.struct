
__version__ = '2.0'


class Struct(dict):
    """
    A dict where keys can also be accessed as attributes.
    """
    def __init__(self, *args, **kwargs):
        Struct.__setattr__(self, '__dict__', self)
        super(Struct, self).__init__(*args, **kwargs)

    def copy(self):
        return type(self)(self)

    def __unicode__(self):
        return u'%s(%s)' % (type(self).__name__, u', '.join([u'%s=%r' % (key, self[key]) for key in sorted(self.keys())]))

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, ', '.join(['%s=%r' % (key, self[key]) for key in sorted(self.keys())]))

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, item))


class FrozenStruct(Struct):

    def __hash__(self):
        try:
            _hash = self['_hash']
        except KeyError:
            _hash = hash(tuple((k, self[k]) for k in sorted(self.keys())))
            dict.__setitem__(self, '_hash', _hash)
        return _hash

    def __setitem__(self, *_, **__):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__, ))

    def __setattr__(self, key, value):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__,))

    def setdefault(self, *_, **__):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__, ))

    def update(self, *_, **__):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__, ))

    def clear(self, *_, **__):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__, ))

    def __delitem__(self, *_, **__):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__, ))

    def __delattr__(self, *_, **__):
        raise TypeError("'%s' object attributes are read-only" % (type(self).__name__,))

    def __reduce__(self):
        return type(self), (), dict(self)

    def __setstate__(self, state):
        dict.update(self, state)
