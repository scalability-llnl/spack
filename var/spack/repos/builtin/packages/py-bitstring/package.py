# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBitstring(PythonPackage):
    """Simple construction, analysis and modification of binary data."""

    homepage = "http://pythonhosted.org/bitstring"
    pypi = "bitstring/bitstring-3.1.6.tar.gz"

    license("MIT")

    version("4.0.2", sha256="a391db8828ac4485dd5ce72c80b27ebac3e7b989631359959e310cd9729723b2")
    version("3.1.5", sha256="c163a86fcef377c314690051885d86b47419e3e1770990c212e16723c1c08faa")

    depends_on("py-setuptools", when="@:4.0.1", type="build")
    depends_on("py-setuptools@61:", when="@4.0.2:", type="build")
    depends_on("py-bitarray@2.7.4", when="@4.1:")

    def url_for_version(self, version):
        url = "https://pypi.org/packages/source/s/bitstring/bitstring-{}.{}"
        if version < Version("3.1.6"):
            suffix = "zip"
        else:
            suffix = "tar.gz"
        return url.format(version, suffix)
