# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tempfile

import spack.binary_distribution as bindist
import spack.error
import spack.hooks
import spack.store


def rewire(spliced_spec):
    """Given a spliced spec, this function conducts all the rewiring on all
    nodes in the DAG of that spec."""
    assert spliced_spec.spliced
    for spec in spliced_spec.traverse(order="post", root=True):
        if not spec.build_spec.installed:
            # TODO: May want to change this at least for the root spec...
            # TODO: Also remember to import PackageInstaller
            # PackageInstaller([spec.build_spec.package]).install()
            raise PackageNotInstalledError(spliced_spec, spec.build_spec, spec)
        if spec.build_spec is not spec and not spec.installed:
            explicit = spec is spliced_spec
            rewire_node(spec, explicit)


def rewire_node(spec, explicit):
    """This function rewires a single node, worrying only about references to
    its subgraph. Binaries, text, and links are all changed in accordance with
    the splice. The resulting package is then 'installed.'"""
    tempdir = tempfile.mkdtemp()

    # Copy spec.build_spec.prefix to spec.prefix through a temporary tarball
    tarball = os.path.join(tempdir, f"{spec.dag_hash()}.tar.gz")
    bindist.create_tarball(spec.build_spec, tarball)

    spack.hooks.pre_install(spec)
    bindist.extract_buildcache_tarball(tarball, destination=spec.prefix)
    bindist.relocate_package(spec)

    # run post install hooks and add to db
    spack.hooks.post_install(spec, explicit)
    spack.store.STORE.db.add(spec, explicit=explicit)


class RewireError(spack.error.SpackError):
    """Raised when something goes wrong with rewiring."""

    def __init__(self, message, long_msg=None):
        super().__init__(message, long_msg)


class PackageNotInstalledError(RewireError):
    """Raised when the build_spec for a splice was not installed."""

    def __init__(self, spliced_spec, build_spec, dep):
        super().__init__(
            """Rewire of {0}
            failed due to missing install of build spec {1}
            for spec {2}""".format(
                spliced_spec, build_spec, dep
            )
        )
