# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKaldiio(PythonPackage):
    """A pure python module for reading and writing kaldi ark files"""

    homepage = "https://github.com/nttcslab-sp/kaldiio"
    pypi = "kaldiio/kaldiio-2.17.2.tar.gz"

    version("2.17.2", sha256="51bc2d805ed5b15403501d410adcb2e79fe2bd7f5ef63c20b4ddb345c6a8de01")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pytest-runner", type="build")
