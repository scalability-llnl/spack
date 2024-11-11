# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from llnl.util.symlink import _windows_can_symlink

import spack.concretize
import spack.util.spack_yaml as s_yaml
from spack.installer import PackageInstaller
from spack.main import SpackCommand

extensions = SpackCommand("extensions")
install = SpackCommand("install")
view = SpackCommand("view")

if sys.platform == "win32":
    if not _windows_can_symlink():
        pytest.skip(
            "Windows must be able to create symlinks to run tests.", allow_module_level=True
        )
    # TODO: Skipping hardlink command testing on windows until robust checks can be added.
    #   See https://github.com/spack/spack/pull/46335#discussion_r1757411915
    commands = ["symlink", "add", "copy", "relocate"]
else:
    commands = ["hardlink", "symlink", "hard", "add", "copy", "relocate"]


def create_projection_file(tmp_path, projection):
    if "projections" not in projection:
        projection = {"projections": projection}
    projection_file = tmp_path / "projection" / "projection.yaml"
    projection_file.parent.mkdir(parents=True, exist_ok=True)
    projection_file.write_text(s_yaml.dump(projection))
    return projection_file


@pytest.mark.parametrize("cmd", commands)
def test_view_link_type(tmp_path, mock_packages, mock_archive, mock_fetch, install_mockery, cmd):
    install("--fake", "libdwarf")
    view_dir = tmp_path / f"view_{cmd}"
    view(cmd, str(view_dir), "libdwarf")
    package_bin = view_dir / "bin" / "libdwarf"
    assert package_bin.exists()

    # Check that we use symlinks for and only for the appropriate subcommands
    is_link_cmd = cmd in ("symlink", "add")
    assert os.path.islink(str(package_bin)) == is_link_cmd


@pytest.mark.parametrize("add_cmd", commands)
def test_view_link_type_remove(
    tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery, add_cmd
):
    install("needs-relocation")
    viewpath = str(tmpdir.mkdir("view_{0}".format(add_cmd)))
    view(add_cmd, viewpath, "needs-relocation")
    bindir = os.path.join(viewpath, "bin")
    assert os.path.exists(bindir)

    view("remove", viewpath, "needs-relocation")
    assert not os.path.exists(bindir)


@pytest.mark.parametrize("cmd", commands)
def test_view_projections(tmp_path, mock_packages, mock_archive, mock_fetch, install_mockery, cmd):
    install("--fake", "libdwarf@20130207")
    view_dir = tmp_path / f"view_{cmd}"

    view_projection = {"projections": {"all": "{name}-{version}"}}
    projection_file = create_projection_file(tmp_path, view_projection)
    view(cmd, str(view_dir), f"--projection-file={projection_file}", "libdwarf")

    package_bin = view_dir / "libdwarf-20130207" / "bin" / "libdwarf"
    assert package_bin.exists()

    # Check that we use symlinks for and only for the appropriate subcommands
    is_symlink_cmd = cmd in ("symlink", "add")
    assert package_bin.is_symlink() == is_symlink_cmd


def test_view_multiple_projections(
    tmp_path, mock_packages, mock_archive, mock_fetch, install_mockery
):
    install("--fake", "libdwarf@20130207")
    install("--fake", "extendee@1.0")
    view_dir = tmp_path / "view"

    view_projection = s_yaml.syaml_dict(
        [("extendee", "{name}-{architecture.platform}"), ("all", "{name}-{version}")]
    )

    projection_file = create_projection_file(tmp_path, view_projection)
    view("add", str(view_dir), f"--projection-file={projection_file}", "libdwarf", "extendee")

    libdwarf_prefix = view_dir / "libdwarf-20130207" / "bin"
    extendee_prefix = view_dir / "extendee-test" / "bin"
    assert libdwarf_prefix.exists()
    assert extendee_prefix.exists()


