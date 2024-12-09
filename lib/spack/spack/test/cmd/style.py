# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import io
import os
import pathlib
import shutil
import sys

import pytest

from llnl.util.filesystem import FileFilter

import spack.cmd.style
import spack.main
import spack.paths
import spack.repo
from spack.cmd.style import _run_import_check, changed_files
from spack.util.executable import which

#: directory with sample style files
style_data = os.path.join(spack.paths.test_path, "data", "style")


style = spack.main.SpackCommand("style")


ISORT = which("isort")
BLACK = which("black")
FLAKE8 = which("flake8")
MYPY = which("mypy")


@pytest.fixture(autouse=True)
def has_develop_branch(git):
    """spack style requires git and a develop branch to run -- skip if we're missing either."""
    git("show-ref", "--verify", "--quiet", "refs/heads/develop", fail_on_error=False)
    if git.returncode != 0:
        pytest.skip("requires git and a develop branch")


@pytest.fixture(scope="function")
def flake8_package(tmpdir):
    """Style only checks files that have been modified. This fixture makes a small
    change to the ``flake8`` mock package, yields the filename, then undoes the
    change on cleanup.
    """
    repo = spack.repo.from_path(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("flake8")
    rel_path = os.path.dirname(os.path.relpath(filename, spack.paths.prefix))
    tmp = tmpdir / rel_path / "flake8-ci-package.py"
    tmp.ensure()
    tmp = str(tmp)

    shutil.copy(filename, tmp)
    package = FileFilter(tmp)
    package.filter("state = 'unmodified'", "state = 'modified'", string=True)
    yield tmp


@pytest.fixture
def flake8_package_with_errors(scope="function"):
    """A flake8 package with errors."""
    repo = spack.repo.from_path(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("flake8")
    tmp = filename + ".tmp"

    shutil.copy(filename, tmp)
    package = FileFilter(tmp)

    # this is a black error (quote style and spacing before/after operator)
    package.filter('state = "unmodified"', "state    =    'modified'", string=True)

    # this is an isort error (orderign) and a flake8 error (unused import)
    package.filter(
        "from spack.package import *", "from spack.package import *\nimport os", string=True
    )
    yield tmp


def test_changed_files_from_git_rev_base(git, tmpdir, capfd):
    """Test arbitrary git ref as base."""
    with tmpdir.as_cwd():
        git("init")
        git("checkout", "-b", "main")
        git("config", "user.name", "test user")
        git("config", "user.email", "test@user.com")
        git("commit", "--no-gpg-sign", "--allow-empty", "-m", "initial commit")

        tmpdir.ensure("bin/spack")
        assert changed_files(base="HEAD") == ["bin/spack"]
        assert changed_files(base="main") == ["bin/spack"]

        git("add", "bin/spack")
        git("commit", "--no-gpg-sign", "-m", "v1")
        assert changed_files(base="HEAD") == []
        assert changed_files(base="HEAD~") == ["bin/spack"]


def test_changed_no_base(git, tmpdir, capfd):
    """Ensure that we fail gracefully with no base branch."""
    tmpdir.join("bin").ensure("spack")
    with tmpdir.as_cwd():
        git("init")
        git("config", "user.name", "test user")
        git("config", "user.email", "test@user.com")
        git("add", ".")
        git("commit", "--no-gpg-sign", "-m", "initial commit")

        with pytest.raises(SystemExit):
            changed_files(base="foobar")

        out, err = capfd.readouterr()
        assert "This repository does not have a 'foobar'" in err


def test_changed_files_all_files():
    # it's hard to guarantee "all files", so do some sanity checks.
    files = set(
        [
            os.path.join(spack.paths.prefix, os.path.normpath(path))
            for path in changed_files(all_files=True)
        ]
    )

    # spack has a lot of files -- check that we're in the right ballpark
    assert len(files) > 6000

    # a builtin package
    zlib = spack.repo.PATH.get_pkg_class("zlib")
    zlib_file = zlib.module.__file__
    if zlib_file.endswith("pyc"):
        zlib_file = zlib_file[:-1]
    assert zlib_file in files

    # a core spack file
    assert os.path.join(spack.paths.module_path, "spec.py") in files

    # a mock package
    repo = spack.repo.from_path(spack.paths.mock_packages_path)
    filename = repo.filename_for_package_name("flake8")
    assert filename in files

    # this test
    assert __file__ in files

    # ensure externals are excluded
    assert not any(f.startswith(spack.paths.external_path) for f in files)


def test_bad_root(tmpdir):
    """Ensure that `spack style` doesn't run on non-spack directories."""
    output = style("--root", str(tmpdir), fail_on_error=False)
    assert "This does not look like a valid spack root" in output
    assert style.returncode != 0


def test_style_is_package(tmpdir):
    """Ensure the is_package() function works."""
    assert spack.cmd.style.is_package("var/spack/repos/builtin/packages/hdf5/package.py")
    assert spack.cmd.style.is_package("var/spack/repos/builtin/packages/zlib/package.py")
    assert not spack.cmd.style.is_package("lib/spack/spack/spec.py")
    assert not spack.cmd.style.is_package("lib/spack/external/pytest.py")


@pytest.fixture
def external_style_root(git, flake8_package_with_errors, tmpdir):
    """Create a mock git repository for running spack style."""
    # create a sort-of spack-looking directory
    script = tmpdir / "bin" / "spack"
    script.ensure()
    spack_dir = tmpdir / "lib" / "spack" / "spack"
    spack_dir.ensure("__init__.py")
    llnl_dir = tmpdir / "lib" / "spack" / "llnl"
    llnl_dir.ensure("__init__.py")

    # create a base develop branch
    with tmpdir.as_cwd():
        git("init")
        git("config", "user.name", "test user")
        git("config", "user.email", "test@user.com")
        git("add", ".")
        git("commit", "--no-gpg-sign", "-m", "initial commit")
        git("branch", "-m", "develop")
        git("checkout", "-b", "feature")

    # copy the buggy package in
    py_file = spack_dir / "dummy.py"
    py_file.ensure()
    shutil.copy(flake8_package_with_errors, str(py_file))

    # add the buggy file on the feature branch
    with tmpdir.as_cwd():
        git("add", str(py_file))
        git("commit", "--no-gpg-sign", "-m", "add new file")

    yield tmpdir, py_file


@pytest.mark.skipif(not ISORT, reason="isort is not installed.")
@pytest.mark.skipif(not BLACK, reason="black is not installed.")
def test_fix_style(external_style_root):
    """Make sure spack style --fix works."""
    tmpdir, py_file = external_style_root

    broken_dummy = os.path.join(style_data, "broken.dummy")
    broken_py = str(tmpdir / "lib" / "spack" / "spack" / "broken.py")
    fixed_py = os.path.join(style_data, "fixed.py")

    shutil.copy(broken_dummy, broken_py)
    assert not filecmp.cmp(broken_py, fixed_py)

    # black and isort are the tools that actually fix things
    style("--root", str(tmpdir), "--tool", "isort,black", "--fix")

    assert filecmp.cmp(broken_py, fixed_py)


@pytest.mark.skipif(not FLAKE8, reason="flake8 is not installed.")
@pytest.mark.skipif(not ISORT, reason="isort is not installed.")
@pytest.mark.skipif(not MYPY, reason="mypy is not installed.")
@pytest.mark.skipif(not BLACK, reason="black is not installed.")
def test_external_root(external_style_root, capfd):
    """Ensure we can run in a separate root directory w/o configuration files."""
    tmpdir, py_file = external_style_root

    # make sure tools are finding issues with external root,
    # not the real one.
    output = style("--root-relative", "--root", str(tmpdir), fail_on_error=False)

    # make sure it failed
    assert style.returncode != 0

    # isort error
    assert "%s Imports are incorrectly sorted" % str(py_file) in output

    # mypy error
    assert 'lib/spack/spack/dummy.py:10: error: Name "Package" is not defined' in output

    # black error
    assert "--- lib/spack/spack/dummy.py" in output
    assert "+++ lib/spack/spack/dummy.py" in output

    # flake8 error
    assert "lib/spack/spack/dummy.py:7: [F401] 'os' imported but unused" in output


@pytest.mark.skipif(not FLAKE8, reason="flake8 is not installed.")
def test_style(flake8_package, tmpdir):
    root_relative = os.path.relpath(flake8_package, spack.paths.prefix)

    # use a working directory to test cwd-relative paths, as tests run in
    # the spack prefix by default
    with tmpdir.as_cwd():
        relative = os.path.relpath(flake8_package)

        # one specific arg
        output = style("--tool", "flake8", flake8_package, fail_on_error=False)
        assert relative in output
        assert "spack style checks were clean" in output

        # specific file that isn't changed
        output = style("--tool", "flake8", __file__, fail_on_error=False)
        assert relative not in output
        assert __file__ in output
        assert "spack style checks were clean" in output

    # root-relative paths
    output = style("--tool", "flake8", "--root-relative", flake8_package)
    assert root_relative in output
    assert "spack style checks were clean" in output


@pytest.mark.skipif(not FLAKE8, reason="flake8 is not installed.")
def test_style_with_errors(flake8_package_with_errors):
    root_relative = os.path.relpath(flake8_package_with_errors, spack.paths.prefix)
    output = style(
        "--tool", "flake8", "--root-relative", flake8_package_with_errors, fail_on_error=False
    )
    assert root_relative in output
    assert style.returncode != 0
    assert "spack style found errors" in output


@pytest.mark.skipif(not BLACK, reason="black is not installed.")
@pytest.mark.skipif(not FLAKE8, reason="flake8 is not installed.")
def test_style_with_black(flake8_package_with_errors):
    output = style("--tool", "black,flake8", flake8_package_with_errors, fail_on_error=False)
    assert "black found errors" in output
    assert style.returncode != 0
    assert "spack style found errors" in output


def test_skip_tools():
    output = style("--skip", "import,isort,mypy,black,flake8")
    assert "Nothing to run" in output


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires Python 3.9+")
def test_run_import_check(tmp_path: pathlib.Path):
    file = tmp_path / "issues.py"
    contents = '''
import spack.cmd
import spack.config  # do not drop this import because of this comment

# this comment about spack.error should not be removed
class Example(spack.build_systems.autotools.AutotoolsPackage):
    """this is a docstring referencing unused spack.error.SpackError, which is fine"""
    pass

def foo(config: "spack.error.SpackError"):
    # the type hint is quoted, so it should not be removed
    spack.util.executable.Executable("example")
    print(spack.__version__)
'''
    file.write_text(contents)
    root = str(tmp_path)
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [str(file)],
        fix=False,
        out=output_buf,
        root_relative=False,
        root=spack.paths.prefix,
        working_dir=root,
    )
    output = output_buf.getvalue()

    assert "issues.py: redundant import: spack.cmd" in output
    assert "issues.py: redundant import: spack.config" not in output  # comment prevents removal
    assert "issues.py: missing import: spack" in output  # used by spack.__version__
    assert "issues.py: missing import: spack.build_systems.autotools" in output
    assert "issues.py: missing import: spack.util.executable" in output
    assert "issues.py: missing import: spack.error" not in output  # not directly used
    assert exit_code == 1
    assert file.read_text() == contents  # fix=False should not change the file

    # run it with --fix, should have the same output.
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [str(file)],
        fix=True,
        out=output_buf,
        root_relative=False,
        root=spack.paths.prefix,
        working_dir=root,
    )
    output = output_buf.getvalue()
    assert exit_code == 1
    assert "issues.py: redundant import: spack.cmd" in output
    assert "issues.py: missing import: spack" in output
    assert "issues.py: missing import: spack.build_systems.autotools" in output
    assert "issues.py: missing import: spack.util.executable" in output

    # after fix a second fix is idempotent
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [str(file)],
        fix=True,
        out=output_buf,
        root_relative=False,
        root=spack.paths.prefix,
        working_dir=root,
    )
    output = output_buf.getvalue()
    assert exit_code == 0
    assert not output

    # check that the file was fixed
    new_contents = file.read_text()
    assert "import spack.cmd" not in new_contents
    assert "import spack\n" in new_contents
    assert "import spack.build_systems.autotools\n" in new_contents
    assert "import spack.util.executable\n" in new_contents


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires Python 3.9+")
def test_run_import_check_syntax_error_and_missing(tmp_path: pathlib.Path):
    (tmp_path / "syntax-error.py").write_text("""this 'is n(ot python code""")
    output_buf = io.StringIO()
    exit_code = _run_import_check(
        [str(tmp_path / "syntax-error.py"), str(tmp_path / "missing.py")],
        fix=False,
        out=output_buf,
        root_relative=True,
        root=str(tmp_path),
        working_dir=str(tmp_path / "does-not-matter"),
    )
    output = output_buf.getvalue()
    assert "syntax-error.py: could not parse" in output
    assert "missing.py: could not parse" in output
    assert exit_code == 1


def test_case_sensitive_imports(tmp_path: pathlib.Path):
    # example.Example is a name, while example.example is a module.
    (tmp_path / "lib" / "spack" / "example").mkdir(parents=True)
    (tmp_path / "lib" / "spack" / "example" / "__init__.py").write_text("class Example:\n    pass")
    (tmp_path / "lib" / "spack" / "example" / "example.py").write_text("foo = 1")
    assert spack.cmd.style._module_part(str(tmp_path), "example.Example") == "example"


def test_pkg_imports():
    assert spack.cmd.style._module_part(spack.paths.prefix, "spack.pkg.builtin.boost") is None
    assert spack.cmd.style._module_part(spack.paths.prefix, "spack.pkg") is None
