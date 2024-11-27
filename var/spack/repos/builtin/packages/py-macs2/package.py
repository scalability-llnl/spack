# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack.package import *


class PyMacs2(PythonPackage):
    """MACS2 Model-based Analysis of ChIP-Seq"""

    homepage = "https://github.com/taoliu/MACS"
    pypi = "MACS2/MACS2-2.2.4.tar.gz"

    license("BSD-3-Clause")

    version("2.2.8", sha256="2a0a436ac89d8f8c94a1e410690037760e5e37929ad719c54696e74ef84a98e0")
    version("2.2.7.1", sha256="ad2ca69bdd02a8942a68aae23133289b5c16ba382bcbe20c39fabf3948929de5")
    version("2.2.4", sha256="b131aadc8f5fd94bec35308b821e1f7585def788d2e7c756fc8cac402ffee25b")

    depends_on("c", type="build")  # generated

    # patch to correctly identify python-3.10 as greater than required version
    patch(
        "https://github.com/macs3-project/MACS/pull/497.patch?full_index=1",
        sha256="eaff891b9b3c6a910bd5d454dcc6e21288c8d1ad4d6d6f77e370bc8f90921cbd",
        when="@2.2.7.1^python@3.10:",
    )

    depends_on("python@3.6:", when="@2.2.7.1:", type=("build", "run"))
    # version 2.2.4 does not build with python-3.10
    depends_on("python@3.5:3.9", when="@2.2.4", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@41.2:", when="@2.2.4:", type="build")
    depends_on("py-numpy@1.17:", when="@2.2.4:", type=("build", "run"))
    depends_on("py-cython@0.29.24:", when="@2.2.8:", type="build")
    depends_on("py-cython@0.29:", when="@2.2.4:2.2.7.1", type="build")

    def patch(self):
        # regenerate C files from pyx files with cython
        files = glob.glob("MACS2/**/[!c]*.c", recursive=True)
        force_remove(*files)
