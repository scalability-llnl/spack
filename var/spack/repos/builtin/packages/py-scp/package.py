# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScp(PythonPackage):
    """scp module for paramiko"""

    homepage = "https://github.com/jbardin/scp.py"
    pypi = "scp/scp-0.13.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.13.2", sha256="ef9d6e67c0331485d3db146bf9ee9baff8a48f3eb0e6c08276a8584b13bf34b3")

    depends_on("py-setuptools", type="build")
    depends_on("py-paramiko", type=("build", "run"))
    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
