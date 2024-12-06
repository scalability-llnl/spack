# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestscenarios(PythonPackage):
    """Testscenarios, a pyunit extension for dependency injection"""

    homepage = "https://launchpad.net/testscenarios"
    pypi = "testscenarios/testscenarios-0.5.0.tar.gz"

    license("Apache-2.0")

    version("0.5.0", sha256="c257cb6b90ea7e6f8fef3158121d430543412c9a87df30b5dde6ec8b9b57a2b6")

    depends_on("py-setuptools", type="build")
