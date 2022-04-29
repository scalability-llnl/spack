# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains additional behavior that can be attached to any given
package.
"""
import os
import sys
from typing import Callable, DefaultDict, List  # novm

if sys.version_info >= (3, 5):
    CallbackDict = DefaultDict[str, List[Callable]]
else:
    CallbackDict = None

import llnl.util.filesystem

import spack.builder


def filter_compiler_wrappers(*files, **kwargs):
    """Substitutes any path referring to a Spack compiler wrapper with the
    path of the underlying compiler that has been used.

    If this isn't done, the files will have CC, CXX, F77, and FC set to
    Spack's generic cc, c++, f77, and f90. We want them to be bound to
    whatever compiler they were built with.

    Args:
        *files: files to be filtered relative to the search root (which is,
            by default, the installation prefix)

        **kwargs: allowed keyword arguments

            after
                specifies after which phase the files should be
                filtered (defaults to 'install')

            relative_root
                path relative to prefix where to start searching for
                the files to be filtered. If not set the install prefix
                wil be used as the search root. **It is highly recommended
                to set this, as searching from the installation prefix may
                affect performance severely in some cases**.

            ignore_absent, backup
                these two keyword arguments, if present, will be forwarded
                to ``filter_file`` (see its documentation for more information
                on their behavior)

            recursive
                this keyword argument, if present, will be forwarded to
                ``find`` (see its documentation for more information on the
                behavior)
    """
    after = kwargs.get('after', 'install')
    relative_root = kwargs.get('relative_root', None)

    filter_kwargs = {
        'ignore_absent': kwargs.get('ignore_absent', True),
        'backup': kwargs.get('backup', False),
        'string': True
    }

    find_kwargs = {
        'recursive': kwargs.get('recursive', False)
    }

    def _filter_compiler_wrappers_impl(self):
        # Compute the absolute path of the search root
        root = os.path.join(
            self.prefix, relative_root
        ) if relative_root else self.prefix

        # Compute the absolute path of the files to be filtered and
        # remove links from the list.
        abs_files = llnl.util.filesystem.find(root, files, **find_kwargs)
        abs_files = [x for x in abs_files if not os.path.islink(x)]

        x = llnl.util.filesystem.FileFilter(*abs_files)

        compiler_vars = [
            ('CC', self.compiler.cc),
            ('CXX', self.compiler.cxx),
            ('F77', self.compiler.f77),
            ('FC', self.compiler.fc)
        ]

        # Some paths to the compiler wrappers might be substrings of the others.
        # For example:
        #   CC=/path/to/spack/lib/spack/env/cc (realpath to the wrapper)
        #   FC=/path/to/spack/lib/spack/env/cce/ftn
        # Therefore, we perform the filtering in the reversed sorted order of
        # the substituted strings. If, however, the strings are identical (e.g.
        # both CC and FC are set using realpath), the filtering is done
        # according to the order in compiler_vars. To achieve that, we populate
        # the following array with tuples of three elements: path to the
        # wrapper, negated index of the variable in compiler_vars, path to the
        # real compiler. This way, the reversed sorted order of the resulting
        # array is the order of replacements that we need.
        replacements = []

        for idx, (env_var, compiler_path) in enumerate(compiler_vars):
            if env_var in os.environ:
                # filter spack wrapper and links to spack wrapper in case
                # build system runs realpath
                wrapper = os.environ[env_var]
                for wrapper_path in (wrapper, os.path.realpath(wrapper)):
                    replacements.append((wrapper_path, -idx, compiler_path))

        for wrapper_path, _, compiler_path in sorted(replacements,
                                                     reverse=True):
            x.filter(wrapper_path, compiler_path, **filter_kwargs)

        # Remove this linking flag if present (it turns RPATH into RUNPATH)
        x.filter('{0}--enable-new-dtags'.format(self.compiler.linker_arg), '',
                 **filter_kwargs)

        # NAG compiler is usually mixed with GCC, which has a different
        # prefix for linker arguments.
        if self.compiler.name == 'nag':
            x.filter('-Wl,--enable-new-dtags', '', **filter_kwargs)

    spack.builder.run_after(after)(_filter_compiler_wrappers_impl)
