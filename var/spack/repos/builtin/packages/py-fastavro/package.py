# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastavro(PythonPackage):
    """Fastavro for Python."""

    homepage = "https://github.com/fastavro/fastavro"
    url = "https://github.com/fastavro/fastavro/archive/1.0.0.post1.tar.gz"

    license("MIT")

    version(
        "1.0.0.post1", sha256="74f9bf0f9bc9e484c6d42fad603d6e6f907e716a78189873761dc86ce64cc6c5"
    )
    version("1.0.0", sha256="9aca6f425dd898f40e2c4e10714276604e610c6ad3df53109d6fb3ad49761b5e")
    version("0.24.2", sha256="6ccd711a0c6960c3263a7c1c0e0e3bf7c5e949e11c3a676edece36138c62caba")
    version("0.24.1", sha256="8b109b4f564f6fe7fd82d3e2d582fba8da58167bcf2fa65e27fd3c4e49afddf9")
    version("0.24.0", sha256="d60c2a90d7bbe7a70aab30d3b772faedcbd9487bc1f7e2cd65a93a555688965e")
    version("0.23.6", sha256="b511dc55a9514205765f96b4d964f1d74fca9696dbac91229cef6100a028a29f")
    version("0.23.5", sha256="5542b69a99a74a57988c2a48da9be4356db4223cebac599ec3e9bf1b74ef534b")
    version("0.23.4", sha256="e699940a06fc713d56ba8b9cb88665e2fa2a6abc2c342cd540ee7cd4428af973")
    version("0.23.3", sha256="4e4bebe7b43b5cdad030bdbeb7f7f0ccb537ea025a9e28c7a4826876872fc84b")
    version("0.23.2", sha256="3b31707d6eaa1e98fc60536d0b3483bafb78be39bf9f0a1affe1b353e70bd5b2")

    def setup_build_environment(self, env):
        # Use cython for building as *.c files are missing from repo
        env.set("FASTAVRO_USE_CYTHON", 1)

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-snappy", type=("build", "run"))
    depends_on("py-lz4", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
