# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys
import urllib.parse
from typing import List

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.repo
import spack.stage
from spack.spec import Spec
from spack.url import (
    UndetectableNameError,
    UndetectableVersionError,
    find_versions_of_archive,
    parse_name,
    parse_version,
)
from spack.util.editor import editor
from spack.util.executable import which
from spack.util.format import get_version_lines
from spack.util.naming import mod_to_class, simplify_name, valid_fully_qualified_module_name

description = "create a new package file"
section = "packaging"
level = "short"


package_template = '''\
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install {name}
#
# You can edit this file again by typing:
#
#     spack edit {name}
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class {class_name}({base_class_name}):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
{url_def}

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

{versions}

{dependencies}

{body_def}
'''


class BundlePackageTemplate:
    """
    Provides the default values to be used for a bundle package file template.
    """

    base_class_name = "BundlePackage"

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on("foo")"""

    url_def = "    # There is no URL since there is no code to download."
    body_def = "    # There is no need for install() since there is no code."

    def __init__(self, name: str, versions, languages: List[str]):
        self.name = name
        self.class_name = mod_to_class(name)
        self.versions = versions
        self.languages = languages

    def write(self, pkg_path):
        """Writes the new package file."""

        all_deps = [f'    depends_on("{lang}", type="build")' for lang in self.languages]
        if all_deps and self.dependencies:
            all_deps.append("")
        all_deps.append(self.dependencies)

        # Write out a template for the file
        with open(pkg_path, "w") as pkg_file:
            pkg_file.write(
                package_template.format(
                    name=self.name,
                    class_name=self.class_name,
                    base_class_name=self.base_class_name,
                    url_def=self.url_def,
                    versions=self.versions,
                    dependencies="\n".join(all_deps),
                    body_def=self.body_def,
                )
            )


class PackageTemplate(BundlePackageTemplate):
    """Provides the default values to be used for the package file template"""

    base_class_name = "Package"

    body_def = """\
    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make("install")"""

    url_line = '    url = "{url}"'

    def __init__(self, name, url, versions, languages: List[str]):
        super().__init__(name, versions, languages)

        self.url_def = self.url_line.format(url=url)


class AutotoolsPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Autotools-based packages
    that *do* come with a ``configure`` script"""

    base_class_name = "AutotoolsPackage"

    body_def = """\
    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args"""


class AutoreconfPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Autotools-based packages
    that *do not* come with a ``configure`` script"""

    base_class_name = "AutotoolsPackage"

    dependencies = """\
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # FIXME: Add additional dependencies if required.
    # depends_on("foo")"""

    body_def = """\
    def autoreconf(self, spec, prefix):
        # FIXME: Modify the autoreconf method as necessary
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args"""


class CargoPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for cargo-based packages"""

    base_class_name = "CargoPackage"

    body_def = ""


class CMakePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for CMake-based packages"""

    base_class_name = "CMakePackage"

    body_def = """\
    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args"""


class GoPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Go-module-based packages"""

    base_class_name = "GoPackage"

    body_def = ""


class LuaPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for LuaRocks-based packages"""

    base_class_name = "LuaPackage"

    body_def = """\
    def luarocks_args(self):
        # FIXME: Add arguments to `luarocks make` other than rockspec path
        # FIXME: If not needed delete this function
        args = []
        return args"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name lua-lpeg`, don't rename it lua-lua-lpeg
        if not name.startswith("lua-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to lua-{0}".format(name))
            name = "lua-{0}".format(name)
        super().__init__(name, url, versions, languages)


class MesonPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for meson-based packages"""

    base_class_name = "MesonPackage"

    body_def = """\
    def meson_args(self):
        # FIXME: If not needed delete this function
        args = []
        return args"""


class QMakePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for QMake-based packages"""

    base_class_name = "QMakePackage"

    body_def = """\
    def qmake_args(self):
        # FIXME: If not needed delete this function
        args = []
        return args"""


class MavenPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Maven-based packages"""

    base_class_name = "MavenPackage"

    body_def = """\
    def build(self, spec, prefix):
        # FIXME: If not needed delete this function
        pass"""


class SconsPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for SCons-based packages"""

    base_class_name = "SConsPackage"

    body_def = """\
    def build_args(self, spec, prefix):
        # FIXME: Add arguments to pass to build.
        # FIXME: If not needed delete this function
        args = []
        return args"""


class WafPackageTemplate(PackageTemplate):
    """Provides appropriate override for Waf-based packages"""

    base_class_name = "WafPackage"

    body_def = """\
    # FIXME: Override configure_args(), build_args(),
    # or install_args() if necessary."""


class BazelPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Bazel-based packages"""

    dependencies = """\
    # FIXME: Add additional dependencies if required.
    depends_on("bazel", type="build")"""

    body_def = """\
    def install(self, spec, prefix):
        # FIXME: Add logic to build and install here.
        bazel()"""


class RacketPackageTemplate(PackageTemplate):
    """Provides approriate overrides for Racket extensions"""

    base_class_name = "RacketPackage"

    url_line = """\
    # FIXME: set the proper location from which to fetch your package
    git = "git@github.com:example/example.git"
    """

    dependencies = """\
    # FIXME: Add dependencies if required. Only add the racket dependency
    # if you need specific versions. A generic racket dependency is
    # added implicity by the RacketPackage class.
    # depends_on("racket@8.3:", type=("build", "run"))"""

    body_def = """\
    # FIXME: specify the name of the package,
    # as it should appear to ``raco pkg install``
    name = "{0}"
    # FIXME: set to true if published on pkgs.racket-lang.org
    # pkgs = False
    # FIXME: specify path to the root directory of the
    # package, if not the base directory
    # subdirectory = None
    """

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name rkt-scribble`, don't rename it rkt-rkt-scribble
        if not name.startswith("rkt-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to rkt-{0}".format(name))
            name = "rkt-{0}".format(name)
        self.body_def = self.body_def.format(name[4:])
        super().__init__(name, url, versions, languages)


class PythonPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for python extensions"""

    base_class_name = "PythonPackage"

    dependencies = """\
    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    # depends_on("python@2.X:2.Y,3.Z:", type=("build", "run"))
    # depends_on("py-pip@X.Y:", type="build")
    # depends_on("py-wheel@X.Y:", type="build")

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    # depends_on("py-setuptools", type="build")
    # depends_on("py-hatchling", type="build")
    # depends_on("py-flit-core", type="build")
    # depends_on("py-poetry-core", type="build")

    # FIXME: Add additional dependencies if required.
    # depends_on("py-foo", type=("build", "run"))"""

    body_def = """\
    def config_settings(self, spec, prefix):
        # FIXME: Add configuration settings to be passed to the build backend
        # FIXME: If not needed, delete this function
        settings = {}
        return settings"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name py-numpy`, don't rename it py-py-numpy
        if not name.startswith("py-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to py-{0}".format(name))
            name = "py-{0}".format(name)

        # Simple PyPI URLs:
        # https://<hostname>/packages/<type>/<first character of project>/<project>/<download file>
        # e.g. https://pypi.io/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://www.pypi.io/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://pypi.org/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://pypi.python.org/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://files.pythonhosted.org/packages/source/n/numpy/numpy-1.19.4.zip

        # PyPI URLs containing hash:
        # https://<hostname>/packages/<two character hash>/<two character hash>/<longer hash>/<download file>
        # e.g. https://pypi.io/packages/c5/63/a48648ebc57711348420670bb074998f79828291f68aebfff1642be212ec/numpy-1.19.4.zip
        # e.g. https://files.pythonhosted.org/packages/c5/63/a48648ebc57711348420670bb074998f79828291f68aebfff1642be212ec/numpy-1.19.4.zip
        # e.g. https://files.pythonhosted.org/packages/c5/63/a48648ebc57711348420670bb074998f79828291f68aebfff1642be212ec/numpy-1.19.4.zip#sha256=141ec3a3300ab89c7f2b0775289954d193cc8edb621ea05f99db9cb181530512

        # PyPI URLs for wheels:
        # https://pypi.io/packages/py3/a/azureml_core/azureml_core-1.11.0-py3-none-any.whl
        # https://pypi.io/packages/py3/d/dotnetcore2/dotnetcore2-2.1.14-py3-none-macosx_10_9_x86_64.whl
        # https://pypi.io/packages/py3/d/dotnetcore2/dotnetcore2-2.1.14-py3-none-manylinux1_x86_64.whl
        # https://files.pythonhosted.org/packages/cp35.cp36.cp37.cp38.cp39/s/shiboken2/shiboken2-5.15.2-5.15.2-cp35.cp36.cp37.cp38.cp39-abi3-manylinux1_x86_64.whl
        # https://files.pythonhosted.org/packages/f4/99/ad2ef1aeeb395ee2319bb981ea08dbbae878d30dd28ebf27e401430ae77a/azureml_core-1.36.0.post2-py3-none-any.whl#sha256=60bcad10b4380d78a8280deb7365de2c2cd66527aacdcb4a173f613876cbe739

        match = re.search(r"(?:pypi|pythonhosted)[^/]+/packages" + "/([^/#]+)" * 4, url)
        if match:
            # PyPI URLs for wheels are too complicated, ignore them for now
            # https://www.python.org/dev/peps/pep-0427/#file-name-convention
            if not match.group(4).endswith(".whl"):
                if len(match.group(2)) == 1:
                    # Simple PyPI URL
                    url = "/".join(match.group(3, 4))
                else:
                    # PyPI URL containing hash
                    # Project name doesn't necessarily match download name, but it
                    # usually does, so this is the best we can do
                    project = parse_name(url)
                    url = "/".join([project, match.group(4)])

                self.url_line = '    pypi = "{url}"'
        else:
            # Add a reminder about spack preferring PyPI URLs
            self.url_line = (
                """
    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
"""
                + self.url_line
            )

        super().__init__(name, url, versions, languages)


class RPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for R extensions"""

    base_class_name = "RPackage"

    dependencies = """\
    # FIXME: Add dependencies if required.
    # depends_on("r-foo", type=("build", "run"))"""

    body_def = """\
    def configure_args(self):
        # FIXME: Add arguments to pass to install via --configure-args
        # FIXME: If not needed delete this function
        args = []
        return args"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name r-rcpp`, don't rename it r-r-rcpp
        if not name.startswith("r-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to r-{0}".format(name))
            name = "r-{0}".format(name)

        r_name = parse_name(url)

        cran = re.search(r"(?:r-project|rstudio)[^/]+/src" + "/([^/]+)" * 2, url)

        if cran:
            url = r_name
            self.url_line = '    cran = "{url}"'

        bioc = re.search(r"(?:bioconductor)[^/]+/packages" + "/([^/]+)" * 5, url)

        if bioc:
            self.url_line = '    url = "{0}"\n' '    bioc = "{1}"'.format(url, r_name)

        super().__init__(name, url, versions, languages)


class PerlmakePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Perl extensions
    that come with a Makefile.PL"""

    base_class_name = "PerlPackage"

    dependencies = """\
    # FIXME: Add dependencies if required:
    # depends_on("perl-foo", type=("build", "run"))"""

    body_def = """\
    def configure_args(self):
        # FIXME: Add non-standard arguments
        # FIXME: If not needed delete this function
        args = []
        return args"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name perl-cpp`, don't rename it perl-perl-cpp
        if not name.startswith("perl-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to perl-{0}".format(name))
            name = "perl-{0}".format(name)

        super().__init__(name, url, versions, languages)


class PerlbuildPackageTemplate(PerlmakePackageTemplate):
    """Provides appropriate overrides for Perl extensions
    that come with a Build.PL instead of a Makefile.PL"""

    dependencies = """\
    depends_on("perl-module-build", type="build")

    # FIXME: Add additional dependencies if required:
    # depends_on("perl-foo", type=("build", "run"))"""


class OctavePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for octave packages"""

    base_class_name = "OctavePackage"

    dependencies = """\
    extends("octave")

    # FIXME: Add additional dependencies if required.
    # depends_on("octave-foo", type=("build", "run"))"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name octave-splines`, don't rename it
        # octave-octave-splines
        if not name.startswith("octave-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to octave-{0}".format(name))
            name = "octave-{0}".format(name)

        super().__init__(name, url, versions, languages)


class RubyPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Ruby packages"""

    base_class_name = "RubyPackage"

    dependencies = """\
    # FIXME: Add dependencies if required. Only add the ruby dependency
    # if you need specific versions. A generic ruby dependency is
    # added implicity by the RubyPackage class.
    # depends_on("ruby@X.Y.Z:", type=("build", "run"))
    # depends_on("ruby-foo", type=("build", "run"))"""

    body_def = """\
    def build(self, spec, prefix):
        # FIXME: If not needed delete this function
        pass"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name ruby-numpy`, don't rename it
        # ruby-ruby-numpy
        if not name.startswith("ruby-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to ruby-{0}".format(name))
            name = "ruby-{0}".format(name)

        super().__init__(name, url, versions, languages)


class MakefilePackageTemplate(PackageTemplate):
    """Provides appropriate overrides for Makefile packages"""

    base_class_name = "MakefilePackage"

    body_def = """\
    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter("Makefile")
        # makefile.filter("CC = .*", "CC = cc")
        pass"""


class IntelPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for licensed Intel software"""

    base_class_name = "IntelPackage"

    body_def = """\
    # FIXME: Override `setup_environment` if necessary."""


class SIPPackageTemplate(PackageTemplate):
    """Provides appropriate overrides for SIP packages."""

    base_class_name = "SIPPackage"

    body_def = """\
    def configure_args(self, spec, prefix):
        # FIXME: Add arguments other than --bindir and --destdir
        # FIXME: If not needed delete this function
        args = []
        return args"""

    def __init__(self, name, url, versions, languages: List[str]):
        # If the user provided `--name py-pyqt4`, don't rename it py-py-pyqt4
        if not name.startswith("py-"):
            # Make it more obvious that we are renaming the package
            tty.msg("Changing package name from {0} to py-{0}".format(name))
            name = "py-{0}".format(name)

        super().__init__(name, url, versions, languages)


templates = {
    "autoreconf": AutoreconfPackageTemplate,
    "autotools": AutotoolsPackageTemplate,
    "bazel": BazelPackageTemplate,
    "bundle": BundlePackageTemplate,
    "cargo": CargoPackageTemplate,
    "cmake": CMakePackageTemplate,
    "generic": PackageTemplate,
    "go": GoPackageTemplate,
    "intel": IntelPackageTemplate,
    "lua": LuaPackageTemplate,
    "makefile": MakefilePackageTemplate,
    "maven": MavenPackageTemplate,
    "meson": MesonPackageTemplate,
    "octave": OctavePackageTemplate,
    "perlbuild": PerlbuildPackageTemplate,
    "perlmake": PerlmakePackageTemplate,
    "python": PythonPackageTemplate,
    "qmake": QMakePackageTemplate,
    "r": RPackageTemplate,
    "racket": RacketPackageTemplate,
    "ruby": RubyPackageTemplate,
    "scons": SconsPackageTemplate,
    "sip": SIPPackageTemplate,
    "waf": WafPackageTemplate,
}


def setup_parser(subparser):
    subparser.add_argument("url", nargs="?", help="url of package archive")
    subparser.add_argument(
        "--keep-stage",
        action="store_true",
        help="don't clean up staging area when command completes",
    )
    subparser.add_argument("-n", "--name", help="name of the package to create")
    subparser.add_argument(
        "-t",
        "--template",
        metavar="TEMPLATE",
        choices=sorted(templates.keys()),
        help="build system template to use\n\noptions: %(choices)s",
    )
    subparser.add_argument(
        "-r", "--repo", help="path to a repository where the package should be created"
    )
    subparser.add_argument(
        "-N",
        "--namespace",
        help="specify a namespace for the package\n\nmust be the namespace of "
        "a repository registered with Spack",
    )
    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite any existing package file with the same name",
    )
    subparser.add_argument(
        "--skip-editor",
        action="store_true",
        help="skip the edit session for the package (e.g., automation)",
    )
    subparser.add_argument(
        "-b", "--batch", action="store_true", help="don't ask which versions to checksum"
    )


