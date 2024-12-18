# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrian(PythonPackage):
    """A clock-driven simulator for spiking neural networks"""

    homepage = "https://www.briansimulator.org"
    pypi = "brian/brian-1.4.3.tar.gz"

    version("1.4.3", sha256="c881dcfcd1a21990f9cb3cca76cdd868111cfd9e227ef5c1b13bb372d2efeaa4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@0.90.1:", type=("build", "run"))
    depends_on("py-numpy@1.4.1:", type=("build", "run"))
    depends_on("py-scipy@0.7.0:", type=("build", "run"))
