# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastremap(PythonPackage):
    """Renumber and relabel Numpy arrays at C++ speed and physically convert rectangular
    Numpy arrays between C and Fortran order using an in-place transposition"""

    homepage = "https://github.com/seung-lab/fastremap/"
    pypi = "fastremap/fastremap-1.14.1.tar.gz"

    license("LGPL-3.0", checked_by="A-N-Other")

    version("1.14.1", sha256="067d42d6cb3b1b0789889efd1d7fae58006c82ada4a8446d40e9e838b358ee7c")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:3", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
    depends_on("py-cython", type="build")

    depends_on("py-numpy", type=("build", "run"))
