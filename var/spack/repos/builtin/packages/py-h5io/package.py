# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5io(PythonPackage):
    """Python Objects Onto HDF5."""

    homepage = "http://h5io.github.io"
    pypi = "h5io/h5io-0.1.7.tar.gz"
    git = "https://github.com/h5io/h5io.git"

    license("BSD-3-Clause")

    version("0.1.7", sha256="be2684e678a28a5d59140de838f0165f095af865e48b8e498a279a3c2b89303e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
