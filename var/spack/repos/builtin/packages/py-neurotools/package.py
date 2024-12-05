# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurotools(PythonPackage):
    """A collection of tools for representing and anlyzing neuroscientific
    data."""

    homepage = "http://neuralensemble.org/NeuroTools"
    pypi = "neurotools/NeuroTools-0.3.1.tar.gz"

    license("GPL-2.0-or-later")

    version("0.3.1", sha256="a459420fc0e9ff6b59af28716ddb0c75d11a63b8db80a5f4844e0d7a90c2c653")

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-tables", type=("build", "run"))
    depends_on("py-pyaml", type=("build", "run"))

    patch("neurotools-0.3.1.patch", when="@0.3.1")
