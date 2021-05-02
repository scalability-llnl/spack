# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Implementation of Spack imports that uses importlib underneath.

``importlib`` is only fully implemented in Python 3.
"""
from importlib.machinery import SourceFileLoader  # novm
from importlib.util import spec_from_loader, module_from_spec  # novm


class PrependFileLoader(SourceFileLoader):
    def __init__(self, full_name, path, prepend=None):
        super(PrependFileLoader, self).__init__(full_name, path)
        self.prepend = prepend

    def path_stats(self, path):
        stats = super(PrependFileLoader, self).path_stats(path)
        if self.prepend:
            stats["size"] += len(self.prepend) + 1
        return stats

    def get_data(self, path):
        data = super(PrependFileLoader, self).get_data(path)
        if path != self.path or self.prepend is None:
            return data
        else:
            return self.prepend.encode() + b"\n" + data


def load_source(full_name, path, prepend=None):
    """Import a Python module from source.

    Args:
        full_name (str): full name of the module to be loaded
        path (str): path to the file that should be loaded
        prepend (str, optional): some optional code to prepend to the
            loaded module; e.g., can be used to inject import statements

    Returns:
        (ModuleType): the loaded module
    """
    # use our custom loader
    loader = PrependFileLoader(full_name, path, prepend)
    # Note this is a ModuleSpec object defined in importlib and not a
    # Spack Spec object
    module_spec = spec_from_loader(full_name, loader)
    mod = module_from_spec(module_spec)
    module_spec.loader.exec_module(mod)
    return mod
