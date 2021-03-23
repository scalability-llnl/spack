# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand, SpackCommandError
from spack.spec import Spec


extensions = SpackCommand('extensions')


@pytest.fixture
def python_database(mock_packages, mutable_database):
    specs = [Spec(s).concretized() for s in [
        'python',
        'py-extension1',
        'py-extension2',
    ]]

    for spec in specs:
        spec.package.do_install(fake=True, explicit=True)

    yield


@pytest.mark.db
def test_extensions(mock_packages, python_database, config, capsys):
    ext2   = Spec("py-extension2").concretized()

    def check_output(ni, na):
        with capsys.disabled():
            output = extensions("python")
            packages = extensions("-s", "packages", "python")
            installed = extensions("-s", "installed", "python")
            activated = extensions("-s", "activated", "python")
        assert "==> python@2.7.11" in output
        assert "==> 3 extensions" in output
        assert "flake8" in output
        assert "py-extension1" in output
        assert "py-extension2" in output

        assert "==> 3 extensions" in packages
        assert "flake8" in packages
        assert "py-extension1" in packages
        assert "py-extension2" in packages
        assert "installed" not in packages
        assert "activated" not in packages

        assert ("%s installed" % (ni if ni else "None")) in output
        assert ("%s activated" % (na if na else "None")) in output
        assert ("%s installed" % (ni if ni else "None")) in installed
        assert ("%s activated" % (na if na else "None")) in activated

    check_output(2, 0)

    ext2.package.do_activate()
    check_output(2, 2)

    ext2.package.do_deactivate(force=True)
    check_output(2, 1)

    ext2.package.do_activate()
    check_output(2, 2)

    ext2.package.do_uninstall(force=True)
    check_output(1, 1)


def test_extensions_no_arguments(mock_packages):
    out = extensions()
    assert 'python' in out


def test_extensions_raises_if_not_extendable(mock_packages):
    with pytest.raises(SpackCommandError):
        extensions("flake8")


def test_extensions_raises_if_multiple_specs(mock_packages):
    with pytest.raises(SpackCommandError):
        extensions("python", "flake8")
