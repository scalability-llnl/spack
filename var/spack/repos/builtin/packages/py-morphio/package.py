# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyMorphio(PythonPackage):
    """Python library for reading / writing morphology files"""

    homepage = "https://github.com/BlueBrain/MorphIO"
    git = "https://github.com/BlueBrain/MorphIO.git"
    pypi = "morphio/MorphIO-3.3.2.tar.gz"

    license("LGPL-3.0-or-later", when="@:3.3.6")
    license("Apache-2.0", when="@3.3.7:")

    maintainers("tristan0x")

    version("master", branch="master", submodules=True)

    version("3.3.7", sha256="7cb6676fcbaa2ac154742ca8aed3fcb03bb4643852e36e368858580133b61732")
    version("3.3.6", sha256="0f2e55470d92a3d89f2141ae905ee104fd16257b93dafb90682d90171de2f4e6")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@24.2:", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("ninja", type="build")
    depends_on("cmake@3.2:", type="build")
    depends_on("py-numpy@1.14.1:", type=("build", "run"))
    depends_on("py-h5py@3", when="platform=windows", type=("build", "run"))
    if sys.platform != "win32":
        depends_on("hdf5")
