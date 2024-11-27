# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBioblend(PythonPackage):
    """BioBlend is a Python library for interacting with the Galaxy API."""

    homepage = "https://bioblend.readthedocs.io"
    pypi = "bioblend/bioblend-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="3794288bbf891ae6edc1bcdd9618a3ae16b6ed4a04c946505f7e29f2f28898a5")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests@2.20.0:", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.5.1:0.8,0.9.1:", type=("build", "run"))
    depends_on("py-tuspy", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
