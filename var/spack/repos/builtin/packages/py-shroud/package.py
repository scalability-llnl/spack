# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShroud(PythonPackage):
    """Create Fortran wrappers for a C++ library."""

    homepage = "https://github.com/LLNL/shroud"
    git = "https://github.com/LLNL/shroud.git"
    tags = ["radiuss"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("0.12.2", tag="v0.12.2", commit="939ba0a3e8b5a885da3ddaebb92bf93cb12b0401")
    version("0.12.1", tag="v0.12.1", commit="c09344655371885a42783f8c0ac8a31f2bbffc9f")
    version("0.11.0", tag="v0.11.0", commit="503b852796d549199c5ab94b14e59ebd62988870")
    version("0.10.1", tag="v0.10.1", commit="13a3c70bc5190e0e8531e17925928fbd7154acb5")
    version("0.9.0", tag="v0.9.0", commit="94aa2831290d10b604df16cb87ee17aa722fb998")
    version("0.8.0", tag="v0.8.0", commit="b58ac35f41514428d08849a578c45ad444bfddc9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-pyyaml@4.2:", type=("build", "run"))
