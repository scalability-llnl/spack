# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyheadtail(PythonPackage):
    """CERN PyHEADTAIL numerical n-body simulation code for simulating
    macro-particle beam dynamics with collective effects."""

    homepage = "https://github.com/PyCOMPLETE/PyHEADTAIL"
    pypi = "PyHEADTAIL/PyHEADTAIL-1.14.1.tar.gz"

    version("1.16.1", sha256="bbe69eeb2f57fffee455a35dc14cca95a9c650ba334982fa9ba62a1ebd5b5606")
    version("1.14.1", sha256="bf90ac7e8764176c55e82c363cad7ab43543863b6ef482760ced23b78e917bb4")
    version("1.13.1", sha256="29c742573a918126b5a9c21806ee0ec6a34ec642a0e6ad200f6d4551bf1bb310")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("python", type=("build", "run"))
    depends_on("python@3:", when="@1.13.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    # cython@3: support was added in 1.16.1
    depends_on("py-cython@:2", when="@:1.16.0", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
