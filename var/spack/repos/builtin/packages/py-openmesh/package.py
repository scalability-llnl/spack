# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenmesh(PythonPackage):
    """A versatile halfedge-based data structure for representing and
    manipulating polygon meshes"""

    homepage = "https://www.graphics.rwth-aachen.de:9000/OpenMesh/openmesh-python"
    pypi = "openmesh/openmesh-1.1.3.tar.gz"

    license("BSD-3-Clause")

    version("1.2.1", sha256="6fd3fa41a68148e4a7523f562426aa9758bf65ccc6642abcf79c37bae9c6af3c")
    version("1.1.3", sha256="c1d24abc85b7b518fe619639f89750bf19ed3b8938fed4dd739a72f1e6f8b0f6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("cmake@3.1:", when="@1.1.3 platform=windows", type="build")
    depends_on("cmake@3.3.0:", when="@1.2.2 platform=windows", type="build")
    depends_on("cmake", type="build")

    depends_on("py-numpy", type=("build", "run"))
