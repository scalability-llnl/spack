# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymumps(PythonPackage):
    """Python bindings for MUMPS, a parallel sparse direct solver"""

    homepage = "https://github.com/pymumps/pymumps"
    pypi = "PyMUMPS/PyMUMPS-0.3.2.tar.gz"
    git = "https://github.com/PyMumps/pymumps.git"

    # Add a list of GitHub accounts to notify when the
    # package is updated
    maintainers("payerle")

    license("BSD-3-Clause")

    version("0.3.2", sha256="f290ec4850098f108fb91cb9e7fa07302ebf5076e4329f8e6ea4924de8ba35df")

    depends_on("py-cython", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("mumps", type="link")
    depends_on("py-mpi4py", type=("build", "run"))

    # Patch to add libmumps_common.so to library dependencies
    # See https://github.com/PyMumps/pymumps/issues/13
    patch("py-pymumps.setup.patch")
