# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

"""
stuff to deal with comments and formatting on dict/list/ordereddict/set
these are not really related, formatting could be factored out as
a separate base
"""

import sys
from compat import MutableSet

__all__ = ["CommentedSeq", "CommentedMap", "CommentedOrderedMap",
           "CommentedSet", 'comment_attrib', 'merge_attrib']


try:
    from .compat import ordereddict
except ImportError:
    from ruamel.yaml.compat import ordereddict

comment_attrib = '_yaml_comment'
format_attrib = '_yaml_format'
line_col_attrib = '_yaml_line_col'
anchor_attrib = '_yaml_anchor'
merge_attrib = '_yaml_merge'
tag_attrib = '_yaml_tag'


class Comment(object):
    # sys.getsize tested the Comment objects, __slots__ make them bigger
    # and adding self.end did not matter
    attrib = comment_attrib

    def __init__(self):
        self.comment = None  # [post, [pre]]
        # map key (mapping/omap/dict) or index (sequence/list) to a  list of
        # dict: post_key, pre_key, post_value, pre_value
        # list: pre item, post item
        self._items = {}
        # self._start = [] # should not put these on first item
        self._end = []  # end of document comments

    def __str__(self):
        if self._end:
            end = ',\n  end=' + str(self._end)
        else:
            end = ''
        return "Comment(comment={0},\n  items={1}{2})".format(
            self.comment, self._items, end)

    @property
    def items(self):
        return self._items

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value


# to distinguish key from None
def NoComment():
    pass


class Format(object):
    attrib = format_attrib

    def __init__(self):
        self._flow_style = None

    def set_flow_style(self):
        self._flow_style = True

    def set_block_style(self):
        self._flow_style = False

    def flow_style(self, default=None):
        """if default (the flow_style) is None, the flow style tacked on to
        the object explicitly will be taken. If that is None as well the
        default flow style rules the format down the line, or the type
        of the constituent values (simple -> flow, map/list -> block)"""
        if self._flow_style is None:
            return default
        return self._flow_style


class LineCol(object):
    attrib = line_col_attrib

    def __init__(self):
        self.line = None
        self.col = None
        self.data = None

    def add_kv_line_col(self, key, data):
        if self.data is None:
            self.data = {}
        self.data[key] = data

    def key(self, k):
        return self._kv(k, 0, 1)

    def value(self, k):
        return self._kv(k, 2, 3)

    def _kv(self, k, x0, x1):
        if self.data is None:
            return None
        data = self.data[k]
        return data[x0], data[x1]

    def item(self, idx):
        if self.data is None:
            return None
        return self.data[idx][0], self.data[idx][1]

    def add_idx_line_col(self, key, data):
        if self.data is None:
            self.data = {}
        self.data[key] = data


class Anchor(object):
    attrib = anchor_attrib

    def __init__(self):
        self.value = None
        self.always_dump = False


class Tag(object):
    """store tag information for roundtripping"""
    attrib = tag_attrib

    def __init__(self):
        self.value = None


