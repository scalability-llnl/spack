# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNptyping(PythonPackage):
    """Type hints for numpy"""

    homepage = "https://github.com/ramonhagenaars/nptyping"
    url = "https://github.com/ramonhagenaars/nptyping/archive/v2.4.1.tar.gz"
    # avoid pypi for now: https://github.com/ramonhagenaars/nptyping/issues/98

    license("MIT")

    version("2.4.1", sha256="1c1b2b08220d271f3e52dbf2bd9190e4dd15b3c04abfcf7a04ec533d3cc9fdab")
    version("1.4.1", sha256="bbcedb967f8be1302dffdd999eb531b99712c6914078294b4411758d5899b3b6")
    version("1.0.1", sha256="a00e672bfdaddc99aa6b25dd1ae89d7d58d2b76e8ad099bd69577bac2598589f")

    depends_on("py-setuptools", type="build")
    depends_on("py-typish@1.7.0:", type=("build", "run"))
    depends_on("py-numpy@1.21.5", when="^python@:3.7", type=("build", "run"))
    depends_on("py-numpy@1.20.0:1", when="^python@3.8:", type=("build", "run"))
    depends_on("py-typing-extensions@4.0.0:4", when="^python@:3.9", type=("build", "run"))
