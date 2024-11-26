# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybv(PythonPackage):
    """A lightweight I/O utility for the BrainVision data format."""

    homepage = "https://github.com/bids-standard/pybv"
    pypi = "pybv/pybv-0.7.5.tar.gz"
    git = "https://github.com/bids-standard/pybv"

    license("BSD-3-Clause")

    version("0.7.5", sha256="57bb09305c1255b11dd5c6a75d0e6b3c81675cf0469d6a757b148ac332ac05d5")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type="build")

    depends_on("py-numpy@1.18.1:", type=("build", "run"))