class CommentedBase(object):
    @property
    def ca(self):
        if not hasattr(self, Comment.attrib):
            setattr(self, Comment.attrib, Comment())
        return getattr(self, Comment.attrib)

    def yaml_end_comment_extend(self, comment, clear=False):
        if clear:
            self.ca.end = []
        self.ca.end.extend(comment)

    def yaml_key_comment_extend(self, key, comment, clear=False):
        l = self.ca._items.setdefault(key, [None, None, None, None])
        if clear or l[1] is None:
            if comment[1] is not None:
                assert isinstance(comment[1], list)
            l[1] = comment[1]
        else:
            l[1].extend(comment[0])
        l[0] = comment[0]

    def yaml_value_comment_extend(self, key, comment, clear=False):
        l = self.ca._items.setdefault(key, [None, None, None, None])
        if clear or l[3] is None:
            if comment[1] is not None:
                assert isinstance(comment[1], list)
            l[3] = comment[1]
        else:
            l[3].extend(comment[0])
        l[2] = comment[0]

    def yaml_set_start_comment(self, comment, indent=0):
        """overwrites any preceding comment lines on an object
        expects comment to be without `#` and possible have mutlple lines
        """
        from .error import Mark
        from .tokens import CommentToken
        pre_comments = self._yaml_get_pre_comment()
        if comment[-1] == '\n':
            comment = comment[:-1]  # strip final newline if there
        start_mark = Mark(None, None, None, indent, None, None)
        for com in comment.split('\n'):
            pre_comments.append(CommentToken('# ' + com + '\n', start_mark, None))

    @property
    def fa(self):
        """format attribute

        set_flow_style()/set_block_style()"""
        if not hasattr(self, Format.attrib):
            setattr(self, Format.attrib, Format())
        return getattr(self, Format.attrib)

    def yaml_add_eol_comment(self, comment, key=NoComment, column=None):
        """
        there is a problem as eol comments should start with ' #'
        (but at the beginning of the line the space doesn't have to be before
        the #. The column index is for the # mark
        """
        from .tokens import CommentToken
        from .error import Mark
        if column is None:
            column = self._yaml_get_column(key)
        if comment[0] != '#':
            comment = '# ' + comment
        if column is None:
            if comment[0] == '#':
                comment = ' ' + comment
                column = 0
        start_mark = Mark(None, None, None, column, None, None)
        ct = [CommentToken(comment, start_mark, None), None]
        self._yaml_add_eol_comment(ct, key=key)

    @property
    def lc(self):
        if not hasattr(self, LineCol.attrib):
            setattr(self, LineCol.attrib, LineCol())
        return getattr(self, LineCol.attrib)

    def _yaml_set_line_col(self, line, col):
        self.lc.line = line
        self.lc.col = col

    def _yaml_set_kv_line_col(self, key, data):
        self.lc.add_kv_line_col(key, data)

    def _yaml_set_idx_line_col(self, key, data):
        self.lc.add_idx_line_col(key, data)

    @property
    def anchor(self):
        if not hasattr(self, Anchor.attrib):
            setattr(self, Anchor.attrib, Anchor())
        return getattr(self, Anchor.attrib)

    def yaml_anchor(self):
        if not hasattr(self, Anchor.attrib):
            return None
        return self.anchor

    def yaml_set_anchor(self, value, always_dump=False):
        self.anchor.value = value
        self.anchor.always_dump = always_dump

    @property
    def tag(self):
        if not hasattr(self, Tag.attrib):
            setattr(self, Tag.attrib, Tag())
        return getattr(self, Tag.attrib)

    def yaml_set_tag(self, value):
        self.tag.value = value


class CommentedSeq(list, CommentedBase):
    __slots__ = [Comment.attrib, ]

    def _yaml_add_comment(self, comment, key=NoComment):
        if key is not NoComment:
            self.yaml_key_comment_extend(key, comment)
        else:
            self.ca.comment = comment

    def _yaml_add_eol_comment(self, comment, key):
        self._yaml_add_comment(comment, key=key)

    def _yaml_get_columnX(self, key):
        return self.ca.items[key][0].start_mark.column

    def insert(self, idx, val):
        """the comments after the insertion have to move forward"""
        list.insert(self, idx, val)
        for list_index in sorted(self.ca.items, reverse=True):
            if list_index < idx:
                break
            self.ca.items[list_index+1] = self.ca.items.pop(list_index)

    def pop(self, idx):
        res = list.pop(self, idx)
        self.ca.items.pop(idx, None)  # might not be there -> default value
        for list_index in sorted(self.ca.items):
            if list_index < idx:
                continue
            self.ca.items[list_index-1] = self.ca.items.pop(list_index)
        return res

    def _yaml_get_column(self, key):
        column = None
        sel_idx = None
        pre, post = key-1, key+1
        if pre in self.ca.items:
            sel_idx = pre
        elif post in self.ca.items:
            sel_idx = post
        else:
            # self.ca.items is not ordered
            for row_idx, k1 in enumerate(self):
                if row_idx >= key:
                    break
                if row_idx not in self.ca.items:
                    continue
                sel_idx = row_idx
        if sel_idx is not None:
            column = self._yaml_get_columnX(sel_idx)
        return column

    def _yaml_get_pre_comment(self):
        if self.ca.comment is None:
            pre_comments = []
            self.ca.comment = [None, pre_comments]
        else:
            pre_comments = self.ca.comment[1] = []
        return pre_comments