def test_view_multiple_projections_all_first(
    tmp_path, mock_packages, mock_archive, mock_fetch, install_mockery
):
    install("--fake", "libdwarf@20130207")
    install("--fake", "extendee@1.0")
    view_dir = tmp_path / "view"

    view_projection = s_yaml.syaml_dict(
        [("all", "{name}-{version}"), ("extendee", "{name}-{architecture.platform}")]
    )

    projection_file = create_projection_file(tmp_path, view_projection)
    view("add", str(view_dir), f"--projection-file={projection_file}", "libdwarf", "extendee")

    libdwarf_prefix = view_dir / "libdwarf-20130207" / "bin"
    extendee_prefix = view_dir / "extendee-test" / "bin"
    assert libdwarf_prefix.exists()
    assert extendee_prefix.exists()


def test_view_external(tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery):
    install("externaltool")
    viewpath = str(tmpdir.mkdir("view"))
    output = view("symlink", viewpath, "externaltool")
    assert "Skipping external package: externaltool" in output


def test_view_extension(tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery):
    install("extendee")
    install("extension1@1.0")
    install("extension1@2.0")
    install("extension2@1.0")
    viewpath = str(tmpdir.mkdir("view"))
    view("symlink", viewpath, "extension1@1.0")
    all_installed = extensions("--show", "installed", "extendee")
    assert "extension1@1.0" in all_installed
    assert "extension1@2.0" in all_installed
    assert "extension2@1.0" in all_installed
    assert os.path.exists(os.path.join(viewpath, "bin", "extension1"))


def test_view_extension_remove(tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery):
    install("extendee")
    install("extension1@1.0")
    viewpath = str(tmpdir.mkdir("view"))
    view("symlink", viewpath, "extension1@1.0")
    view("remove", viewpath, "extension1@1.0")
    all_installed = extensions("--show", "installed", "extendee")
    assert "extension1@1.0" in all_installed
    assert not os.path.exists(os.path.join(viewpath, "bin", "extension1"))


def test_view_extension_conflict(tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery):
    install("extendee")
    install("extension1@1.0")
    install("extension1@2.0")
    viewpath = str(tmpdir.mkdir("view"))
    view("symlink", viewpath, "extension1@1.0")
    output = view("symlink", viewpath, "extension1@2.0")
    assert "Package conflict detected" in output


def test_view_extension_conflict_ignored(
    tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery
):
    install("extendee")
    install("extension1@1.0")
    install("extension1@2.0")
    viewpath = str(tmpdir.mkdir("view"))
    view("symlink", viewpath, "extension1@1.0")
    view("symlink", viewpath, "-i", "extension1@2.0")
    with open(os.path.join(viewpath, "bin", "extension1"), "r", encoding="utf-8") as fin:
        assert fin.read() == "1.0"


def test_view_fails_with_missing_projections_file(tmpdir):
    viewpath = str(tmpdir.mkdir("view"))
    projection_file = os.path.join(str(tmpdir), "nonexistent")
    with pytest.raises(SystemExit):
        view("symlink", "--projection-file", projection_file, viewpath, "foo")


@pytest.mark.parametrize("with_projection", [False, True])
@pytest.mark.parametrize("cmd", ["symlink", "copy"])
def test_view_files_not_ignored(
    tmpdir, mock_packages, mock_archive, mock_fetch, install_mockery, cmd, with_projection
):
    spec = spack.concretize.concretize_one("view-not-ignored")
    pkg = spec.package
    PackageInstaller([pkg], explicit=True).install()
    pkg.assert_installed(spec.prefix)

    install("view-file")  # Arbitrary package to add noise

    viewpath = str(tmpdir.mkdir("view_{0}".format(cmd)))

    if with_projection:
        proj = str(tmpdir.join("proj.yaml"))
        with open(proj, "w", encoding="utf-8") as f:
            f.write('{"projections":{"all":"{name}"}}')
        prefix_in_view = os.path.join(viewpath, "view-not-ignored")
        args = ["--projection-file", proj]
    else:
        prefix_in_view = viewpath
        args = []

    view(cmd, *(args + [viewpath, "view-not-ignored", "view-file"]))
    pkg.assert_installed(prefix_in_view)

    view("remove", viewpath, "view-not-ignored")
    pkg.assert_not_installed(prefix_in_view)
