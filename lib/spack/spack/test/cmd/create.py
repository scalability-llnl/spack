# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tarfile

import pytest

import spack.cmd.create
import spack.url
from spack.main import SpackCommand
from spack.url import UndetectableNameError
from spack.util.executable import which

create = SpackCommand("create")


@pytest.mark.parametrize(
    "args,name,expected",
    [
        # Basic package cases
        (["/test-package"], "test-package", [r"TestPackage(Package)", r"def install(self"]),
        (
            ["-n", "test-named-package", "file://example.tar.gz"],
            "test-named-package",
            [r"TestNamedPackage(Package)", r"def install(self"],
        ),
        (["file://example.tar.gz"], "example", [r"Example(Package)", r"def install(self"]),
        (
            ["-n", "test-license"],
            "test-license",
            [r'license("UNKNOWN", checked_by="github_user1")'],
        ),
        # Template-specific cases
        (
            ["-t", "autoreconf", "/test-autoreconf"],
            "test-autoreconf",
            [
                r"TestAutoreconf(AutotoolsPackage)",
                r'depends_on("autoconf',
                r"def autoreconf(self",
                r"def configure_args(self",
            ],
        ),
        (
            ["-t", "autotools", "/test-autotools"],
            "test-autotools",
            [r"TestAutotools(AutotoolsPackage)", r"def configure_args(self"],
        ),
        (
            ["-t", "bazel", "/test-bazel"],
            "test-bazel",
            [r"TestBazel(Package)", r'depends_on("bazel', r"bazel()"],
        ),
        (["-t", "bundle", "/test-bundle"], "test-bundle", [r"TestBundle(BundlePackage)"]),
        (
            ["-t", "cmake", "/test-cmake"],
            "test-cmake",
            [r"TestCmake(CMakePackage)", r"def cmake_args(self"],
        ),
        (
            ["-t", "intel", "/test-intel"],
            "test-intel",
            [r"TestIntel(IntelPackage)", r"setup_environment"],
        ),
        (
            ["-t", "makefile", "/test-makefile"],
            "test-makefile",
            [r"TestMakefile(MakefilePackage)", r"def edit(self", r"makefile"],
        ),
        (
            ["-t", "meson", "/test-meson"],
            "test-meson",
            [r"TestMeson(MesonPackage)", r"def meson_args(self"],
        ),
        (
            ["-t", "octave", "/test-octave"],
            "octave-test-octave",
            [r"OctaveTestOctave(OctavePackage)", r'extends("octave', r'depends_on("octave'],
        ),
        (
            ["-t", "perlbuild", "/test-perlbuild"],
            "perl-test-perlbuild",
            [
                r"PerlTestPerlbuild(PerlPackage)",
                r'depends_on("perl-module-build',
                r"def configure_args(self",
            ],
        ),
        (
            ["-t", "perlmake", "/test-perlmake"],
            "perl-test-perlmake",
            [r"PerlTestPerlmake(PerlPackage)", r'depends_on("perl-', r"def configure_args(self"],
        ),
        (
            ["-t", "python", "/test-python"],
            "py-test-python",
            [r"PyTestPython(PythonPackage)", r'depends_on("py-', r"def config_settings(self"],
        ),
        (
            ["-t", "qmake", "/test-qmake"],
            "test-qmake",
            [r"TestQmake(QMakePackage)", r"def qmake_args(self"],
        ),
        (
            ["-t", "r", "/test-r"],
            "r-test-r",
            [r"RTestR(RPackage)", r'depends_on("r-', r"def configure_args(self"],
        ),
        (
            ["-t", "scons", "/test-scons"],
            "test-scons",
            [r"TestScons(SConsPackage)", r"def build_args(self"],
        ),
        (
            ["-t", "sip", "/test-sip"],
            "py-test-sip",
            [r"PyTestSip(SIPPackage)", r"def configure_args(self"],
        ),
        (["-t", "waf", "/test-waf"], "test-waf", [r"TestWaf(WafPackage)", r"configure_args()"]),
    ],
)
def test_create_template(mock_test_repo, args, name, expected):
    """Test template creation."""
    repo, repodir = mock_test_repo

    create("--skip-editor", *args)

    filename = repo.filename_for_package_name(name)
    assert os.path.exists(filename)

    with open(filename, "r") as package_file:
        content = package_file.read()
        for entry in expected:
            assert entry in content

    black = which("black", required=False)
    if not black:
        pytest.skip("checking blackness of `spack create` output requires black")

    black("--check", "--diff", filename)


