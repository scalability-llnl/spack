# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Definitions that control how Spack creates Spec hashes."""

import spack.dependency as dp


class SpecHashDescriptor(object):
    """This class defines how hashes are generated on Spec objects.

    Spec hashes in Spack are generated from a serialized (e.g., with
    YAML) representation of the Spec graph.  The representation may only
    include certain dependency types, and it may optionally include a
    canonicalized hash of the package.py for each node in the graph.

    We currently use different hashes for different use cases.
    """

    hash_types = ('_dag_hash', '_build_hash', '_full_hash')

    def __init__(self, deptype=('link', 'run'), package_hash=False, attr=None):
        self.deptype = dp.canonical_deptype(deptype)
        self.package_hash = package_hash
        self.attr = attr


#: Default Hash descriptor, used by Spec.dag_hash() and stored in the DB.
dag_hash = SpecHashDescriptor(deptype=('link', 'run'), package_hash=False,
                              attr='_hash')


#: Hash descriptor that includes build dependencies.
build_hash = SpecHashDescriptor(
    deptype=('build', 'link', 'run'), package_hash=False, attr='_build_hash')


#: Full hash used in build pipelines to determine when to rebuild packages.
full_hash = SpecHashDescriptor(
    deptype=('build', 'link', 'run'), package_hash=True, attr='_full_hash')
