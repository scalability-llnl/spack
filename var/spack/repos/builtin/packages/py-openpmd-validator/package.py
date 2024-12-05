# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpmdValidator(PythonPackage):
    """Validator and Example Scripts for the openPMD markup.

    openPMD is an open standard for particle-mesh data files."""

    homepage = "https://www.openPMD.org"
    git = "https://github.com/openPMD/openPMD-validator.git"
    pypi = "openPMD-validator/openPMD-validator-1.1.0.3.tar.gz"

    maintainers("ax3l")

    license("ISC")

    version("1.1.0.3", sha256="b2e57123c1dc09cdc121011d007e30fab82b3d21732d02e4f1ba919b24345810")
    version("1.1.0.2", sha256="6ac6e2860351d9940821ca6f3b44ab63629e0bd06f6984225c55830c3e58b83c")
    version("1.1.0.1", sha256="7585abbd32523ae6b8065772e1cc27a45e232c526a9fc0bd8ce85182d1b4b325")
    version("1.0.0.2", sha256="9610b552aef48baf37e1ce3fe1372b5a2a2f358ff50e23283e79fdfb6fee5366")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.6.1:", type=("build", "run"))
    depends_on("py-python-dateutil@2.3.0:", type=("build", "run"))
    depends_on("py-h5py@2.0.0:", type=("build", "run"))
