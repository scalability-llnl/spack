# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScineChemoton(PythonPackage):
    """Software driving the automated exploration of chemical reaction networks"""

    homepage = "https://scine.ethz.ch/download/chemoton"
    pypi = "scine_chemoton/scine_chemoton-2.2.0.tar.gz"
    git = "https://github.com/qcscine/puffin.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2.2.0", sha256="cda4f9de1e1c00ecc5e0b2d9c17a5edb56b468d454022e3f4045ec116ba2ec45")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("scine-database+python", type=("build", "run"))
    depends_on("scine-molassembler+python", type=("build", "run"))
    depends_on("scine-utilities+python", type=("build", "run"))