#: C file extensions
C_EXT = {".c"}

#: C++ file extensions
CXX_EXT = {
    ".C",
    ".c++",
    ".cc",
    ".ccm",
    ".cpp",
    ".CPP",
    ".cxx",
    ".h++",
    ".hh",
    ".hpp",
    ".hxx",
    ".inl",
    ".ipp",
    ".ixx",
    ".tcc",
    ".tpp",
}

#: Fortran file extensions
FORTRAN_EXT = {
    ".f77",
    ".F77",
    ".f90",
    ".F90",
    ".f95",
    ".F95",
    ".f",
    ".F",
    ".for",
    ".FOR",
    ".ftn",
    ".FTN",
}


class BuildSystemAndLanguageGuesser:
    """An instance of BuildSystemAndLanguageGuesser provides a callable object to be used
    during ``spack create``. By passing this object to ``spack checksum``, we
    can take a peek at the fetched tarball and discern the build system it uses
    """

    def __init__(self):
        """Sets the default build system."""
        self.build_system = "generic"
        self._c = False
        self._cxx = False
        self._fortran = False

        # List of files in the archive ordered by their depth in the directory tree.
        self._file_entries: List[str] = []

    def __call__(self, archive: str, url: str) -> None:
        """Try to guess the type of build system used by a project based on
        the contents of its archive or the URL it was downloaded from."""

        # Peek inside the compressed file.
        if archive.endswith(".zip") or ".zip#" in archive:
            try:
                unzip = which("unzip")
                assert unzip is not None
                output = unzip("-lq", archive, output=str)
            except Exception:
                output = ""
        else:
            try:
                tar = which("tar")
                assert tar is not None
                output = tar("tf", archive, output=str)
            except Exception:
                output = ""
        self._file_entries[:] = output.splitlines()

        # Files closest to the root should be considered first when determining build system.
        self._file_entries.sort(key=lambda p: p.count("/"))

        self._determine_build_system(url)
        self._determine_language()

    def _determine_build_system(self, url: str) -> None:
        # Most octave extensions are hosted on Octave-Forge:
        #     https://octave.sourceforge.net/index.html
        # They all have the same base URL.
        if "downloads.sourceforge.net/octave/" in url:
            self.build_system = "octave"
        elif url.endswith(".gem"):
            self.build_system = "ruby"
        elif url.endswith(".whl") or ".whl#" in url:
            self.build_system = "python"
        elif url.endswith(".rock"):
            self.build_system = "lua"
        elif self._file_entries:
            # A list of clues that give us an idea of the build system a package
            # uses. If the regular expression matches a file contained in the
            # archive, the corresponding build system is assumed.
            # NOTE: Order is important here. If a package supports multiple
            # build systems, we choose the first match in this list.
            clues = [
                (re.compile(pattern), build_system)
                for pattern, build_system in (
                    (r"/CMakeLists\.txt$", "cmake"),
                    (r"/NAMESPACE$", "r"),
                    (r"/Cargo\.toml$", "cargo"),
                    (r"/go\.mod$", "go"),
                    (r"/configure$", "autotools"),
                    (r"/configure\.(in|ac)$", "autoreconf"),
                    (r"/Makefile\.am$", "autoreconf"),
                    (r"/pom\.xml$", "maven"),
                    (r"/SConstruct$", "scons"),
                    (r"/waf$", "waf"),
                    (r"/pyproject.toml", "python"),
                    (r"/setup\.(py|cfg)$", "python"),
                    (r"/WORKSPACE$", "bazel"),
                    (r"/Build\.PL$", "perlbuild"),
                    (r"/Makefile\.PL$", "perlmake"),
                    (r"/.*\.gemspec$", "ruby"),
                    (r"/Rakefile$", "ruby"),
                    (r"/setup\.rb$", "ruby"),
                    (r"/.*\.pro$", "qmake"),
                    (r"/.*\.rockspec$", "lua"),
                    (r"/(GNU)?[Mm]akefile$", "makefile"),
                    (r"/DESCRIPTION$", "octave"),
                    (r"/meson\.build$", "meson"),
                    (r"/configure\.py$", "sip"),
                )
            ]

            # Determine the build system based on the files contained in the archive.
            for file in self._file_entries:
                for pattern, build_system in clues:
                    if pattern.search(file):
                        self.build_system = build_system
                        return

    def _determine_language(self):
        for entry in self._file_entries:
            _, ext = os.path.splitext(entry)

            if not self._c and ext in C_EXT:
                self._c = True
            elif not self._cxx and ext in CXX_EXT:
                self._cxx = True
            elif not self._fortran and ext in FORTRAN_EXT:
                self._fortran = True

            if self._c and self._cxx and self._fortran:
                return

    @property
    def languages(self) -> List[str]:
        langs: List[str] = []
        if self._c:
            langs.append("c")
        if self._cxx:
            langs.append("cxx")
        if self._fortran:
            langs.append("fortran")
        return langs


