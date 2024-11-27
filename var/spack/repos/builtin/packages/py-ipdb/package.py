# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpdb(PythonPackage):
    """ipdb is the iPython debugger and has many additional features, including
    a better interactive debugging experience via colorized output."""

    pypi = "ipdb/ipdb-0.13.11.tar.gz"

    license("BSD-3-Clause")

    version("0.13.11", sha256="c23b6736f01fd4586cc2ecbebdf79a5eb454796853e1cd8f2ed3b7b91d4a3e93")
    version("0.13.10", sha256="6950715f491d59df6c27b49cb372f22c2f1763478a5e9ed03fb0507e2d85f460")
    version("0.13.9", sha256="951bd9a64731c444fd907a5ce268543020086a697f6be08f7cc2c9a752a278c5")
    version("0.13.8", sha256="8d368fa048a93ad6c1985d7f1d78d68580c879e4053fc15714bdcf2a1b042d06")
    version("0.13.7", sha256="178c367a61c1039e44e17c56fcc4a6e7dc11b33561261382d419b6ddb4401810")

    # Dependencies gathered from:
    #     https://github.com/gotcha/ipdb/blob/master/setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-ipython@7.17:", type=("build", "run"))
    depends_on("py-toml@0.10.2:", when="@:0.13.9", type=("build", "run"))

    depends_on("py-ipython@7.31.1:", when="@0.13.10:", type=("build", "run"))
    depends_on("py-tomli", when="@0.13.10: ^python@:3.10", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"))
