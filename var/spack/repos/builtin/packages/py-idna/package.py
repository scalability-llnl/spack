# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIdna(PythonPackage):
    """Internationalized Domain Names for Python (IDNA 2008 and UTS #46)"""

    homepage = "https://github.com/kjd/idna"
    pypi = "idna/idna-3.2.tar.gz"

    license("BSD-3-Clause")

    version("3.4", sha256="814f528e8dead7d329833b91c5faa87d60bf71824cd12a7530b5526063d02cb4")
    version("3.3", sha256="9d643ff0a55b762d5cdb124b8eaa99c66322e2157b69160bc32796e824360e6d")
    version("3.2", sha256="467fbad99067910785144ce333826c71fb0e63a425657295239737f7ecd125f3")
    version("2.9", sha256="7588d1c14ae4c77d74036e8c22ff447b26d0fde8f007354fd48a7814db15b7cb")
    version("2.8", sha256="c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407")
    version("2.5", sha256="3cb5ce08046c4e3a560fc02f138d0ac63e00f8ce5901a56b32ec8b7994082aab")

    depends_on("python@3.5:", when="@3.2:", type=("build", "run"))
    depends_on("python@3.4:", when="@3:", type=("build", "run"))
    depends_on("python@2.7:2,3.4:", when="@2.8:2", type=("build", "run"))
    depends_on("python@2.6:", when="@:2.7", type=("build", "run"))
    depends_on("py-flit-core@3.2:3", when="@3.4:", type="build")
    depends_on("py-setuptools", when="@:3.3", type=("build", "link"))
