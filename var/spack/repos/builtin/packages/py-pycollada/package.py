# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycollada(PythonPackage):
    """Python library for reading and writing collada documents"""

    homepage = "https://pypi.org/project/pycollada/"
    pypi = "pycollada/pycollada-0.7.2.tar.gz"
    git = "https://github.com/pycollada/pycollada"

    version("0.7.2", sha256="70a2630ed499bdab718c0e61a3e6ae3698130d7e4654e89cdecde51bfdaea56f")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-python-dateutil@2.2:", type=("build", "run"))
