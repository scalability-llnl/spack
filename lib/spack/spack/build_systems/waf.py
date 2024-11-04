# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from llnl.util.filesystem import working_dir

import spack.builder
import spack.package_base
from spack.directives import build_system, depends_on

from ._checks import BaseBuilder, execute_build_time_tests, execute_install_time_tests


class WafPackage(spack.package_base.PackageBase):
    """Specialized class for packages that are built using the
    Waf build system. See https://waf.io/book/ for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "WafPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "waf"

    build_system("waf")
    # Much like AutotoolsPackage does not require automake and autoconf
    # to build, WafPackage does not require waf to build. It only requires
    # python to run the waf build script.
    depends_on("python@2.5:", type="build", when="build_system=waf")


@spack.builder.builder("waf")
class WafBuilder(BaseBuilder):
    """The WAF builder provides the following phases that can be overridden:

    * configure
    * build
    * install

    These are all standard Waf commands and can be found by running:

    .. code-block:: console

       $ python waf --help

    Each phase provides a function <phase> that runs:

    .. code-block:: console

       $ python waf -j<jobs> <phase>

    where <jobs> is the number of parallel jobs to build with. Each phase
    also has a <phase_args> function that can pass arguments to this call.
    All of these functions are empty except for the ``configure_args``
    function, which passes ``--prefix=/path/to/installation/prefix``.
    """

    phases = ("configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = (
        "build_test",
        "install_test",
        "configure_args",
        "build_args",
        "install_args",
        "build_test",
        "install_test",
    )

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_time_test_callbacks",
        "build_directory",
        "install_time_test_callbacks",
    )

    # Callback names for build-time test
    build_time_test_callbacks = ["build_test"]

    # Callback names for install-time test
    install_time_test_callbacks = ["install_test"]

    @property
    def build_directory(self):
        """The directory containing the ``waf`` file."""
        return self.stage.source_path

    def python(self, *args, **kwargs):
        """The python ``Executable``."""
        self.pkg.module.python(*args, **kwargs)

    def waf(self, *args, **kwargs):
        """Runs the waf ``Executable``."""
        jobs = self.pkg.module.make_jobs

        with working_dir(self.build_directory):
            self.python("waf", "-j{0}".format(jobs), *args, **kwargs)

    def configure(self, pkg, spec, prefix):
        """Configures the project."""
        args = ["--prefix={0}".format(self.pkg.prefix)]
        args += self.configure_args()

        self.waf("configure", *args)

    def configure_args(self):
        """Arguments to pass to configure."""
        return []

    def build(self, pkg, spec, prefix):
        """Executes the build."""
        args = self.build_args()

        self.waf("build", *args)

    def build_args(self):
        """Arguments to pass to build."""
        return []

    def install(self, pkg, spec, prefix):
        """Installs the targets on the system."""
        args = self.install_args()

        self.waf("install", *args)

    def install_args(self):
        """Arguments to pass to install."""
        return []

    def build_test(self):
        """Run unit tests after build.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    spack.builder.run_after("build")(execute_build_time_tests)

    def install_test(self):
        """Run unit tests after install.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    spack.builder.run_after("install")(execute_install_time_tests)
