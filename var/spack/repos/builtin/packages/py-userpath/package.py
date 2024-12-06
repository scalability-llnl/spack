# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUserpath(PythonPackage):
    """Cross-platform tool for adding locations to the user PATH."""

    homepage = "https://github.com/ofek/userpath"
    pypi = "userpath/userpath-1.8.0.tar.gz"

    license("MIT")
    version("1.9.0", sha256="85e3274543174477c62d5701ed43a3ef1051824a9dd776968adc411e58640dd1")
    version("1.8.0", sha256="04233d2fcfe5cff911c1e4fb7189755640e1524ff87a4b82ab9d6b875fee5787")
    version("1.7.0", sha256="dcd66c5fa9b1a3c12362f309bbb5bc7992bac8af86d17b4e6b1a4b166a11c43f")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-hatchling", type="build")

    depends_on("py-click", type=("build", "run"))
