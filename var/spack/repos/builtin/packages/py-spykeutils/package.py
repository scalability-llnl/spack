# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpykeutils(PythonPackage):
    """Utilities for analyzing electrophysiological data"""

    homepage = "https://github.com/rproepp/spykeutils"
    pypi = "spykeutils/spykeutils-0.4.3.tar.gz"

    version("0.4.3", sha256="ff6206d9116d665024109c997377bfed37d953a4cac2859b79a610f395b6b37b")

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-quantities", type=("build", "run"))
    depends_on("py-neo@0.2.1:0.3", type=("build", "run"))
