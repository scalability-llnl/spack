# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyvolve(PythonPackage):
    """Pyvolve is an open-source Python module for simulating sequences
    along a phylogenetic tree according to continuous-time Markov models
    of sequence evolution"""

    homepage = "https://github.com/sjspielman/pyvolve"
    pypi = "Pyvolve/Pyvolve-1.1.0.tar.gz"

    version("1.1.0", sha256="850aae6213a95c3f8c438ef7cdab33f4dafe8ef305b6fa85bbea1a9e7484c787")
    version("1.0.3", sha256="725d5851f24b3b4564970a999bad8e2e90782cf81a07c3a3370c492a956d9d51")

    depends_on("py-setuptools", type="build")
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-numpy@1.20.0:", type=("build", "run"), when="@1.1.0:")
    depends_on("py-numpy@1.7:", type=("build", "run"), when="@1.0.3:")
    depends_on("py-scipy", type=("build", "run"))
