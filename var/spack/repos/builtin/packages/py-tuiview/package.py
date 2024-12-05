# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTuiview(PythonPackage):
    """TuiView is a lightweight raster GIS with powerful raster attribute
    table manipulation abilities.
    """

    homepage = "https://github.com/ubarsc/tuiview"
    url = (
        "https://github.com/ubarsc/tuiview/releases/download/tuiview-1.2.13/TuiView-1.2.13.tar.gz"
    )

    maintainers("neilflood", "gillins")

    version("1.2.14", sha256="80cf4ac607b37bb9d7348b3d40e1e18910323f7ad47e79ae850cbb4750775f7c")
    version("1.2.13", sha256="48c8d4175c324f70941dc49c5a119882c9d501bd20bc13c76bc2455dee5236a5")
    version("1.2.12", sha256="3f0c1673f2f861db01726f3d7f6f1dde4a42ec57894a79b89457c398768dd25f")
    version("1.2.11", sha256="81f870ad98ec1e3175f25028d261135b6198fa85038bfaa900789e04e3cf8517")
    version("1.2.10", sha256="5ea777a4e89780488b03b346f00b586b46a0bd4c8a994e6def46a6494fa486ef")
    version("1.2.9", sha256="b5d11e9501cf61cf62f1223416dfe408cf604ae48c06d697589dfc0a606ad6a9")
    version("1.2.8", sha256="e75950908a2d1f7c7216dfeead82483e1d3b0267fff9561549d85ca00725456b")
    version("1.2.7", sha256="35dfeb79b2bb57dfb5b8c90c3edf8c8a0a3f89cef85c33f9935e4a4add282aaf")
    version("1.2.6", sha256="61b136fa31c949d7a7a4dbf8562e6fc677d5b1845b152ec39e337f4eb2e91662")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-pyqt5", type=("build", "run"))
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("gdal+geos+python", type=("build", "run"))
