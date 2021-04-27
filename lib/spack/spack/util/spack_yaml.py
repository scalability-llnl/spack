# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Enhanced YAML parsing for Spack.

- ``load()`` preserves YAML Marks on returned objects -- this allows
  us to access file and line information later.

- ``Our load methods use ``OrderedDict`` class instead of YAML's
  default unorderd dict.

"""
import ctypes
import re
import sys
from typing import List  # novm

from ordereddict_backport import OrderedDict
from six import string_types, StringIO

import ruamel.yaml as yaml
from ruamel.yaml import RoundTripLoader, RoundTripDumper

from llnl.util.tty.color import colorize, clen, cextra

import spack.error


if sys.version_info >= (3, 3):
    from collections.abc import Mapping  # novm
else:
    from collections import Mapping


# Only export load and dump
__all__ = ['load', 'dump', 'SpackYAMLError']

# Make new classes so we can add custom attributes.
# Also, use OrderedDict instead of just dict.


class syaml_dict(OrderedDict):
    def __repr__(self):
        mappings = ('%r: %r' % (k, v) for k, v in self.items())
        return '{%s}' % ', '.join(mappings)


class syaml_list(list):
    __repr__ = list.__repr__


class syaml_str(str):
    __repr__ = str.__repr__


class syaml_int(int):
    __repr__ = int.__repr__


#: mapping from syaml type -> primitive type
syaml_types = {
    syaml_str: string_types,
    syaml_int: int,
    syaml_dict: dict,
    syaml_list: list,
}


markable_types = set(syaml_types) | set([
    yaml.comments.CommentedSeq,
    yaml.comments.CommentedMap])


def syaml_type(obj):
    """Get the corresponding syaml wrapper type for a primitive type.

    Return:
        (object): syaml-typed copy of object, or the obj if no wrapper
    """
    for syaml_t, t in syaml_types.items():
        if type(obj) is not bool and isinstance(obj, t):
            return syaml_t(obj) if type(obj) != syaml_t else obj
    return obj


def markable(obj):
    """Whether an object can be marked."""
    return type(obj) in markable_types


def mark(obj, node):
    """Add start and end markers to an object."""
    if hasattr(node, 'start_mark'):
        obj._start_mark = node.start_mark
    elif hasattr(node, '_start_mark'):
        obj._start_mark = node._start_mark
    if hasattr(node, 'end_mark'):
        obj._end_mark = node.end_mark
    elif hasattr(node, '_end_mark'):
        obj._end_mark = node._end_mark


def marked(obj):
    """Whether an object has been marked by spack_yaml."""
    return (hasattr(obj, '_start_mark') and obj._start_mark or
            hasattr(obj, '_end_mark') and obj._end_mark)


class OrderedLineLoader(RoundTripLoader):
    """YAML loader specifically intended for reading Spack configuration
       files. It preserves order and line numbers. It also has special-purpose
       logic for handling dictionary keys that indicate a Spack config
       override: namely any key that contains an "extra" ':' character.

       Mappings read in by this loader behave like an ordered dict.
       Sequences, mappings, and strings also have new attributes,
       ``_start_mark`` and ``_end_mark``, that preserve YAML line
       information in the output data.

    """
    #
    # Override construct_yaml_* so that we can apply _start_mark/_end_mark to
    # them. The superclass returns CommentedMap/CommentedSeq objects that we
    # can add attributes to (and we depend on their behavior to preserve
    # comments).
    #
    # The inherited sequence/dictionary constructors return empty instances
    # and fill in with mappings later.  We preserve this behavior.
    #

    def construct_yaml_str(self, node):
        value = super(OrderedLineLoader, self).construct_yaml_str(node)
        # There is no specific marker to indicate that we are parsing a key,
        # so this assumes we are talking about a Spack config override key if
        # it ends with a ':' and does not contain a '@' (which can appear
        # in config values that refer to Spack specs)
        if value and value.endswith(':') and '@' not in value:
            value = syaml_str(value[:-1])
            value.override = True
        else:
            value = syaml_str(value)
        mark(value, node)
        return value

    def construct_yaml_seq(self, node):
        gen = super(OrderedLineLoader, self).construct_yaml_seq(node)
        data = next(gen)
        if markable(data):
            mark(data, node)
        yield data
        for x in gen:
            pass

    def construct_yaml_map(self, node):
        gen = super(OrderedLineLoader, self).construct_yaml_map(node)
        data = next(gen)
        if markable(data):
            mark(data, node)
        yield data
        for x in gen:
            pass


# register above new constructors
OrderedLineLoader.add_constructor(
    'tag:yaml.org,2002:map', OrderedLineLoader.construct_yaml_map)
OrderedLineLoader.add_constructor(
    'tag:yaml.org,2002:seq', OrderedLineLoader.construct_yaml_seq)
OrderedLineLoader.add_constructor(
    'tag:yaml.org,2002:str', OrderedLineLoader.construct_yaml_str)


class OrderedLineDumper(RoundTripDumper):
    """Dumper that preserves ordering and formats ``syaml_*`` objects.

      This dumper preserves insertion ordering ``syaml_dict`` objects
      when they're written out.  It also has some custom formatters
      for ``syaml_*`` objects so that they are formatted like their
      regular Python equivalents, instead of ugly YAML pyobjects.

    """

    def ignore_aliases(self, _data):
        """Make the dumper NEVER print YAML aliases."""
        return True

    def represent_data(self, data):
        result = super(OrderedLineDumper, self).represent_data(data)
        if data is None:
            result.value = syaml_str("null")
        return result

    def represent_str(self, data):
        if hasattr(data, 'override') and data.override:
            data = data + ':'
        return super(OrderedLineDumper, self).represent_str(data)


class SafeDumper(RoundTripDumper):

    def ignore_aliases(self, _data):
        """Make the dumper NEVER print YAML aliases."""
        return True


# Make our special objects look like normal YAML ones.
RoundTripDumper.add_representer(syaml_dict, RoundTripDumper.represent_dict)
RoundTripDumper.add_representer(syaml_list, RoundTripDumper.represent_list)
RoundTripDumper.add_representer(syaml_int, RoundTripDumper.represent_int)
RoundTripDumper.add_representer(syaml_str, RoundTripDumper.represent_str)
OrderedLineDumper.add_representer(syaml_str, OrderedLineDumper.represent_str)


#: Max integer helps avoid passing too large a value to cyaml.
maxint = 2 ** (ctypes.sizeof(ctypes.c_int) * 8 - 1) - 1


def dump(obj, default_flow_style=False, stream=None):
    return yaml.dump(obj, default_flow_style=default_flow_style, width=maxint,
                     Dumper=SafeDumper, stream=stream)


def file_line(mark):
    """Format a mark as <file>:<line> information."""
    result = mark.name
    if mark.line:
        result += ':' + str(mark.line)
    return result


#: Global for interactions between LineAnnotationDumper and dump_annotated().
#: This is nasty but YAML doesn't give us many ways to pass arguments --
#: yaml.dump() takes a class (not an instance) and instantiates the dumper
#: itself, so we can't just pass an instance
_annotations = []  # type: List[str]


class LineAnnotationDumper(OrderedLineDumper):
    """Dumper that generates per-line annotations.

    Annotations are stored in the ``_annotations`` global.  After one
    dump pass, the strings in ``_annotations`` will correspond one-to-one
    with the lines output by the dumper.

    LineAnnotationDumper records blame information after each line is
    generated. As each line is parsed, it saves file/line info for each
    object printed. At the end of each line, it creates an annotation
    based on the saved mark and stores it in ``_annotations``.

    For an example of how to use this, see ``dump_annotated()``, which
    writes to a ``StringIO`` then joins the lines from that with
    annotations.
    """
    saved = None

    def __init__(self, *args, **kwargs):
        super(LineAnnotationDumper, self).__init__(*args, **kwargs)
        del _annotations[:]
        self.colors = 'KgrbmcyGRBMCY'
        self.filename_colors = {}

    def process_scalar(self):
        super(LineAnnotationDumper, self).process_scalar()
        if marked(self.event.value):
            self.saved = self.event.value

    def represent_data(self, data):
        """Force syaml_str to be passed through with marks."""
        result = super(LineAnnotationDumper, self).represent_data(data)
        if data is None:
            result.value = syaml_str("null")
        elif isinstance(result.value, string_types):
            result.value = syaml_str(data)
        if markable(result.value):
            mark(result.value, data)
        return result

    def write_line_break(self):
        super(LineAnnotationDumper, self).write_line_break()
        if self.saved is None:
            _annotations.append(colorize('@K{---}'))
            return

        # append annotations at the end of each line
        if self.saved:
            mark = self.saved._start_mark

            color = self.filename_colors.get(mark.name)
            if not color:
                ncolors = len(self.colors)
                color = self.colors[len(self.filename_colors) % ncolors]
                self.filename_colors[mark.name] = color

            fmt = '@%s{%%s}' % color
            ann = fmt % mark.name
            if mark.line is not None:
                ann += ':@c{%s}' % (mark.line + 1)
            _annotations.append(colorize(ann))
        else:
            _annotations.append('')


def load_config(*args, **kwargs):
    """Load but modify the loader instance so that it will add __line__
       attributes to the returned object."""
    kwargs['Loader'] = OrderedLineLoader
    return yaml.load(*args, **kwargs)


def load(*args, **kwargs):
    return yaml.load(*args, **kwargs)


def dump_config(*args, **kwargs):
    blame = kwargs.pop('blame', False)

    if blame:
        return dump_annotated(*args, **kwargs)
    else:
        kwargs['Dumper'] = OrderedLineDumper
        return yaml.dump(*args, **kwargs)


def dump_annotated(data, stream=None, *args, **kwargs):
    kwargs['Dumper'] = LineAnnotationDumper

    sio = StringIO()
    yaml.dump(data, sio, *args, **kwargs)

    # write_line_break() is not called by YAML for empty lines, so we
    # skip empty lines here with \n+.
    lines = re.split(r"\n+", sio.getvalue().rstrip())

    getvalue = None
    if stream is None:
        stream = StringIO()
        getvalue = stream.getvalue

    # write out annotations and lines, accounting for color
    width = max(clen(a) for a in _annotations)
    formats = ['%%-%ds  %%s\n' % (width + cextra(a)) for a in _annotations]

    for f, a, l in zip(formats, _annotations, lines):
        stream.write(f % (a, l))

    if getvalue:
        return getvalue()


def sorted_dict(dict_like):
    """Return an ordered dict with all the fields sorted recursively.

    Args:
        dict_like (dict): dictionary to be sorted

    Returns:
        dictionary sorted recursively
    """
    result = syaml_dict(sorted(dict_like.items()))
    for key, value in result.items():
        if isinstance(value, Mapping):
            result[key] = sorted_dict(value)
    return result


class SpackYAMLError(spack.error.SpackError):
    """Raised when there are issues with YAML parsing."""
    def __init__(self, msg, yaml_error):
        super(SpackYAMLError, self).__init__(msg, str(yaml_error))
