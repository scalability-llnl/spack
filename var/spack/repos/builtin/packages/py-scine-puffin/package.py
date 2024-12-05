# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScinePuffin(PythonPackage):
    """Calculation handler for SCINE Chemoton"""

    homepage = "https://scine.ethz.ch/download/puffin"
    pypi = "scine_puffin/scine_puffin-1.1.0.tar.gz"
    git = "https://github.com/qcscine/puffin.git"

    version("master", branch="master")
    version("1.1.0", sha256="1a15232b1b472c36349e5534e4fdf9dd90bc554926cb42fba37eee8e60be8c44")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-python-daemon", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # Promoted from optional to explicit dependencies to avoid compiling them on puffin startup
    depends_on("scine-database+python", type=("build", "run"))
    depends_on("scine-molassembler+python", type=("build", "run"))
    depends_on("scine-readuct+python", type=("build", "run"))
    depends_on("scine-utilities+python", type=("build", "run"))