class CommentedMap(ordereddict, CommentedBase):
    __slots__ = [Comment.attrib, ]

    def _yaml_add_comment(self, comment, key=NoComment, value=NoComment):
        """values is set to key to indicate a value attachment of comment"""
        if key is not NoComment:
            self.yaml_key_comment_extend(key, comment)
            return
        if value is not NoComment:
            self.yaml_value_comment_extend(value, comment)
        else:
            self.ca.comment = comment

    def _yaml_add_eol_comment(self, comment, key):
        """add on the value line, with value specified by the key"""
        self._yaml_add_comment(comment, value=key)

    def _yaml_get_columnX(self, key):
        return self.ca.items[key][2].start_mark.column

    def _yaml_get_column(self, key):
        column = None
        sel_idx = None
        pre, post, last = None, None, None
        for x in self:
            if pre is not None and x != key:
                post = x
                break
            if x == key:
                pre = last
            last = x
        if pre in self.ca.items:
            sel_idx = pre
        elif post in self.ca.items:
            sel_idx = post
        else:
            # self.ca.items is not ordered
            for row_idx, k1 in enumerate(self):
                if k1 >= key:
                    break
                if k1 not in self.ca.items:
                    continue
                sel_idx = k1
        if sel_idx is not None:
            column = self._yaml_get_columnX(sel_idx)
        return column

    def _yaml_get_pre_comment(self):
        if self.ca.comment is None:
            pre_comments = []
            self.ca.comment = [None, pre_comments]
        else:
            pre_comments = self.ca.comment[1] = []
        return pre_comments

    def update(self, *vals, **kwds):
        try:
            ordereddict.update(self, *vals, **kwds)
        except TypeError:
            # probably a dict that is used
            for x in vals:
                self[x] = vals[x]

    def insert(self, pos, key, value, comment=None):
        """insert key value into given position
        attach comment if provided
        """
        ordereddict.insert(self, pos, key, value)
        if comment is not None:
            self.yaml_add_eol_comment(comment, key=key)

    def mlget(self, key, default=None, list_ok=False):
        """multi-level get that expects dicts within dicts"""
        if not isinstance(key, list):
            return self.get(key, default)
        # assume that the key is a list of recursively accessible dicts

        def get_one_level(key_list, level, d):
            if not list_ok:
                assert isinstance(d, dict)
            if level >= len(key_list):
                if level > len(key_list):
                    raise IndexError
                return d[key_list[level-1]]
            return get_one_level(key_list, level+1, d[key_list[level-1]])

        try:
            return get_one_level(key, 1, self)
        except KeyError:
            return default
        except (TypeError, IndexError):
            if not list_ok:
                raise
            return default

    def __getitem__(self, key):
        try:
            return ordereddict.__getitem__(self, key)
        except KeyError:
            for merged in getattr(self, merge_attrib, []):
                if key in merged[1]:
                    return merged[1][key]
            raise

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except:
            return default

    @property
    def merge(self):
        if not hasattr(self, merge_attrib):
            setattr(self, merge_attrib, [])
        return getattr(self, merge_attrib)

    def add_yaml_merge(self, value):
        self.merge.extend(value)


class CommentedOrderedMap(CommentedMap):
    __slots__ = [Comment.attrib, ]


class CommentedSet(MutableSet, CommentedMap):
    __slots__ = [Comment.attrib, 'odict']

    def __init__(self, values=None):
        self.odict = ordereddict()
        MutableSet.__init__(self)
        if values is not None:
            self |= values

    def add(self, value):
        """Add an element."""
        self.odict[value] = None

    def discard(self, value):
        """Remove an element.  Do not raise an exception if absent."""
        del self.odict[value]

    def __contains__(self, x):
        return x in self.odict

    def __iter__(self):
        for x in self.odict:
            yield x

    def __len__(self):
        return len(self.odict)

    def __repr__(self):
        return 'set({0!r})'.format(self.odict.keys())
