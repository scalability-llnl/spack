# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import pathlib

import pytest

import spack.cmd.checksum
import spack.concretize
import spack.error
import spack.package_base
import spack.repo
import spack.stage
import spack.util.web
from spack.main import SpackCommand
from spack.package_base import ManualDownloadRequiredError
from spack.stage import interactive_version_filter
from spack.version import Version

spack_checksum = SpackCommand("checksum")


@pytest.fixture
def no_add(monkeypatch):
    def add_versions_to_pkg(pkg, version_lines, open_in_editor):
        raise AssertionError("Should not be called")

    monkeypatch.setattr(spack.cmd.checksum, "add_versions_to_pkg", add_versions_to_pkg)


@pytest.fixture
def can_fetch_versions(monkeypatch, no_add):
    """Fake successful version detection."""

    def fetch_remote_versions(pkg, concurrency):
        return {Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz"}

    def get_checksums_for_versions(url_by_version, package_name, **kwargs):
        return {
            v: "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
            for v in url_by_version
        }

    def url_exists(url, curl=None):
        return True

    monkeypatch.setattr(
        spack.package_base.PackageBase, "fetch_remote_versions", fetch_remote_versions
    )
    monkeypatch.setattr(spack.stage, "get_checksums_for_versions", get_checksums_for_versions)
    monkeypatch.setattr(spack.util.web, "url_exists", url_exists)


@pytest.fixture
def cannot_fetch_versions(monkeypatch, no_add):
    """Fake unsuccessful version detection."""

    def fetch_remote_versions(pkg, concurrency):
        return {}

    def get_checksums_for_versions(url_by_version, package_name, **kwargs):
        return {}

    def url_exists(url, curl=None):
        return False

    monkeypatch.setattr(
        spack.package_base.PackageBase, "fetch_remote_versions", fetch_remote_versions
    )
    monkeypatch.setattr(spack.stage, "get_checksums_for_versions", get_checksums_for_versions)
    monkeypatch.setattr(spack.util.web, "url_exists", url_exists)


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["--batch", "patch"], (True, False, False, False, False)),
        (["--latest", "patch"], (False, True, False, False, False)),
        (["--preferred", "patch"], (False, False, True, False, False)),
        (["--add-to-package", "patch"], (False, False, False, True, False)),
        (["--verify", "patch"], (False, False, False, False, True)),
    ],
)
def test_checksum_args(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.checksum.setup_parser(parser)
    args = parser.parse_args(arguments)
    check = args.batch, args.latest, args.preferred, args.add_to_package, args.verify
    assert check == expected


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["--batch", "preferred-test"], "version of preferred-test"),
        (["--latest", "preferred-test"], "Found 1 version"),
        (["--preferred", "preferred-test"], "Found 1 version"),
        (["--verify", "preferred-test"], "Verified 1 of 1"),
        (["--verify", "zlib", "1.2.13"], "1.2.13  [-] No previous checksum"),
    ],
)
def test_checksum(arguments, expected, mock_packages, can_fetch_versions):
    output = spack_checksum(*arguments)
    assert expected in output

    # --verify doesn't print versions strings like other flags
    if "--verify" not in arguments:
        assert "version(" in output


def input_from_commands(*commands):
    """Create a function that returns the next command from a list of inputs for interactive spack
    checksum. If None is encountered, this is equivalent to EOF / ^D."""
    commands = iter(commands)

    def _input(prompt):
        cmd = next(commands)
        if cmd is None:
            raise EOFError
        assert isinstance(cmd, str)
        return cmd

    return _input


def test_checksum_interactive_filter():
    # Filter effectively by 1:1.0, then checksum.
    input = input_from_commands("f", "@1:", "f", "@:1.0", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
    }


def test_checksum_interactive_return_from_filter_prompt():
    # Enter and then exit filter subcommand.
    input = input_from_commands("f", None, "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
        Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
        Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
    }


def test_checksum_interactive_quit_returns_none():
    # Quit after filtering something out (y to confirm quit)
    input = input_from_commands("f", "@1:", "q", "y")
    assert (
        interactive_version_filter(
            {
                Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
                Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
                Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
            },
            input=input,
        )
        is None
    )


