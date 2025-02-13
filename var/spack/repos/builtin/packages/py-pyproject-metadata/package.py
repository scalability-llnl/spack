# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectMetadata(PythonPackage):
    """PEP 621 metadata parsing."""

    homepage = "https://github.com/FFY00/python-pyproject-metadata"
    pypi = "pyproject-metadata/pyproject_metadata-0.6.1.tar.gz"

    license("MIT")

    version("0.9.0", sha256="8511c00a4cad96686af6a6b4143433298beb96105a9379afdc9b0328f4f260c9")
    version("0.7.1", sha256="0a94f18b108b9b21f3a26a3d541f056c34edcb17dc872a144a15618fed7aef67")
    version("0.6.1", sha256="b5fb09543a64a91165dfe85796759f9e415edc296beb4db33d1ecf7866a862bd")

    depends_on("py-flit", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging@19:", type=("build", "run"))
