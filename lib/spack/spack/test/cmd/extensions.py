# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import spack.concretize
from spack.installer import PackageInstaller
from spack.main import SpackCommand, SpackCommandError

extensions = SpackCommand("extensions")


@pytest.fixture
def python_database(mock_packages, mutable_database):
    specs = [
        spack.concretize.concretize_one(s) for s in ["python", "py-extension1", "py-extension2"]
    ]
    PackageInstaller([s.package for s in specs], explicit=True, fake=True).install()
    yield


@pytest.mark.not_on_windows("All Fetchers Failed")
@pytest.mark.db
def test_extensions(mock_packages, python_database, capsys):
    ext2 = spack.concretize.concretize_one("py-extension2")

    def check_output(ni):
        with capsys.disabled():
            output = extensions("python")
            packages = extensions("-s", "packages", "python")
            installed = extensions("-s", "installed", "python")
        assert "==> python@2.7.11" in output
        assert "==> 3 extensions" in output
        assert "py-extension1" in output
        assert "py-extension2" in output
        assert "python-venv" in output

        assert "==> 3 extensions" in packages
        assert "py-extension1" in packages
        assert "py-extension2" in packages
        assert "python-venv" in packages
        assert "installed" not in packages

        assert f"{ni if ni else 'None'} installed" in output
        assert f"{ni if ni else 'None'} installed" in installed

    check_output(3)
    ext2.package.do_uninstall(force=True)
    check_output(2)


def test_extensions_no_arguments(mock_packages):
    out = extensions()
    assert "python" in out


def test_extensions_raises_if_not_extendable(mock_packages):
    with pytest.raises(SpackCommandError):
        extensions("flake8")


def test_extensions_raises_if_multiple_specs(mock_packages):
    with pytest.raises(SpackCommandError):
        extensions("python", "flake8")