def test_checksum_interactive_reset_resets():
    # Filter 1:, then reset, then filter :0, should just given 0.9 (it was filtered out
    # before reset)
    input = input_from_commands("f", "@1:", "r", "f", ":0", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz"}


def test_checksum_interactive_ask_each():
    # Ask each should run on the filtered list. First select 1.x, then select only the second
    # entry, which is 1.0.1.
    input = input_from_commands("f", "@1:", "a", "n", "y", "n")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {Version("1.0.1"): "https://www.example.com/pkg-1.0.1.tar.gz"}


def test_checksum_interactive_quit_from_ask_each():
    # Enter ask each mode, select the second item, then quit from submenu, then checksum, which
    # should still include the last item at which ask each stopped.
    input = input_from_commands("a", "n", "y", None, "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
        Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
    }


def test_checksum_interactive_nothing_left():
    """If nothing is left after interactive filtering, return an empty dict."""
    input = input_from_commands("f", "@2", "c")
    assert (
        interactive_version_filter(
            {
                Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
                Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
                Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
            },
            input=input,
        )
        == {}
    )


def test_checksum_interactive_new_only():
    # The 1.0 version is known already, and should be dropped on `n`.
    input = input_from_commands("n", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        known_versions=[Version("1.0")],
        input=input,
    ) == {
        Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
        Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
    }


def test_checksum_interactive_top_n():
    """Test integers select top n versions"""
    input = input_from_commands("2", "c")
    assert interactive_version_filter(
        {
            Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
            Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
            Version("0.9"): "https://www.example.com/pkg-0.9.tar.gz",
        },
        input=input,
    ) == {
        Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz",
        Version("1.0"): "https://www.example.com/pkg-1.0.tar.gz",
    }


def test_checksum_interactive_unrecognized_command():
    """Unrecognized commands should be ignored"""
    input = input_from_commands("-1", "0", "hello", "c")
    v = {Version("1.1"): "https://www.example.com/pkg-1.1.tar.gz"}
    assert interactive_version_filter(v.copy(), input=input) == v


def test_checksum_versions(mock_packages, can_fetch_versions, monkeypatch):
    pkg_cls = spack.repo.PATH.get_pkg_class("zlib")
    versions = [str(v) for v in pkg_cls.versions]
    output = spack_checksum("zlib", *versions)
    assert "Found 3 versions" in output
    assert "version(" in output


def test_checksum_missing_version(mock_packages, cannot_fetch_versions):
    output = spack_checksum("preferred-test", "99.99.99", fail_on_error=False)
    assert "Could not find any remote versions" in output
    output = spack_checksum("--add-to-package", "preferred-test", "99.99.99", fail_on_error=False)
    assert "Could not find any remote versions" in output


def test_checksum_deprecated_version(mock_packages, can_fetch_versions):
    output = spack_checksum("deprecated-versions", "1.1.0", fail_on_error=False)
    assert "Version 1.1.0 is deprecated" in output
    output = spack_checksum(
        "--add-to-package", "deprecated-versions", "1.1.0", fail_on_error=False
    )
    assert "Version 1.1.0 is deprecated" in output


def test_checksum_url(mock_packages, config):
    pkg_cls = spack.repo.PATH.get_pkg_class("zlib")
    with pytest.raises(spack.error.SpecSyntaxError):
        spack_checksum(f"{pkg_cls.url}")


def test_checksum_verification_fails(default_mock_concretization, capsys, can_fetch_versions):
    spec = spack.concretize.concretize_one("zlib")
    pkg = spec.package
    versions = list(pkg.versions.keys())
    version_hashes = {versions[0]: "abadhash", Version("0.1"): "123456789"}
    with pytest.raises(SystemExit):
        spack.cmd.checksum.print_checksum_status(pkg, version_hashes)
    out = str(capsys.readouterr())
    assert out.count("Correct") == 0
    assert "No previous checksum" in out
    assert "Invalid checksum" in out


def test_checksum_manual_download_fails(mock_packages, monkeypatch):
    """Confirm that checksumming a manually downloadable package fails."""
    name = "zlib"
    pkg_cls = spack.repo.PATH.get_pkg_class(name)
    versions = [str(v) for v in pkg_cls.versions]
    monkeypatch.setattr(spack.package_base.PackageBase, "manual_download", True)

    # First check that the exception is raised with the default download
    # instructions.
    with pytest.raises(ManualDownloadRequiredError, match=f"required for {name}"):
        spack_checksum(name, *versions)

    # Now check that the exception is raised with custom download instructions.
    error = "Cannot calculate the checksum for a manually downloaded package."
    monkeypatch.setattr(spack.package_base.PackageBase, "download_instr", error)
    with pytest.raises(ManualDownloadRequiredError, match=error):
        spack_checksum(name, *versions)


def test_upate_package_contents(tmp_path: pathlib.Path):
    """Test that the package.py file is updated with the new versions."""
    pkg_path = tmp_path / "package.py"
    pkg_path.write_text(
        """\
from spack.package import *

class Zlib(Package):
    homepage = "http://zlib.net"
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version("1.2.11", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    version("1.2.8", sha256="36658cb768a54c1d4dec43c3116c27ed893e88b02ecfcb44f2166f9c0b7f2a0d")
    version("1.2.3", sha256="1795c7d067a43174113fdf03447532f373e1c6c57c08d61d9e4e9be5e244b05e")
    variant("pic", default=True, description="test")

    def install(self, spec, prefix):
        make("install")
"""
    )
    version_lines = """\
    version("1.2.13", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.2.5", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.2.3", sha256="1795c7d067a43174113fdf03447532f373e1c6c57c08d61d9e4e9be5e244b05e")
"""
    # two new versions are added
    assert spack.cmd.checksum.add_versions_to_pkg(str(pkg_path), version_lines) == 2
    assert (
        pkg_path.read_text()
        == """\
from spack.package import *

class Zlib(Package):
    homepage = "http://zlib.net"
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version("1.2.13", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")  # FIXME
    version("1.2.11", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1")
    version("1.2.8", sha256="36658cb768a54c1d4dec43c3116c27ed893e88b02ecfcb44f2166f9c0b7f2a0d")
    version("1.2.5", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")  # FIXME
    version("1.2.3", sha256="1795c7d067a43174113fdf03447532f373e1c6c57c08d61d9e4e9be5e244b05e")
    variant("pic", default=True, description="test")

    def install(self, spec, prefix):
        make("install")
"""
    )
