# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImagesize(PythonPackage):
    """Parses image file headers and returns image size. Supports PNG, JPEG,
    JPEG2000, and GIF image file formats."""

    homepage = "https://github.com/shibukawa/imagesize_py"
    pypi = "imagesize/imagesize-0.7.1.tar.gz"

    license("MIT")

    version("1.4.1", sha256="69150444affb9cb0d5cc5a92b3676f0b2fb7cd9ae39e947a5e11a36b4497cd4a")
    version("1.3.0", sha256="cd1750d452385ca327479d45b64d9c7729ecf0b3969a58148298c77092261f9d")
    version("1.1.0", sha256="f3832918bc3c66617f92e35f5d70729187676313caa60c187eb0f28b8fe5e3b5")
    version("0.7.1", sha256="0ab2c62b87987e3252f89d30b7cedbec12a01af9274af9ffa48108f2c13c6062")

    depends_on("python@2.7:2,3.4:", when="@1.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
