# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

import llnl.util.tty as tty
from llnl.util.filesystem import find, working_dir

import spack.builder
import spack.install_test
import spack.package_base
from spack.directives import build_system, depends_on, extends
from spack.multimethod import when
from spack.util.executable import Executable

from ._checks import BaseBuilder, execute_install_time_tests


class SIPPackage(spack.package_base.PackageBase):
    """Specialized class for packages that are built using the
    SIP build system. See https://www.riverbankcomputing.com/software/sip/intro
    for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "SIPPackage"

    #: Name of private sip module to install alongside package
    sip_module = "sip"

    #: Callback names for install-time testing
    install_time_test_callbacks = ["test_imports"]
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "sip"

    build_system("sip")

    with when("build_system=sip"):
        extends("python", type=("build", "link", "run"))
        depends_on("py-sip", type="build")

    @property
    def import_modules(self):
        """Names of modules that the Python package provides.

        These are used to test whether or not the installation succeeded.
        These names generally come from running:

        .. code-block:: python

           >> import setuptools
           >> setuptools.find_packages()

        in the source tarball directory. If the module names are incorrectly
        detected, this property can be overridden by the package.

        Returns:
            list: list of strings of module names
        """
        modules = []
        root = os.path.join(self.prefix, self.spec["python"].package.platlib)

        # Some Python libraries are packages: collections of modules
        # distributed in directories containing __init__.py files
        for path in find(root, "__init__.py", recursive=True):
            modules.append(
                path.replace(root + os.sep, "", 1)
                .replace(os.sep + "__init__.py", "")
                .replace("/", ".")
            )

        # Some Python libraries are modules: individual *.py files
        # found in the site-packages directory
        for path in find(root, "*.py", recursive=False):
            modules.append(path.replace(root + os.sep, "", 1).replace(".py", "").replace("/", "."))

        modules = [mod for mod in modules if re.match("[a-zA-Z0-9._]+$", mod)]

        tty.debug("Detected the following modules: {0}".format(modules))

        return modules

    def python(self, *args, **kwargs):
        """The python ``Executable``."""
        self.pkg.module.python(*args, **kwargs)

    def test_imports(self):
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        for module in self.import_modules:
            with spack.install_test.test_part(
                self,
                "test_imports_{0}".format(module),
                purpose="checking import of {0}".format(module),
                work_dir="spack-test",
            ):
                self.python("-c", "import {0}".format(module))


@spack.builder.builder("sip")
class SIPBuilder(BaseBuilder):
    """The SIP builder provides the following phases that can be overridden:

    * configure
    * build
    * install

    The configure phase already adds a set of default flags. To see more
    options, run ``sip-build --help``.
    """

    phases = ("configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("configure_args", "build_args", "install_args")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "build_directory",
    )

    build_directory = "build"

    def configure(self, pkg, spec, prefix):
        """Configure the package."""

        # https://www.riverbankcomputing.com/static/Docs/sip/command_line_tools.html
        args = ["--verbose", "--target-dir", pkg.module.python_platlib]
        args.extend(self.configure_args())

        # https://github.com/Python-SIP/sip/commit/cb0be6cb6e9b756b8b0db3136efb014f6fb9b766
        if spec["py-sip"].satisfies("@6.1.0:"):
            args.extend(["--scripts-dir", pkg.prefix.bin])

        sip_build = Executable(spec["py-sip"].prefix.bin.join("sip-build"))
        sip_build(*args)

    def configure_args(self):
        """Arguments to pass to configure."""
        return []

    def build(self, pkg, spec, prefix):
        """Build the package."""
        args = self.build_args()

        with working_dir(self.build_directory):
            pkg.module.make(*args)

    def build_args(self):
        """Arguments to pass to build."""
        return []

    def install(self, pkg, spec, prefix):
        """Install the package."""
        args = self.install_args()

        with working_dir(self.build_directory):
            pkg.module.make("install", *args)

    def install_args(self):
        """Arguments to pass to install."""
        return []

    spack.builder.run_after("install")(execute_install_time_tests)
