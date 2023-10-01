# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc
import inspect
import os
from typing import List

import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
import spack.phase_callbacks
import spack.spec
import spack.util.prefix
from spack.directives import build_system, conflicts, depends_on, variant
from spack.multimethod import when

from ._checks import BuilderWithDefaults, execute_build_time_tests


class MesonPackage(spack.package_base.PackageBase):
    """Specialized class for packages built using Meson. For more information
    on the Meson build system, see https://mesonbuild.com/
    """

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "MesonPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "meson"

    build_system("meson")

    with when("build_system=meson"):
        variant(
            "buildtype",
            default="release",
            description="Meson build type",
            values=("plain", "debug", "debugoptimized", "release", "minsize"),
        )
        variant(
            "default_library",
            default="shared",
            values=("shared", "static"),
            multi=True,
            description="Build shared libs, static libs or both",
        )
        variant("strip", default=False, description="Strip targets on install")
        depends_on("meson", type="build")
        depends_on("ninja", type="build")
        # Python detection in meson requires distutils to be importable, but distutils no longer
        # exists in Python 3.12. In Spack, we can't use setuptools as distutils replacement,
        # because the distutils-precedence.pth startup file that setuptools ships with is not run
        # when setuptools is in PYTHONPATH; it has to be in system site-packages. In a future meson
        # release, the distutils requirement will be dropped, so this conflict can be relaxed.
        # We have patches to make it work with meson 1.1 and above.
        conflicts("^python@3.12:", when="^meson@:1.0")

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass the specified
        compiler flags to meson."""
        # Has to be dynamic attribute due to caching
        setattr(self, "meson_flag_args", [])


@spack.builder.builder("meson")
class MesonBuilder(BuilderWithDefaults):
    """The Meson builder encodes the default way to build software with Meson.
    The builder has three phases that can be overridden, if need be:

            1. :py:meth:`~.MesonBuilder.meson`
            2. :py:meth:`~.MesonBuilder.build`
            3. :py:meth:`~.MesonBuilder.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.MesonBuilder.meson_args`.

    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.MesonBuilder.root_mesonlists_dir` | Location of the    |
        |                                               | root MesonLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MesonBuilder.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+
    """

    phases = ("meson", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("meson_args", "check")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "root_mesonlists_dir",
        "std_meson_args",
        "build_directory",
    )

    build_targets: List[str] = []
    install_targets = ["install"]

    build_time_test_callbacks = ["check"]

    @property
    def archive_files(self):
        """Files to archive for packages based on Meson"""
        return [os.path.join(self.build_directory, "meson-logs", "meson-log.txt")]

    @property
    def root_mesonlists_dir(self) -> str:
        """Relative path to the directory containing meson.build

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.
        """
        return self.pkg.stage.source_path

    @property
    def std_meson_args(self) -> List[str]:
        """Standard meson arguments provided as a property for convenience
        of package writers.
        """
        # standard Meson arguments

        std_meson_args = MesonBuilder.std_args(self.pkg)
        std_meson_args += getattr(self, "meson_flag_args", [])
        return std_meson_args

    @staticmethod
    def std_args(pkg) -> List[str]:
        """Standard meson arguments for a generic package."""
        try:
            build_type = pkg.spec.variants["buildtype"].value
        except KeyError:
            build_type = "release"

        strip = "true" if "+strip" in pkg.spec else "false"

        if "default_library=static,shared" in pkg.spec:
            default_library = "both"
        elif "default_library=static" in pkg.spec:
            default_library = "static"
        else:
            default_library = "shared"

        return [
            "-Dprefix={0}".format(pkg.prefix),
            # If we do not specify libdir explicitly, Meson chooses something
            # like lib/x86_64-linux-gnu, which causes problems when trying to
            # find libraries and pkg-config files.
            # See https://github.com/mesonbuild/meson/issues/2197
            "-Dlibdir={0}".format(pkg.prefix.lib),
            "-Dbuildtype={0}".format(build_type),
            "-Dstrip={0}".format(strip),
            "-Ddefault_library={0}".format(default_library),
            # Do not automatically download and install dependencies
            "-Dwrap_mode=nodownload",
        ]

    @staticmethod
    def define(meson_var, value):
        """Return a meson command line argument that defines a variable.

        The resulting argument will convert boolean values to false/true
        and lists/tuples to meson colon-separated string lists. All other
        values will be interpreted as strings.

        Examples:

            .. code-block:: python

                [define('prefer_static', True),
                 define('cpp_std', 14),
                 define('swr', ['avx', 'avx2'])]

            will generate the following configuration options:

            .. code-block:: console

                ["-Dprefer_static=true",
                 "-Dcpp_std=14",
                 "-Dswr=avx,avx2]

        """
        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        if isinstance(value, bool):
            value = "true" if value else "false"
        else:
            if isinstance(value, collections.abc.Sequence) and not isinstance(value, str):
                value = ",".join(str(v) for v in value)
            else:
                value = str(value)

        return "".join(["-D", meson_var, "=", value])

    def define_from_variant(self, meson_var, variant=None):
        """Return a meson command line argument from the given variant's value.

        The optional ``variant`` argument defaults to the lower-case transform
        of ``meson_var``.

        This utility function is similar to
        :meth:`~spack.build_systems.autotools.AutotoolsBuilder.with_or_without`.

        Examples:

            Given a package with:

            .. code-block:: python

                variant('cxxstd', default='11', values=('11', '14'),
                        multi=False, description='')
                variant('static', default=True, description='')
                variant('swr', values=any_combination_of('avx', 'avx2'),
                        description='')

            calling this function like:

            .. code-block:: python

                [self.define_from_variant('prefer_static', 'static'),
                 self.define_from_variant('cpp_std', 'cxxstd'),
                 self.define_from_variant('swr')]

            will generate the following configuration options:

            .. code-block:: console

                ["-Dprefer_static=true",
                 "-Dcpp_std=14",
                 "-Dswr=avx,avx2]

            for ``<spec-name> cxxstd=14 +shared swr=avx,avx2``

        Note: if the provided variant is conditional, and the condition is not met,
                this function returns an empty string. Meson does NOT discard empty
                strings provided on the command line.
        """

        if variant is None:
            variant = meson_var.lower()

        if variant not in self.pkg.variants:
            raise KeyError('"{0}" is not a variant of "{1}"'.format(variant, self.pkg.name))

        if variant not in self.pkg.spec.variants:
            return ""

        value = self.pkg.spec.variants[variant].value
        if isinstance(value, (tuple, list)):
            # Sort multi-valued variants for reproducibility
            value = sorted(value)

        return self.define(meson_var, value)

    @property
    def build_dirname(self):
        """Returns the directory name to use when building the package."""
        return "spack-build-{}".format(self.spec.dag_hash(7))

    @property
    def build_directory(self):
        """Directory to use when building the package."""
        return os.path.join(self.pkg.stage.path, self.build_dirname)

    def meson_args(self) -> List[str]:
        """List of arguments that must be passed to meson, except:

        * ``--prefix``
        * ``--libdir``
        * ``--buildtype``
        * ``--strip``
        * ``--default_library``

        which will be set automatically.
        """
        return []

    def meson(
        self,
        pkg: spack.package_base.PackageBase,
        spec: spack.spec.Spec,
        prefix: spack.util.prefix.Prefix,
    ) -> None:
        """Run ``meson`` in the build directory"""
        options = []
        if self.spec["meson"].satisfies("@0.64:"):
            options.append("setup")
        options.append(os.path.abspath(self.root_mesonlists_dir))
        options += self.std_meson_args
        options += self.meson_args()
        with fs.working_dir(self.build_directory, create=True):
            pkg.module.meson(*options)

    def build(
        self,
        pkg: spack.package_base.PackageBase,
        spec: spack.spec.Spec,
        prefix: spack.util.prefix.Prefix,
    ) -> None:
        """Make the build targets"""
        options = ["-v"]
        options += self.build_targets
        with fs.working_dir(self.build_directory):
            pkg.module.ninja(*options)

    def install(
        self,
        pkg: spack.package_base.PackageBase,
        spec: spack.spec.Spec,
        prefix: spack.util.prefix.Prefix,
    ) -> None:
        """Make the install targets"""
        with fs.working_dir(self.build_directory):
            pkg.module.ninja(*self.install_targets)

    spack.phase_callbacks.run_after("build")(execute_build_time_tests)

    def check(self) -> None:
        """Search Meson-generated files for the target ``test`` and run it if found."""
        with fs.working_dir(self.build_directory):
            self.pkg._if_ninja_target_execute("test")
            self.pkg._if_ninja_target_execute("check")
