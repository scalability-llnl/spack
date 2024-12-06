# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectMetadata(PythonPackage):
    """PEP 621 metadata parsing."""

    homepage = "https://github.com/FFY00/python-pyproject-metadata"
    pypi = "pyproject-metadata/pyproject-metadata-0.6.1.tar.gz"

    license("MIT")

    version("0.7.1", sha256="0a94f18b108b9b21f3a26a3d541f056c34edcb17dc872a144a15618fed7aef67")
    version("0.6.1", sha256="b5fb09543a64a91165dfe85796759f9e415edc296beb4db33d1ecf7866a862bd")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging@19:", type=("build", "run"))
