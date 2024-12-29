# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Definitions that control how Spack creates Spec hashes."""

import spack.deptypes as dt
import spack.repo

hashes = []


class SpecHashDescriptor:
    """This class defines how hashes are generated on Spec objects.

    Spec hashes in Spack are generated from a serialized (e.g., with
    YAML) representation of the Spec graph.  The representation may only
    include certain dependency types, and it may optionally include a
    canonicalized hash of the package.py for each node in the graph.

    We currently use different hashes for different use cases."""

    def __init__(self, depflag: dt.DepFlag, package_hash, name, override=None):
        self.depflag = depflag
        self.package_hash = package_hash
        self.name = name
        hashes.append(self)
        # Allow spec hashes to have an alternate computation method
        self.override = override

    @property
    def attr(self):
        """Private attribute stored on spec"""
        return "_" + self.name

    def __call__(self, spec):
        """Run this hash on the provided spec."""
        return spec.spec_hash(self)

    def __repr__(self):
        return (
            f"SpecHashDescriptor(depflag={self.depflag!r}, "
            f"package_hash={self.package_hash!r}, name={self.name!r}, override={self.override!r})"
        )


#: Spack's deployment hash. Includes all inputs that can affect how a package is built.
dag_hash = SpecHashDescriptor(depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=True, name="hash")


#: Hash descriptor used only to transfer a DAG, as is, across processes
process_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN | dt.TEST, package_hash=True, name="process_hash"
)


def _content_hash_override(spec):
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pkg = pkg_cls(spec)
    return pkg.content_hash()


#: Package hash used as part of dag hash
package_hash = SpecHashDescriptor(
    depflag=0, package_hash=True, name="package_hash", override=_content_hash_override
)


# Deprecated hash types, no longer used, but needed to understand old serialized
# spec formats

full_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=True, name="full_hash"
)


build_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=False, name="build_hash"
)
