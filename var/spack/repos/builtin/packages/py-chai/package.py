# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChai(PythonPackage):
    """Chai - Python Mocking Made Easy"""

    homepage = "https://github.com/agoragames/chai"
    pypi = "chai/chai-1.1.2.tar.gz"

    license("BSD-3-Clause")

    version("1.1.2", sha256="ff8d2b6855f660cd23cd5ec79bd10264d39f24f6235773331b48e7fcd637d6cc")

    depends_on("py-setuptools", type="build")
