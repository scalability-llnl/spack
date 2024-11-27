# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDlcpar(PythonPackage):
    """DLCpar is a reconciliation method for inferring gene duplications,
    losses, and coalescence (accounting for incomplete lineage sorting)."""

    homepage = "https://www.cs.hmc.edu/~yjw/software/dlcpar/"
    url = "https://www.cs.hmc.edu/~yjw/software/dlcpar/pub/sw/dlcpar-1.0.tar.gz"

    version("1.0", sha256="774319caba0f10d1230b8f85b8a147eda5871f9a316d7b3381b91c1bde97aa0a")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
