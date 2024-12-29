# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorlog(PythonPackage):
    """A colored formatter for the python logging module"""

    homepage = "https://github.com/borntyping/python-colorlog"
    pypi = "colorlog/colorlog-4.0.2.tar.gz"

    version("6.8.2", sha256="3e3e079a41feb5a1b64f978b5ea4f46040a94f11f0e8bbb8261e3dbbeca64d44")
    version("4.0.2", sha256="3cf31b25cbc8f86ec01fef582ef3b840950dea414084ed19ab922c8b493f9b42")
    version("3.1.4", sha256="418db638c9577f37f0fae4914074f395847a728158a011be2a193ac491b9779d")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@38.6.0:", when="@6.8.0:", type="build")
