# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgon2CffiBindings(PythonPackage):
    """Low-level CFFI bindings for Argon2."""

    homepage = "https://github.com/hynek/argon2-cffi-bindings"
    pypi = "argon2-cffi-bindings/argon2-cffi-bindings-21.2.0.tar.gz"

    license("MIT")

    version("21.2.0", sha256="bb89ceffa6c791807d1305ceb77dbfacc5aa499891d2c55661c6459651fc39e3")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")
    depends_on("py-cffi@1.0.1:", type=("build", "run"))
