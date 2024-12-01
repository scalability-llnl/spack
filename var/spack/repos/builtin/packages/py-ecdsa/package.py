# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEcdsa(PythonPackage):
    """ECDSA cryptographic signature library (pure python)"""

    homepage = "https://github.com/warner/python-ecdsa"
    pypi = "ecdsa/ecdsa-0.15.tar.gz"

    license("MIT")

    version("0.15", sha256="8f12ac317f8a1318efa75757ef0a651abe12e51fc1af8838fb91079445227277")
    version("0.13.2", sha256="5c034ffa23413ac923541ceb3ac14ec15a0d2530690413bff58c12b80e56d884")

    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.9.0:", type=("build", "run"))
