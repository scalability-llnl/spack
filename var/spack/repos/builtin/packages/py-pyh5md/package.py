# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyh5md(PythonPackage):
    """Read and write H5MD files."""

    homepage = "https://github.com/pdebuyl/pyh5md"
    pypi = "pyh5md/pyh5md-1.0.0.tar.gz"

    version("1.0.0", sha256="424cb9737464db5f49996b3be2371e718bf2a27dec0440870bc89591817015d2")

    depends_on("py-setuptools", type="build")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
