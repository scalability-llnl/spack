# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYarl(PythonPackage):
    """The module provides handy URL class for URL parsing and changing."""

    homepage = "https://github.com/aio-libs/yarl"
    pypi = "yarl/yarl-1.4.2.tar.gz"

    license("Apache-2.0")

    version("1.9.2", sha256="04ab9d4b9f587c06d801c2abfe9317b77cdf996c65a90d5e84ecc45010823571")
    version("1.8.1", sha256="af887845b8c2e060eb5605ff72b6f2dd2aab7a761379373fd89d314f4752abbf")
    version("1.7.2", sha256="45399b46d60c253327a460e99856752009fcee5f5d3c80b2f7c0cae1c38d56dd")
    version("1.4.2", sha256="58cd9c469eced558cd81aa3f484b2924e8897049e06889e8ff2510435b7ef74b")
    version("1.3.0", sha256="024ecdc12bc02b321bc66b41327f930d1c2c543fa9a561b39861da9388ba7aa9")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@40:", type="build", when="@1.7.2:")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")

    depends_on("py-multidict@4.0:", type=("build", "run"))
    depends_on("py-idna@2.0:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@1.7.2: ^python@:3.7", type=("build", "run"))

    @run_before("install")
    def fix_cython(self):
        if self.spec.satisfies("@1.7.2:"):
            pyxfile = "yarl/_quoting_c"
        else:
            pyxfile = "yarl/_quoting"

        cython = self.spec["py-cython"].command
        cython("-3", "-o", pyxfile + ".c", pyxfile + ".pyx", "-Iyarl")
