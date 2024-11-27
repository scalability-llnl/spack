# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLiblas(PythonPackage):
    """libLAS is a C/C++ library for reading and writing the very common
    LAS LiDAR format.
    """

    homepage = "https://liblas.org/"
    pypi = "libLAS/libLAS-1.8.1.tar.gz"

    version("1.8.1", sha256="4d517670912989a0c7a33bb057167747e1013db6abdaa372f0775343ff0d1e16")

    depends_on("py-setuptools", type="build")
    depends_on("liblas")

    def setup_build_environment(self, env):
        env_var = "LD_LIBRARY_PATH"
        if self.spec.satisfies("platform=darwin"):
            env_var = "DYLD_FALLBACK_LIBRARY_PATH"
        env.prepend_path(env_var, self.spec["liblas"].libs.directories[0])

    setup_run_environment = setup_build_environment
