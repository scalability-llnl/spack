# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynrrd(PythonPackage):
    """Python library for reading and writing NRRD files into and from numpy arrays"""

    homepage = "https://github.com/mhe/pynrrd"
    pypi = "pynrrd/pynrrd-0.4.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="4eb4caba03fbca1b832114515e748336cb67bce70c7f3ae36bfa2e135fc990d2")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.11.1:", type=("build", "run"))
    depends_on("py-nptyping", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
