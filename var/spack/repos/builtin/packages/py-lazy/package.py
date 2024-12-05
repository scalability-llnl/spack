# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLazy(PythonPackage):
    """Lazy attributes for Python objects"""

    pypi = "lazy/lazy-1.2.zip"

    license("BSD-2-Clause")

    version("1.5", sha256="cb3d8612aa895a48afe8f08860573ba8ef5ee4fdbe1b3cd606c5f50a16152186")
    version("1.4", sha256="2c6d27a5ab130fb85435320651a47403adcb37ecbcc501b0c6606391f65f5b43")
    version("1.2", sha256="127ea610418057b953f0d102bed83f2c367be13b59f8d0ddf3b8a86c7d31b970")

    depends_on("py-setuptools", type="build")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/l/lazy/"

        if version < Version("1.5"):
            url += "lazy-{0}.zip"
        else:
            url += "lazy-{0}.tar.gz"

        url = url.format(version)
        return url
