# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpythonGenutils(PythonPackage):
    """Vestigial utilities from IPython"""

    pypi = "ipython_genutils/ipython_genutils-0.1.0.tar.gz"

    version("0.2.0", sha256="eb2e116e75ecef9d4d228fdc66af54269afa26ab4463042e33785b887c628ba8")
    version("0.1.0", sha256="3a0624a251a26463c9dfa0ffa635ec51c4265380980d9a50d65611c3c2bd82a6")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