def get_name(name, url):
    """Get the name of the package based on the supplied arguments.

    If a name was provided, always use that. Otherwise, if a URL was
    provided, extract the name from that. Otherwise, use a default.

    Args:
        name (str): explicit ``--name`` argument given to ``spack create``
        url (str): ``url`` argument given to ``spack create``

    Returns:
        str: The name of the package
    """

    # Default package name
    result = "example"

    if name is not None:
        # Use a user-supplied name if one is present
        result = name
        if len(name.strip()) > 0:
            tty.msg("Using specified package name: '{0}'".format(result))
        else:
            tty.die("A package name must be provided when using the option.")
    elif url is not None:
        # Try to guess the package name based on the URL
        try:
            result = parse_name(url)
            if result != url:
                desc = "URL"
            else:
                desc = "package name"
            tty.msg("This looks like a {0} for {1}".format(desc, result))
        except UndetectableNameError:
            tty.die(
                "Couldn't guess a name for this package.",
                "  Please report this bug. In the meantime, try running:",
                "  `spack create --name <name> <url>`",
            )

    result = simplify_name(result)

    if not valid_fully_qualified_module_name(result):
        tty.die("Package name can only contain a-z, 0-9, and '-'")

    return result


def get_url(url):
    """Get the URL to use.

    Use a default URL if none is provided.

    Args:
        url (str): ``url`` argument to ``spack create``

    Returns:
        str: The URL of the package
    """

    # Use the user-supplied URL or a default URL if none is present.
    return url or "https://www.example.com/example-1.2.3.tar.gz"


def get_versions(args, name):
    """Returns a list of versions and hashes for a package.

    Also returns a BuildSystemAndLanguageGuesser object.

    Returns default values if no URL is provided.

    Args:
        args (argparse.Namespace): The arguments given to ``spack create``
        name (str): The name of the package

    Returns:
        tuple: versions and hashes, and a BuildSystemAndLanguageGuesser object
    """

    # Default version with hash
    hashed_versions = """\
    # FIXME: Add proper versions and checksums here.
    # version("1.2.3", md5="0123456789abcdef0123456789abcdef")"""

    # Default version without hash
    unhashed_versions = """\
    # FIXME: Add proper versions here.
    # version("1.2.4")"""

    # Default guesser
    guesser = BuildSystemAndLanguageGuesser()

    valid_url = True
    try:
        parsed = urllib.parse.urlparse(args.url)
        if not parsed.scheme or parsed.scheme == "file":
            valid_url = False  # No point in spidering these
    except (ValueError, TypeError):
        valid_url = False

    if args.url is not None and args.template != "bundle" and valid_url:
        # Find available versions
        try:
            url_dict = find_versions_of_archive(args.url)
            if len(url_dict) > 1 and not args.batch and sys.stdin.isatty():
                url_dict_filtered = spack.stage.interactive_version_filter(url_dict)
                if url_dict_filtered is None:
                    exit(0)
                url_dict = url_dict_filtered
        except UndetectableVersionError:
            # Use fake versions
            tty.warn("Couldn't detect version in: {0}".format(args.url))
            return hashed_versions, guesser

        if not url_dict:
            # If no versions were found, revert to what the user provided
            version = parse_version(args.url)
            url_dict = {version: args.url}

        version_hashes = spack.stage.get_checksums_for_versions(
            url_dict, name, first_stage_function=guesser, keep_stage=args.keep_stage
        )

        versions = get_version_lines(version_hashes, url_dict)
    else:
        versions = unhashed_versions

    return versions, guesser


