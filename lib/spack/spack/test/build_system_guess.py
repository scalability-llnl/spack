# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.cmd.create
import spack.stage
import spack.util.executable
import spack.util.url as url_util


@pytest.fixture(
    scope="function",
    params=[
        ("configure", "autotools"),
        ("CMakeLists.txt", "cmake"),
        ("project.pro", "qmake"),
        ("pom.xml", "maven"),
        ("SConstruct", "scons"),
        ("waf", "waf"),
        ("argbah.rockspec", "lua"),
        ("setup.py", "python"),
        ("NAMESPACE", "r"),
        ("WORKSPACE", "bazel"),
        ("Makefile.PL", "perlmake"),
        ("Build.PL", "perlbuild"),
        ("foo.gemspec", "ruby"),
        ("Rakefile", "ruby"),
        ("setup.rb", "ruby"),
        ("GNUmakefile", "makefile"),
        ("makefile", "makefile"),
        ("Makefile", "makefile"),
        ("meson.build", "meson"),
        ("configure.py", "sip"),
        ("foobar", "generic"),
    ],
)
def url_and_build_system(request, tmpdir):
    """Sets up the resources to be pulled by the stage with
    the appropriate file name and returns their url along with
    the correct build-system guess
    """
    tar = spack.util.executable.which("tar")
    orig_dir = tmpdir.chdir()
    filename, system = request.param
    tmpdir.ensure("archive", filename)
    tar("czf", "archive.tar.gz", "archive")
    url = url_util.path_to_file_url(str(tmpdir.join("archive.tar.gz")))
    yield url, system
    orig_dir.chdir()


def test_build_systems(url_and_build_system):
    url, build_system = url_and_build_system
    with spack.stage.Stage(url) as stage:
        stage.fetch()
        guesser = spack.cmd.create.BuildSystemAndLanguageGuesser()
        guesser(stage.archive_file, url)
        assert build_system == guesser.build_system
