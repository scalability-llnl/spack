# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyaestro(PythonPackage):
    """A collection of data classes, data structures, and other utility classes
    that are aimed for use in workflow"""

    homepage = "https://github.com/FrankD412/pyaestro"
    pypi = "pyaestro/pyaestro-0.0.1a2.tar.gz"
    git = "https://github.com/FrankD412/pyaestro"

    maintainers("FrankD412")

    license("MIT")

    # git branches
    version("main", branch="main")
    version("0.0.1a2", sha256="1f6a5068ff8dd9fe4838aba43850e51a5b622f379819ae62103617bf9c8aaa31")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