def get_build_system(template: str, url: str, guesser: BuildSystemAndLanguageGuesser) -> str:
    """Determine the build system template.

    If a template is specified, always use that. Otherwise, if a URL
    is provided, download the tarball and peek inside to guess what
    build system it uses. Otherwise, use a generic template by default.

    Args:
        template: ``--template`` argument given to ``spack create``
        url: ``url`` argument given to ``spack create``
        guesser: The first_stage_function given to ``spack checksum`` which records the build
            system it detects

    Returns:
        str: The name of the build system template to use
    """
    # Default template
    selected_template = "generic"

    if template is not None:
        selected_template = template
        # Use a user-supplied template if one is present
        tty.msg("Using specified package template: '{0}'".format(selected_template))
    elif url is not None:
        # Use whatever build system the guesser detected
        selected_template = guesser.build_system
        if selected_template == "generic":
            tty.warn("Unable to detect a build system. Using a generic package template.")
        else:
            msg = "This package looks like it uses the {0} build system"
            tty.msg(msg.format(selected_template))

    return selected_template


def get_repository(args, name):
    """Returns a Repo object that will allow us to determine the path where
    the new package file should be created.

    Args:
        args (argparse.Namespace): The arguments given to ``spack create``
        name (str): The name of the package to create

    Returns:
        spack.repo.Repo: A Repo object capable of determining the path to the
            package file
    """
    spec = Spec(name)
    # Figure out namespace for spec
    if spec.namespace and args.namespace and spec.namespace != args.namespace:
        tty.die("Namespaces '{0}' and '{1}' do not match.".format(spec.namespace, args.namespace))

    if not spec.namespace and args.namespace:
        spec.namespace = args.namespace

    # Figure out where the new package should live
    repo_path = args.repo
    if repo_path is not None:
        repo = spack.repo.from_path(repo_path)
        if spec.namespace and spec.namespace != repo.namespace:
            tty.die(
                "Can't create package with namespace {0} in repo with "
                "namespace {1}".format(spec.namespace, repo.namespace)
            )
    else:
        if spec.namespace:
            repo = spack.repo.PATH.get_repo(spec.namespace)
        else:
            repo = spack.repo.PATH.first_repo()

    # Set the namespace on the spec if it's not there already
    if not spec.namespace:
        spec.namespace = repo.namespace

    return repo


def create(parser, args):
    # Gather information about the package to be created
    name = get_name(args.name, args.url)
    url = get_url(args.url)
    versions, guesser = get_versions(args, name)
    build_system = get_build_system(args.template, url, guesser)

    # Create the package template object
    constr_args = {"name": name, "versions": versions, "languages": guesser.languages}
    package_class = templates[build_system]
    if package_class != BundlePackageTemplate:
        constr_args["url"] = url
    package = package_class(**constr_args)
    tty.msg("Created template for {0} package".format(package.name))

    # Create a directory for the new package
    repo = get_repository(args, name)
    pkg_path = repo.filename_for_package_name(package.name)
    if os.path.exists(pkg_path) and not args.force:
        tty.die(
            "{0} already exists.".format(pkg_path),
            "  Try running `spack create --force` to overwrite it.",
        )
    else:
        mkdirp(os.path.dirname(pkg_path))

    # Write the new package file
    package.write(pkg_path)
    tty.msg("Created package file: {0}".format(pkg_path))

    # Optionally open up the new package file in your $EDITOR
    if not args.skip_editor:
        editor(pkg_path)
