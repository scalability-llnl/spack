# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPpft(PythonPackage):
    """Distributed and parallel python"""

    homepage = "https://github.com/uqfoundation/ppft"
    pypi = "ppft/ppft-1.6.4.9.tar.gz"

    license("BSD-3-Clause")

    version("1.6.6.4", sha256="473442cc6731856990bd25bd6b454bb98720007de4523a73c560bdd0060463d2")
    version("1.6.4.9", sha256="5537b00afb7b247da0f59cc57ee5680178be61c8b2e21b5a0672b70a3d247791")
    version("1.6.4.7.1", sha256="f94b26491b4a36adc975fc51dba7568089a24756007a3a4ef3414a98d7337651")
    version("1.6.4.6", sha256="92d09061f5425634c43dbf99c5558f2cf2a2e1e351929f8da7e85f4649c11095")
    version("1.6.4.5", sha256="d47da9d2e553848b75727ce7c510f9e149965d5c68f9fc56c774a7c6a3d18214")

    depends_on("python@2.5:2.8,3.1:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:", when="@1.6.6.4:", type=("build", "run"))

    depends_on("py-setuptools@0.6:", type="build")
    depends_on("py-six@1.7.3:", type=("build", "run"))
    depends_on("py-dill@0.2.6:", type=("build", "run"))
    depends_on("py-dill@0.3.4:", type=("build", "run"), when="@1.6.6.4:")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/p/ppft/"
        if Version("1.6.6.4") > version >= Version("1.6.4.8"):
            url += "ppft-{0}.tar.gz"
        else:
            url += "ppft-{0}.zip"

        url = url.format(version)
        return url
