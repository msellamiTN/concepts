# test_contexts.py

import pytest

from concepts.contexts import Context


def test_duplicate_object():
    with pytest.raises(ValueError):
        Context(('spam', 'spam'), ('ham', 'eggs'), [(True, False), (False, True)])


def test_duplicate_property():
    with pytest.raises(ValueError):
        Context(('spam', 'eggs'), ('ham', 'ham'), [(True, False), (False, True)])


def test_object_property_overlap():
    with pytest.raises(ValueError):
        Context(('spam', 'eggs'), ('eggs', 'ham'), [(True, False), (False, True)])


def test_empty_relation():
    with pytest.raises(ValueError):
        Context((), ('spam',), [(False,)])
    with pytest.raises(ValueError):
        Context(('spam',), (), [(False,)])


def test_invalid_bools():
    with pytest.raises(ValueError):
        Context(('spam', 'eggs'), ('camelot', 'launcelot'), [(True, False)])
    with pytest.raises(ValueError):
        Context(('spam', 'eggs'), ('camelot', 'launcelot'), [(True, False, False), (False, True)])


def test_init():
    c = Context(('spam', 'eggs'), ('camelot', 'launcelot'),
                [(True, False), (False, True)])
    assert c.objects == ('spam', 'eggs')
    assert c.properties == ('camelot', 'launcelot')
    assert c.bools == [(True, False), (False, True)]


@pytest.fixture(scope='module')
def context():
    source = '''
       |+1|-1|+2|-2|+3|-3|+sg|+pl|-sg|-pl|
    1sg| X|  |  | X|  | X|  X|   |   |  X|
    1pl| X|  |  | X|  | X|   |  X|  X|   |
    2sg|  | X| X|  |  | X|  X|   |   |  X|
    2pl|  | X| X|  |  | X|   |  X|  X|   |
    3sg|  | X|  | X| X|  |  X|   |   |  X|
    3pl|  | X|  | X| X|  |   |  X|  X|   |
    '''
    return Context.fromstring(source)


def test_eq(context):
    assert context == Context(context.objects, context.properties, context.bools)


def test_eq_undefined(context):
    assert not (context == object())


def test_ne(context):
    assert context != Context(('spam', 'eggs'), ('camelot', 'launcelot'), [(True, False), (False, True)])


def test_minimize_infimum(context):
    assert list(context._minimize((), context.properties)) == [context.properties]


def test_raw(context):
    Extent, Intent = context._Extent, context._Intent
    assert context.intension(['1sg', '1pl'], raw=True) == Intent('1001010000')
    assert context.extension(['+1', '+sg'], raw=True) == Extent('100000')
    assert context.neighbors(['1sg'], raw=True) == \
        [(Extent('110000'), Intent('1001010000')),
         (Extent('101000'), Intent('0000011001')),
         (Extent('100010'), Intent('0001001001'))]


def test_unicode(context):
    assert all(ord(c) < 128 for c in str(context))
    assert u'%s' % context == '%s' % context
