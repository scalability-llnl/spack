# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXattr(PythonPackage):
    """A python interface to access extended file attributes,
    sans libattr dependency.
    """

    homepage = "https://pyxattr.k1024.org/"
    pypi = "xattr/xattr-0.9.6.tar.gz"
    git = "https://github.com/xattr/xattr"

    license("MIT")

    version("master", branch="master")
    version("0.10.1", sha256="c12e7d81ffaa0605b3ac8c22c2994a8e18a9cf1c59287a1b7722a2289c952ec5")
    version("0.9.9", sha256="09cb7e1efb3aa1b4991d6be4eb25b73dc518b4fe894f0915f5b0dcede972f346")
    version("0.9.8", sha256="bf11c8c857215e3ef60b031e7807264f30af4348d7565a7e9b8dca70593753c7")
    version("0.9.7", sha256="b0bbca828e04ef2d484a6522ae7b3a7ccad5e43fa1c6f54d78e24bb870f49d44")
    version("0.9.6", sha256="7cb1b28eeab4fe99cc4350e831434142fce658f7d03f173ff7722144e6a47458")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.0.0:", type=("build", "run"))
