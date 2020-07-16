# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import llnl.util.filesystem
import spack.main
import spack.version

compiler = spack.main.SpackCommand('compiler')


@pytest.fixture
def no_compilers_yaml(mutable_config, monkeypatch):
    """Creates a temporary configuration without compilers.yaml"""

    for scope, local_config in mutable_config.scopes.items():
        compilers_yaml = os.path.join(
            local_config.path, scope, 'compilers.yaml'
        )
        if os.path.exists(compilers_yaml):
            os.remove(compilers_yaml)


@pytest.fixture
def mock_compiler_version():
    return '4.5-spacktest'


@pytest.fixture
def mock_pgi_version():
    return '0.0'


@pytest.fixture
def mock_pgi_version_string():
    return 'pgcc 0.0-0 LLVM 64-bit target on pgispacktest'


@pytest.fixture()
def mock_compiler_dir(tmpdir, mock_compiler_version):
    """Return a directory containing a fake, but detectable compiler."""

    tmpdir.ensure('bin', dir=True)
    bin_dir = tmpdir.join('bin')

    gcc_path = bin_dir.join('gcc')
    gxx_path = bin_dir.join('g++')
    gfortran_path = bin_dir.join('gfortran')

    gcc_path.write("""\
#!/bin/sh

for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '%s'
    fi
done
""" % mock_compiler_version)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(gcc_path))
    gcc_path.copy(gxx_path, mode=True)
    gcc_path.copy(gfortran_path, mode=True)

    return str(tmpdir)


@pytest.fixture()
def mock_two_compiler_dirs(tmpdir, mock_compiler_version):
    """Return two directories containing a fake, but detectable compiler,
    with the same compiler spec."""

    tmpdir.ensure('compiler1/bin', dir=True)
    tmpdir1 = tmpdir.join('compiler1')
    bin_dir1 = tmpdir1.join('bin')

    gcc_path1 = bin_dir1.join('gcc')
    gxx_path1 = bin_dir1.join('g++')
    gfortran_path1 = bin_dir1.join('gfortran')

    tmpdir.ensure('compiler2/bin', dir=True)
    tmpdir2 = tmpdir.join('compiler2')
    bin_dir2 = tmpdir2.join('bin')

    gcc_path2 = bin_dir2.join('gcc')
    gxx_path2 = bin_dir2.join('g++')
    gfortran_path2 = bin_dir2.join('gfortran')

    gcc_path1.write("""\
#!/bin/sh
for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '%s'
    fi
done
""" % mock_compiler_version)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(gcc_path1))
    gcc_path1.copy(gxx_path1, mode=True)
    gcc_path1.copy(gfortran_path1, mode=True)

    gcc_path1.copy(gcc_path2, mode=True)
    gcc_path1.copy(gxx_path2, mode=True)
    gcc_path1.copy(gfortran_path2, mode=True)

    return [str(tmpdir1), str(tmpdir2)]


@pytest.fixture()
def mock_pgi_dir(tmpdir, mock_pgi_version_string):
    """Return a directory containing a fake, but detectable pgi compiler,
    with both old (pgf77, pgf90) and new (pgfortran) names."""

    tmpdir.ensure('bin', dir=True)
    bin_dir = tmpdir.join('bin')

    pgcc_path = bin_dir.join('pgcc')
    pgxx_path = bin_dir.join('pg++')
    pgfortran_path = bin_dir.join('pgfortran')
    pgf77_path = bin_dir.join('pgf77')
    pgf90_path = bin_dir.join('pgf90')

    pgcc_path.write("""\
#!/bin/sh
for arg in "$@"; do
    if [ "$arg" = -V ]; then
        echo '%s'
    fi
done
""" % mock_pgi_version_string)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(pgcc_path))
    pgcc_path.copy(pgxx_path, mode=True)
    pgcc_path.copy(pgfortran_path, mode=True)
    pgcc_path.copy(pgf77_path, mode=True)
    pgcc_path.copy(pgf90_path, mode=True)

    return str(tmpdir)


@pytest.mark.regression('11678,13138')
def test_compiler_find_without_paths(no_compilers_yaml, working_env, tmpdir):
    with tmpdir.as_cwd():
        with open('gcc', 'w') as f:
            f.write("""\
#!/bin/bash
echo "0.0.0"
""")
        os.chmod('gcc', 0o700)

    os.environ['PATH'] = str(tmpdir)
    output = compiler('find', '--scope=site')

    assert 'gcc' in output


def test_compiler_remove(mutable_config, mock_packages):
    args = spack.util.pattern.Bunch(
        all=True, compiler_spec='gcc@4.5.0', add_paths=[], scope=None
    )
    spack.cmd.compiler.compiler_remove(args)
    compilers = spack.compilers.all_compiler_specs()
    assert spack.spec.CompilerSpec("gcc@4.5.0") not in compilers


def test_compiler_add(
        mutable_config, mock_packages, mock_compiler_dir, mock_compiler_version
):
    # Compilers available by default.
    old_compilers = set(spack.compilers.all_compiler_specs())

    args = spack.util.pattern.Bunch(
        all=None,
        compiler_spec=None,
        add_paths=[mock_compiler_dir],
        scope=None
    )
    spack.cmd.compiler.compiler_find(args)

    # Ensure new compiler is in there
    new_compilers = set(spack.compilers.all_compiler_specs())
    new_compiler = new_compilers - old_compilers
    assert any(c.version == spack.version.Version(mock_compiler_version)
               for c in new_compiler)


def test_compiler_add_multiple_in_path(
    mock_two_compiler_dirs, mutable_empty_config, mock_compiler_version
):
    # Find compilers
    args = spack.util.pattern.Bunch(
        all=None,
        compiler_spec=None,
        add_paths=mock_two_compiler_dirs,
        scope=None
    )
    spack.cmd.compiler.compiler_find(args)

    # Ensure new compiler is from the first path passed and has correct version
    new_compilers = set(spack.compilers.all_compiler_specs())
    new_comp = spack.compilers.compilers_for_spec('gcc@%s'
                                                  % mock_compiler_version)
    assert mock_two_compiler_dirs[0] in new_comp[0].cc
    assert any(c.version == spack.version.Version(mock_compiler_version)
               for c in new_compilers)


def test_compiler_add_multiple_names(
    mock_pgi_dir, mutable_empty_config, mock_pgi_version,
    mock_pgi_version_string
):
    # Find compilers
    args = spack.util.pattern.Bunch(
        all=None,
        compiler_spec=None,
        add_paths=[mock_pgi_dir],
        scope=None
    )
    spack.cmd.compiler.compiler_find(args)

    # Ensure new compiler is in there and has newest pgi names
    new_compilers = set(spack.compilers.all_compiler_specs())
    new_comp = spack.compilers.compilers_for_spec('pgi@%s'
                                                  % mock_pgi_version)
    assert 'pgfortran' in new_comp[0].f77
    assert 'pgfortran' in new_comp[0].fc
    assert any(c.version == spack.version.Version(mock_pgi_version)
               for c in new_compilers)
