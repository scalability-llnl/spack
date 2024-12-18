# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPbr(PythonPackage):
    """PBR is a library that injects some useful and sensible default
    behaviors into your setuptools run."""

    pypi = "pbr/pbr-5.4.3.tar.gz"

    # Skip 'pbr.tests' imports
    import_modules = ["pbr", "pbr.cmd", "pbr.hooks"]

    version("5.10.0", sha256="cfcc4ff8e698256fc17ea3ff796478b050852585aa5bae79ecd05b2ab7b39b9a")
    version("5.7.0", sha256="4651ca1445e80f2781827305de3d76b3ce53195f2227762684eb08f17bc473b7")
    version("5.4.3", sha256="2c8e420cd4ed4cec4e7999ee47409e876af575d4c35a45840d59e8b5f3155ab8")
    version("5.2.1", sha256="93d2dc6ee0c9af4dbc70bc1251d0e545a9910ca8863774761f92716dece400b6")
    version("3.1.1", sha256="05f61c71aaefc02d8e37c0a3eeb9815ff526ea28b3b76324769e6158d7f95be1")
    version("2.0.0", sha256="0ccd2db529afd070df815b1521f01401d43de03941170f8a800e7531faba265d")
    version("1.10.0", sha256="186428c270309e6fdfe2d5ab0949ab21ae5f7dea831eab96701b86bd666af39c")
    version("1.8.1", sha256="e2127626a91e6c885db89668976db31020f0af2da728924b56480fc7ccf09649")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
