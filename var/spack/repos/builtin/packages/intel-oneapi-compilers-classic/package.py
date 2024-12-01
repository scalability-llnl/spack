# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

from llnl.util.lang import classproperty
from llnl.util.link_tree import LinkTree

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiCompilersClassic(Package, CompilerPackage):
    """Relies on intel-oneapi-compilers to install the compilers, and
    configures modules for icc/icpc/ifort.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    has_code = False

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["icc"]
    cxx_names = ["icpc"]
    fortran_names = ["ifort"]

    @classproperty
    def compiler_version_argument(self):
        if sys.platform == "win32":
            return "/QV"
        return "--version"

    @classproperty
    def compiler_version_regex(self):
        if sys.platform == "win32":
            return r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"
        return r"\((?:IFORT|ICC)\) ([^ ]+)"

    # Versions before 2021 are in the `intel` package
    # intel-oneapi versions before 2022 use intel@19.0.4
    for ver, oneapi_ver in {
        "2021.1.2": "2021.1.2",
        "2021.2.0": "2021.2.0",
        "2021.3.0": "2021.3.0",
        "2021.4.0": "2021.4.0",
        "2021.5.0": "2022.0.1:2022.0.2",
        "2021.6.0": "2022.1.0",
        "2021.7.0": "2022.2.0",
        "2021.7.1": "2022.2.1",
        "2021.8.0": "2023.0.0",
        "2021.9.0": "2023.1.0",
        "2021.10.0": "2023.2.4",
        "2021.11.1": "2024.0.2",
    }.items():
        # prefer 2021.10.0 because it is the last one that has a C compiler
        version(ver, preferred=(ver == "2021.10.0"))
        depends_on("intel-oneapi-compilers@" + oneapi_ver, when="@" + ver, type="run")

    # icc@2021.6.0 does not support gcc@12 headers
    conflicts("%gcc@12:", when="@:2021.6.0")

    @property
    def oneapi_compiler_prefix(self):
        oneapi_version = self.spec["intel-oneapi-compilers"].version
        return self.spec["intel-oneapi-compilers"].prefix.compiler.join(str(oneapi_version))

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:
        .. code-block:: console
           $ source {prefix}/{component}/{version}/env/vars.sh
        and from setting CC/CXX/F77/FC
        """
        oneapi_pkg = self.spec["intel-oneapi-compilers"].package

        oneapi_pkg.setup_run_environment(env)

        bin_prefix = oneapi_pkg.component_prefix.linux.bin.intel64
        env.set("CC", bin_prefix.icc)
        env.set("CXX", bin_prefix.icpc)
        env.set("F77", bin_prefix.ifort)
        env.set("FC", bin_prefix.ifort)

    def install(self, spec, prefix):
        # If we symlink top-level directories directly, files won't show up in views
        # Create real dirs and symlink files instead
        self.symlink_dir(self.oneapi_compiler_prefix.linux.bin.intel64, prefix.bin)
        self.symlink_dir(self.oneapi_compiler_prefix.linux.lib, prefix.lib)
        self.symlink_dir(self.oneapi_compiler_prefix.linux.include, prefix.include)
        self.symlink_dir(self.oneapi_compiler_prefix.linux.compiler, prefix.compiler)
        self.symlink_dir(self.oneapi_compiler_prefix.documentation.en.man, prefix.man)

    def symlink_dir(self, src, dest):
        # Create a real directory at dest
        mkdirp(dest)

        # Symlink all files in src to dest keeping directories as dirs
        for entry in os.listdir(src):
            src_path = os.path.join(src, entry)
            dest_path = os.path.join(dest, entry)
            if os.path.isdir(src_path) and os.access(src_path, os.X_OK):
                link_tree = LinkTree(src_path)
                link_tree.merge(dest_path)
            else:
                os.symlink(src_path, dest_path)
