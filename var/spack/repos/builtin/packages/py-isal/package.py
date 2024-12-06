# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIsal(PythonPackage):
    """Faster zlib and gzip compatible compression and decompression by
    providing Python bindings for the ISA-L library."""

    homepage = "https://github.com/pycompression/python-isal"
    pypi = "isal/isal-1.1.0.tar.gz"

    license("PSF-2.0")

    version("1.1.0", sha256="1364f4e3255a57d51c01422ab3ae785a43c076d516ebf49f6a25adecf8232105")
    version("1.0.0", sha256="a30369de6852109eef8ca1bdd46d7e4b5c4517846a25acfc707cbb19db66ac80")

    depends_on("c", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@51:", type="build")
    depends_on("libisal")

    def setup_build_environment(self, env):
        env.set("PYTHON_ISAL_LINK_DYNAMIC", "true")
