# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import pytest

import spack.cmd.compiler
import spack.compilers.config
import spack.config
import spack.main
import spack.util.pattern
import spack.version

compiler = spack.main.SpackCommand("compiler")


@pytest.fixture
def compilers_dir(mock_executable):
    """Create a directory with some mock compiler scripts in it.

    Scripts are:
      - clang
      - clang++
      - gcc
      - g++
      - gfortran-8

    """
    clang_path = mock_executable(
        "clang",
        output="""
if [ "$1" = "--version" ]; then
    echo "clang version 11.0.0 (clang-1100.0.33.16)"
    echo "Target: x86_64-apple-darwin18.7.0"
    echo "Thread model: posix"
    echo "InstalledDir: /dummy"
else
    echo "clang: error: no input files"
    exit 1
fi
""",
    )
    shutil.copy(clang_path, clang_path.parent / "clang++")

    gcc_script = """
if [ "$1" = "-dumpversion" ]; then
    echo "8"
elif [ "$1" = "-dumpfullversion" ]; then
    echo "8.4.0"
elif [ "$1" = "--version" ]; then
    echo "{0} (GCC) 8.4.0 20120313 (Red Hat 8.4.0-1)"
    echo "Copyright (C) 2010 Free Software Foundation, Inc."
else
    echo "{1}: fatal error: no input files"
    echo "compilation terminated."
    exit 1
fi
"""
    mock_executable("gcc-8", output=gcc_script.format("gcc", "gcc-8"))
    mock_executable("g++-8", output=gcc_script.format("g++", "g++-8"))
    mock_executable("gfortran-8", output=gcc_script.format("GNU Fortran", "gfortran-8"))

    return clang_path.parent


@pytest.mark.not_on_windows("Cannot execute bash script on Windows")
@pytest.mark.regression("11678,13138")
def test_compiler_find_without_paths(no_packages_yaml, working_env, mock_executable):
    """Tests that 'spack compiler find' looks into PATH by default, if no specific path
    is given.
    """
    gcc_path = mock_executable("gcc", output='echo "0.0.0"')

    os.environ["PATH"] = str(gcc_path.parent)
    output = compiler("find", "--scope=site")

    assert "gcc" in output


@pytest.mark.regression("37996")
def test_compiler_remove(mutable_config, mock_packages):
    """Tests that we can remove a compiler from configuration."""
    assert any(
        compiler.satisfies("gcc@=9.4.0") for compiler in spack.compilers.config.all_compilers()
    )
    args = spack.util.pattern.Bunch(all=True, compiler_spec="gcc@9.4.0", add_paths=[], scope=None)
    spack.cmd.compiler.compiler_remove(args)
    assert not any(
        compiler.satisfies("gcc@=9.4.0") for compiler in spack.compilers.config.all_compilers()
    )


@pytest.mark.regression("37996")
def test_removing_compilers_from_multiple_scopes(mutable_config, mock_packages):
    # Duplicate "site" scope into "user" scope
    site_config = spack.config.get("packages", scope="site")
    spack.config.set("packages", site_config, scope="user")

    assert any(
        compiler.satisfies("gcc@=9.4.0") for compiler in spack.compilers.config.all_compilers()
    )
    args = spack.util.pattern.Bunch(all=True, compiler_spec="gcc@9.4.0", add_paths=[], scope=None)
    spack.cmd.compiler.compiler_remove(args)
    assert not any(
        compiler.satisfies("gcc@=9.4.0") for compiler in spack.compilers.config.all_compilers()
    )


@pytest.mark.not_on_windows("Cannot execute bash script on Windows")
def test_compiler_add(mutable_config, mock_executable):
    """Tests that we can add a compiler to configuration."""
    expected_version = "4.5.3"
    gcc_path = mock_executable(
        "gcc",
        output=f"""\
for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '{expected_version}'
    fi
done
""",
    )
    bin_dir = gcc_path.parent
    root_dir = bin_dir.parent

    compilers_before_find = set(spack.compilers.config.all_compilers())
    args = spack.util.pattern.Bunch(
        all=None,
        compiler_spec=None,
        add_paths=[str(root_dir)],
        scope=None,
        mixed_toolchain=False,
        jobs=1,
    )
    spack.cmd.compiler.compiler_find(args)
    compilers_after_find = set(spack.compilers.config.all_compilers())

    compilers_added_by_find = compilers_after_find - compilers_before_find
    assert len(compilers_added_by_find) == 1
    new_compiler = compilers_added_by_find.pop()
    assert new_compiler.version == spack.version.Version(expected_version)


