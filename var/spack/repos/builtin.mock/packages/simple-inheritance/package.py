# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BaseWithDirectives(Package):
    depends_on("cmake", type="build")
    depends_on("mpi")
    variant("openblas", description="Activates openblas", default=True)
    provides("service1")

    def use_module_variable(self):
        """Must be called in build environment. Allows us to test parent class
        using module variables set up by build_environment."""
        env["TEST_MODULE_VAR"] = "test_module_variable"
        return env["TEST_MODULE_VAR"]


class SimpleInheritance(BaseWithDirectives):
    """Simple package which acts as a build dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/simple-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("openblas", when="+openblas")
    provides("lapack", when="+openblas")
