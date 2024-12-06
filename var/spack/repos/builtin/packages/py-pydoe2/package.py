# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydoe2(PythonPackage):
    """pyDOE2 is a fork of the pyDOE package that is designed to help the
    scientist, engineer, statistician, etc., to construct appropriate
    experimental designs."""

    homepage = "https://github.com/clicumu/pyDOE2"
    pypi = "pyDOE2/pyDOE2-1.3.0.tar.gz"

    license("BSD-3-Clause")

    version("1.3.0", sha256="5492b0f984af52da3af20b1cd61deb21b067c858e65243ec3ba573375f0d6720")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