@pytest.mark.not_on_windows("Cannot execute bash script on Windows")
@pytest.mark.regression("17590")
def test_compiler_find_prefer_no_suffix(no_packages_yaml, working_env, compilers_dir):
    """Ensure that we'll pick 'clang' over 'clang-gpu' when there is a choice."""
    clang_path = compilers_dir / "clang"
    shutil.copy(clang_path, clang_path.parent / "clang-gpu")
    shutil.copy(clang_path, clang_path.parent / "clang++-gpu")

    os.environ["PATH"] = str(compilers_dir)
    output = compiler("find", "--scope=site")

    assert "llvm@11.0.0" in output
    assert "gcc@8.4.0" in output

    compilers = spack.compilers.config.all_compilers_from(no_packages_yaml, scope="site")
    clang = [x for x in compilers if x.satisfies("llvm@11")]

    assert len(clang) == 1
    assert clang[0].extra_attributes["compilers"]["c"] == str(compilers_dir / "clang")
    assert clang[0].extra_attributes["compilers"]["cxx"] == str(compilers_dir / "clang++")


@pytest.mark.not_on_windows("Cannot execute bash script on Windows")
def test_compiler_find_path_order(no_packages_yaml, working_env, compilers_dir):
    """Ensure that we look for compilers in the same order as PATH, when there are duplicates"""
    new_dir = compilers_dir / "first_in_path"
    new_dir.mkdir()
    for name in ("gcc-8", "g++-8", "gfortran-8"):
        shutil.copy(compilers_dir / name, new_dir / name)
    # Set PATH to have the new folder searched first
    os.environ["PATH"] = f"{str(new_dir)}:{str(compilers_dir)}"

    compiler("find", "--scope=site")

    compilers = spack.compilers.config.all_compilers(scope="site")
    gcc = [x for x in compilers if x.satisfies("gcc@8.4")]

    # Ensure we found both duplicates
    assert len(gcc) == 2
    assert gcc[0].extra_attributes["compilers"] == {
        "c": str(new_dir / "gcc-8"),
        "cxx": str(new_dir / "g++-8"),
        "fortran": str(new_dir / "gfortran-8"),
    }


def test_compiler_list_empty(no_packages_yaml, working_env, compilers_dir):
    """Spack should not automatically search for compilers when listing them and none are
    available. And when stdout is not a tty like in tests, there should be no output and
    no error exit code.
    """
    os.environ["PATH"] = str(compilers_dir)
    out = compiler("list")
    assert not out
    assert compiler.returncode == 0


@pytest.mark.parametrize(
    "external,expected",
    [
        (
            {
                "spec": "gcc@=7.7.7 languages=c,cxx,fortran os=foobar target=x86_64",
                "prefix": "/path/to/fake",
                "modules": ["gcc/7.7.7", "foobar"],
                "extra_attributes": {
                    "compilers": {
                        "c": "/path/to/fake/gcc",
                        "cxx": "/path/to/fake/g++",
                        "fortran": "/path/to/fake/gfortran",
                    },
                    "flags": {"fflags": "-ffree-form"},
                },
            },
            """gcc@7.7.7 languages=c,cxx,fortran os=foobar target=x86_64:
  paths:
    cc = /path/to/fake/gcc
    cxx = /path/to/fake/g++
\t\tf77 = /path/to/fake/gfortran
\t\tfc = /path/to/fake/gfortran
\tflags:
\t\tfflags = ['-ffree-form']
\tmodules  = ['gcc/7.7.7', 'foobar']
\toperating system  = foobar
""",
        )
    ],
)
def test_compilers_shows_packages_yaml(
    external, expected, no_packages_yaml, working_env, compilers_dir
):
    """Spack should see a single compiler defined from packages.yaml"""
    external["prefix"] = external["prefix"].format(prefix=os.path.dirname(compilers_dir))
    gcc_entry = {"externals": [external]}

    packages = spack.config.get("packages")
    packages["gcc"] = gcc_entry
    spack.config.set("packages", packages)

    out = compiler("list", fail_on_error=True)
    assert out.count("gcc@7.7.7") == 1
