# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test verifies that the Spack directory layout works properly.
"""
import os
import os.path
from pathlib import Path

import pytest

from llnl.path import path_to_os_path

import spack.hash_types
import spack.paths
import spack.repo
import spack.spec
import spack.util.file_cache
from spack.directory_layout import DirectoryLayout, InvalidDirectoryLayoutParametersError
from spack.spec import Spec

# number of packages to test (to reduce test time)
max_packages = 10


def test_yaml_directory_layout_parameters(tmpdir, default_mock_concretization):
    """This tests the various parameters that can be used to configure
    the install location"""
    spec = default_mock_concretization("python")

    # Ensure default layout matches expected spec format
    layout_default = DirectoryLayout(str(tmpdir))
    path_default = layout_default.relative_path_for_spec(spec)
    assert path_default == str(
        Path(
            spec.format(
                "{architecture}/" "{compiler.name}-{compiler.version}/" "{name}-{version}-{hash}"
            )
        )
    )

    # Test hash_length parameter works correctly
    layout_10 = DirectoryLayout(str(tmpdir), hash_length=10)
    path_10 = layout_10.relative_path_for_spec(spec)
    layout_7 = DirectoryLayout(str(tmpdir), hash_length=7)
    path_7 = layout_7.relative_path_for_spec(spec)

    assert len(path_default) - len(path_10) == 22
    assert len(path_default) - len(path_7) == 25

    # Test path_scheme
    arch, compiler, package7 = path_7.split(os.sep)
    projections_package7 = {"all": "{name}-{version}-{hash:7}"}
    layout_package7 = DirectoryLayout(str(tmpdir), projections=projections_package7)
    path_package7 = layout_package7.relative_path_for_spec(spec)

    assert package7 == path_package7

    # Test separation of architecture or namespace
    spec2 = Spec("libelf").concretized()

    arch_scheme = (
        "{architecture.platform}/{architecture.target}/{architecture.os}/{name}/{version}/{hash:7}"
    )
    ns_scheme = "{architecture}/{namespace}/{name}-{version}-{hash:7}"
    arch_ns_scheme_projections = {"all": arch_scheme, "python": ns_scheme}
    layout_arch_ns = DirectoryLayout(str(tmpdir), projections=arch_ns_scheme_projections)

    arch_path_spec2 = layout_arch_ns.relative_path_for_spec(spec2)
    assert arch_path_spec2 == str(Path(spec2.format(arch_scheme)))

    ns_path_spec = layout_arch_ns.relative_path_for_spec(spec)
    assert ns_path_spec == str(Path(spec.format(ns_scheme)))

    # Ensure conflicting parameters caught
    with pytest.raises(InvalidDirectoryLayoutParametersError):
        DirectoryLayout(str(tmpdir), hash_length=20, projections=projections_package7)


def test_read_and_write_spec(temporary_store, config, mock_packages):
    """This goes through each package in spack and creates a directory for
    it.  It then ensures that the spec for the directory's
    installed package can be read back in consistently, and
    finally that the directory can be removed by the directory
    layout.
    """
    layout = temporary_store.layout
    pkg_names = list(spack.repo.PATH.all_package_names())[:max_packages]

    for name in pkg_names:
        if name.startswith("external"):
            # External package tests cannot be installed
            continue

        # If a spec fails to concretize, just skip it.  If it is a
        # real error, it will be caught by concretization tests.
        try:
            spec = spack.spec.Spec(name).concretized()
        except Exception:
            continue

        layout.create_install_directory(spec)

        install_dir = path_to_os_path(layout.path_for_spec(spec))[0]
        spec_path = layout.spec_file_path(spec)

        # Ensure directory has been created in right place.
        assert os.path.isdir(install_dir)
        assert install_dir.startswith(temporary_store.root)

        # Ensure spec file exists when directory is created
        assert os.path.isfile(spec_path)
        assert spec_path.startswith(install_dir)

        # Make sure spec file can be read back in to get the original spec
        spec_from_file = layout.read_spec(spec_path)

        stored_deptypes = spack.hash_types.dag_hash
        expected = spec.copy(deps=stored_deptypes)
        expected._mark_concrete()

        assert expected.concrete
        assert expected == spec_from_file
        assert expected.eq_dag(spec_from_file)
        assert spec_from_file.concrete

        # Ensure that specs that come out "normal" are really normal.
        with open(spec_path) as spec_file:
            read_separately = Spec.from_yaml(spec_file.read())

        # TODO: revise this when build deps are in dag_hash
        norm = read_separately.copy(deps=stored_deptypes)
        assert norm == spec_from_file
        assert norm.eq_dag(spec_from_file)

        # TODO: revise this when build deps are in dag_hash
        conc = read_separately.concretized().copy(deps=stored_deptypes)
        assert conc == spec_from_file
        assert conc.eq_dag(spec_from_file)

        assert expected.dag_hash() == spec_from_file.dag_hash()

        # Ensure directories are properly removed
        layout.remove_install_directory(spec)
        assert not os.path.isdir(install_dir)
        assert not os.path.exists(install_dir)


def test_handle_unknown_package(temporary_store, config, mock_packages, tmp_path):
    """This test ensures that spack can at least do *some*
    operations with packages that are installed but that it
    does not know about.  This is actually not such an uncommon
    scenario with spack; it can happen when you switch from a
    git branch where you're working on a new package.

    This test ensures that the directory layout stores enough
    information about installed packages' specs to uninstall
    or query them again if the package goes away.
    """
    layout = temporary_store.layout

    repo_cache = spack.util.file_cache.FileCache(str(tmp_path / "cache"))
    mock_db = spack.repo.RepoPath(spack.paths.mock_packages_path, cache=repo_cache)

    not_in_mock = set.difference(
        set(spack.repo.all_package_names()), set(mock_db.all_package_names())
    )
    packages = list(not_in_mock)[:max_packages]

    # Create all the packages that are not in mock.
    installed_specs = {}
    for pkg_name in packages:
        spec = spack.spec.Spec(pkg_name)

        # If a spec fails to concretize, just skip it.  If it is a
        # real error, it will be caught by concretization tests.
        try:
            spec.concretize()
        except Exception:
            continue

        layout.create_install_directory(spec)
        installed_specs[spec] = layout.path_for_spec(spec)

    with spack.repo.use_repositories(spack.paths.mock_packages_path):
        # Now check that even without the package files, we know
        # enough to read a spec from the spec file.
        for spec, path in installed_specs.items():
            spec_from_file = layout.read_spec(os.path.join(path, ".spack", "spec.json"))

            # To satisfy these conditions, directory layouts need to
            # read in concrete specs from their install dirs somehow.
            assert path == layout.path_for_spec(spec_from_file)
            assert spec == spec_from_file
            assert spec.eq_dag(spec_from_file)
            assert spec.dag_hash() == spec_from_file.dag_hash()


def test_find(temporary_store, config, mock_packages):
    """Test that finding specs within an install layout works."""
    layout = temporary_store.layout
    package_names = list(spack.repo.PATH.all_package_names())[:max_packages]

    # Create install prefixes for all packages in the list
    installed_specs = {}
    for name in package_names:
        if name.startswith("external"):
            # External package tests cannot be installed
            continue
        spec = spack.spec.Spec(name).concretized()
        installed_specs[spec.name] = spec
        layout.create_install_directory(spec)

    # Make sure all the installed specs appear in
    # DirectoryLayout.all_specs()
    found_specs = dict((s.name, s) for s in layout.all_specs())
    for name, spec in found_specs.items():
        assert name in found_specs
        assert found_specs[name].eq_dag(spec)


def test_yaml_directory_layout_build_path(tmpdir, default_mock_concretization):
    """This tests build path method."""
    spec = default_mock_concretization("python")
    layout = DirectoryLayout(str(tmpdir))
    rel_path = os.path.join(layout.metadata_dir, layout.packages_dir)
    assert layout.build_packages_path(spec) == os.path.join(spec.prefix, rel_path)
