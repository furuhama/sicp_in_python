class Rlist(object):
    class EmptyList(object):
        def __len__(self):
            return 0

    empty = EmptyList()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        args = repr(self.first)
        if self.rest is not Rlist.empty:
            args += ', {0}'.format(repr(self.rest))
        return 'Rlist({0})'.format(args)

    def __len__(self):
        return 1 + len(self.rest)

    def __getitem__(self, i):
        if i == 0:
            return self.first
        return self.rest[i-1]

def extend_rlist(s1, s2):
    if s1 is Rlist.empty:
        return s2
    return Rlist(s1.first, extend_rlist(s1.rest, s2))

def map_rlist(s, fn):
    if s is Rlist.empty:
        return s
    return Rlist(fn(s.first), map_rlist(s.rest, fn))

def filter_rlist(s, fn):
    if s is Rlist.empty:
        return s
    rest = filter_rlist(s.rest, fn)
    if fn(s.first):
        return Rlist(s.first, rest)
    return rest

"""
Use Rlist as if it is a Set
"""

def empty(s):
    return s is Rlist.empty

def set_contains(s, element):
    if empty(s):
        return False
    elif s.first == element:
        return True
    return set_contains(s.rest, element)

def adjoin_set(s, element):
    if set_contains(s, element):
        return s
    return Rlist(element, s)

#  not fast ver.
#  def intersect_set(s1, s2):
#      return filter_rlist(s1, lambda element: set_contains(s2, element))

def intersect_set(s1, s2):
    if empty(s1) or empty(s2):
        return Rlist.empty
    e1, e2 = s1.first, s2.first
    if e1 == e2:
        return Rlist(e1, intersect_set(s1.rest, s2.rest))
    elif e1 < e2:
        return intersect_set(s1.rest, s2)
    elif e2 < e1:
        return intersect_set(s1, s2.rest)

def union_set(s1, s2):
    in_s1_not_in_s2 = filter_rlist(s1, lambda element: not set_contains(s2, element))
    return extend_rlist(in_s1_not_in_s2, s2)
