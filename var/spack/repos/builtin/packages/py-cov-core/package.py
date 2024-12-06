# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCovCore(PythonPackage):
    """plugin core for use by pytest-cov, nose-cov and nose2-cov"""

    homepage = "https://github.com/schlamar/cov-core"
    pypi = "cov-core/cov-core-1.15.0.tar.gz"

    license("MIT")

    version("1.15.0", sha256="4a14c67d520fda9d42b0da6134638578caae1d374b9bb462d8de00587dba764c")

    depends_on("py-setuptools", type="build")
    depends_on("py-coverage@3.6:", type=("build", "run"))
