# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import tempfile

import spack.binary_distribution as bindist
import spack.deptypes as dt
import spack.error
import spack.hooks
import spack.platforms
import spack.relocate as relocate
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
    buildinfo = bindist.read_buildinfo_file(spec.prefix)

    # compute prefix-to-prefix for every node from the build spec to the spliced
    # spec
    prefix_to_prefix = {spec.build_spec.prefix: spec.prefix}
    build_spec_ids = set(id(s) for s in spec.build_spec.traverse(deptype=dt.ALL & ~dt.BUILD))
    for s in bindist.specs_to_relocate(spec):
        analog = s
        if id(s) not in build_spec_ids:
            analogs = [
                d
                for d in spec.build_spec.traverse(deptype=dt.ALL & ~dt.BUILD)
                if s._splice_match(d, self_root=spec, other_root=spec.build_spec)
            ]
            if analogs:
                # Prefer same-name analogs and prefer higher versions
                # This matches the preferences in Spec.splice, so we will find same node
                analog = max(analogs, key=lambda a: (a.name == s.name, a.version))

        prefix_to_prefix[analog.prefix] = s.prefix

    platform = spack.platforms.by_name(spec.platform)

    text_to_relocate = [
        os.path.join(spec.prefix, rel_path) for rel_path in buildinfo["relocate_textfiles"]
    ]
    if text_to_relocate:
        relocate.relocate_text(files=text_to_relocate, prefixes=prefix_to_prefix)
    links = [os.path.join(spec.prefix, f) for f in buildinfo["relocate_links"]]
    relocate.relocate_links(links, prefix_to_prefix)
    bins_to_relocate = [
        os.path.join(spec.prefix, rel_path) for rel_path in buildinfo["relocate_binaries"]
    ]
    if bins_to_relocate:
        if "macho" in platform.binary_formats:
            relocate.relocate_macho_binaries(bins_to_relocate, prefix_to_prefix)
        if "elf" in platform.binary_formats:
            relocate.relocate_elf_binaries(bins_to_relocate, prefix_to_prefix)
        relocate.relocate_text_bin(binaries=bins_to_relocate, prefixes=prefix_to_prefix)
    shutil.rmtree(tempdir)
    install_manifest = os.path.join(
        spec.prefix,
        spack.store.STORE.layout.metadata_dir,
        spack.store.STORE.layout.manifest_file_name,
    )
    try:
        os.unlink(install_manifest)
    except FileNotFoundError:
        pass
    # Write the spliced spec into spec.json. Without this, Database.add would fail because it
    # checks the spec.json in the prefix against the spec being added to look for mismatches
    spack.store.STORE.layout.write_spec(spec, spack.store.STORE.layout.spec_file_path(spec))
    # add to database, not sure about explicit
    spack.store.STORE.db.add(spec, explicit=explicit)

    # run post install hooks
    spack.hooks.post_install(spec, explicit)


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
