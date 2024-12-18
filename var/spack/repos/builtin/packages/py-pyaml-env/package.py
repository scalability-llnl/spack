# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyamlEnv(PythonPackage):
    """Provides yaml file parsing with environment variable resolution"""

    homepage = "https://github.com/mkaranasou/pyaml_env"
    pypi = "pyaml_env/pyaml_env-1.2.1.tar.gz"

    license("MIT", checked_by="A_N_Other")

    version("1.2.1", sha256="6d5dc98c8c82df743a132c196e79963050c9feb05b0a6f25f3ad77771d3d95b0")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@5:7", type=("build", "run"))