@pytest.mark.parametrize(
    "name,expected", [(" ", "name must be provided"), ("bad#name", "name can only contain")]
)
def test_create_template_bad_name(mock_test_repo, name, expected):
    """Test template creation with bad name options."""
    output = create("--skip-editor", "-n", name, fail_on_error=False)
    assert expected in output
    assert create.returncode != 0


def test_build_system_guesser_no_stage():
    """Test build system guesser when stage not provided."""
    guesser = spack.cmd.create.BuildSystemAndLanguageGuesser()

    # Ensure get the expected build system
    with pytest.raises(AttributeError, match="'NoneType' object has no attribute"):
        guesser(None, "/the/url/does/not/matter")


def test_build_system_guesser_octave(tmp_path):
    """
    Test build system guesser for the special case, where the same base URL
    identifies the build system rather than guessing the build system from
    files contained in the archive.
    """
    url, expected = "downloads.sourceforge.net/octave/", "octave"
    guesser = spack.cmd.create.BuildSystemAndLanguageGuesser()

    # Ensure get the expected build system
    guesser(str(tmp_path / "archive.tar.gz"), url)
    assert guesser.build_system == expected

    # Also ensure get the correct template
    bs = spack.cmd.create.get_build_system(None, url, guesser)
    assert bs == expected


@pytest.mark.parametrize(
    "url,expected", [("testname", "testname"), ("file://example.com/archive.tar.gz", "archive")]
)
def test_get_name_urls(url, expected):
    """Test get_name with different URLs."""
    name = spack.cmd.create.get_name(None, url)
    assert name == expected


def test_get_name_error(monkeypatch, capsys):
    """Test get_name UndetectableNameError exception path."""

    def _parse_name_offset(path, v):
        raise UndetectableNameError(path)

    monkeypatch.setattr(spack.url, "parse_name_offset", _parse_name_offset)

    url = "downloads.sourceforge.net/noapp/"

    with pytest.raises(SystemExit):
        spack.cmd.create.get_name(None, url)
    captured = capsys.readouterr()
    assert "Couldn't guess a name" in str(captured)


def test_no_url():
    """Test creation of package without a URL."""
    create("--skip-editor", "-n", "create-new-package")


@pytest.mark.parametrize(
    "source_files,languages",
    [
        (["fst.c", "snd.C"], ["c", "cxx"]),
        (["fst.c", "snd.cxx"], ["c", "cxx"]),
        (["fst.F", "snd.cc"], ["cxx", "fortran"]),
        (["fst.f", "snd.c"], ["c", "fortran"]),
        (["fst.jl", "snd.py"], []),
    ],
)
def test_language_and_build_system_detection(tmp_path, source_files, languages):
    """Test that languages are detected from tarball, and the build system is guessed from the
    most top-level build system file."""

    def add(tar: tarfile.TarFile, name: str, type):
        tarinfo = tarfile.TarInfo(name)
        tarinfo.type = type
        tar.addfile(tarinfo)

    tarball = str(tmp_path / "example.tar.gz")

    with tarfile.open(tarball, "w:gz") as tar:
        add(tar, "./third-party/", tarfile.DIRTYPE)
        add(tar, "./third-party/example/", tarfile.DIRTYPE)
        add(tar, "./third-party/example/CMakeLists.txt", tarfile.REGTYPE)  # false positive
        add(tar, "./configure", tarfile.REGTYPE)  # actual build system
        add(tar, "./src/", tarfile.DIRTYPE)
        for file in source_files:
            add(tar, f"src/{file}", tarfile.REGTYPE)

    guesser = spack.cmd.create.BuildSystemAndLanguageGuesser()
    guesser(str(tarball), "https://example.com")

    assert guesser.build_system == "autotools"
    assert guesser.languages == languages
