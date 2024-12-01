# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyArgon2Cffi(PythonPackage):
    """The secure Argon2 password hashing algorithm.."""

    homepage = "https://argon2-cffi.readthedocs.io/"
    pypi = "argon2-cffi/argon2-cffi-20.1.0.tar.gz"

    license("MIT")

    version("21.3.0", sha256="d384164d944190a7dd7ef22c6aa3ff197da12962bd04b17f64d4e93d934dba5b")
    version("21.1.0", sha256="f710b61103d1a1f692ca3ecbd1373e28aa5e545ac625ba067ff2feca1b2bb870")
    version("20.1.0", sha256="d8029b2d3e4b4cea770e9e5a0104dd8fa185c1724a0f01528ae4826a6d25f97d")

    depends_on("python@3.6:", when="@21.2:", type=("build", "run"))
    depends_on("python@3.5:", when="@21.1:", type=("build", "run"))
    depends_on("python@2.7:2,3.5:", type=("build", "run"))

    depends_on("py-flit-core@3.4:3", when="@21.2:", type="build")
    depends_on("py-setuptools", when="@:21.1", type="build")

    depends_on("py-argon2-cffi-bindings", when="@21.2:", type=("build", "run"))
    depends_on("py-typing-extensions", when="@21.2: ^python@:3.7", type=("build", "run"))
    depends_on("py-cffi@1.0.0:", when="@:21.1", type=("build", "run"))
    depends_on("py-six", when="@:20.1", type=("build", "run"))
