# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import textwrap

import jinja2
import llnl.util.lang
import six

import spack.config
from spack.config import canonicalize_path


TemplateNotFound = jinja2.TemplateNotFound


class ContextMeta(type):
    """Meta class for Context. It helps reducing the boilerplate in
    client code.
    """
    #: Keeps track of the context properties that have been added
    #: by the class that is being defined
    _new_context_properties = []

    def __new__(cls, name, bases, attr_dict):
        # Merge all the context properties that are coming from base classes
        # into a list without duplicates.
        context_properties = list(cls._new_context_properties)
        for x in bases:
            try:
                context_properties.extend(x.context_properties)
            except AttributeError:
                pass
        context_properties = list(llnl.util.lang.dedupe(context_properties))

        # Flush the list
        cls._new_context_properties = []

        # Attach the list to the class being created
        attr_dict['context_properties'] = context_properties

        return super(ContextMeta, cls).__new__(cls, name, bases, attr_dict)

    @classmethod
    def context_property(cls, func):
        """Decorator that adds a function name to the list of new context
        properties, and then returns a property.
        """
        name = func.__name__
        cls._new_context_properties.append(name)
        return property(func)


#: A saner way to use the decorator
context_property = ContextMeta.context_property


class Context(six.with_metaclass(ContextMeta, object)):
    """Base class for context classes that are used with the template
    engine.
    """

    def to_dict(self):
        """Returns a dictionary containing all the context properties."""
        d = [(name, getattr(self, name)) for name in self.context_properties]
        return dict(d)


def make_environment(dirs=None):
    """Returns an configured environment for template rendering."""
    if dirs is None:
        # Default directories where to search for templates
        builtins = spack.config.get('config:template_dirs')
        extensions = spack.extensions.get_template_dirs()
        dirs = [canonicalize_path(d)
                for d in itertools.chain(builtins, extensions)]

    # Loader for the templates
    loader = jinja2.FileSystemLoader(dirs)
    # Environment of the template engine
    env = jinja2.Environment(loader=loader, trim_blocks=True)
    # Custom filters
    _set_filters(env)
    return env


# Extra filters for template engine environment

def prepend_to_line(text, token):
    """Prepends a token to each line in text"""
    return [token + line for line in text]


def quote(text):
    """Quotes each line in text"""
    return ['"{0}"'.format(line) for line in text]


def _set_filters(env):
    """Sets custom filters to the template engine environment"""
    env.filters['textwrap'] = textwrap.wrap
    env.filters['prepend_to_line'] = prepend_to_line
    env.filters['join'] = '\n'.join
    env.filters['quote'] = quote
