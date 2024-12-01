# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestRemotedata(PythonPackage):
    """Pytest plugin for controlling remote data access."""

    homepage = "https://github.com/astropy/pytest-remotedata"
    pypi = "pytest-remotedata/pytest-remotedata-0.4.0.tar.gz"

    license("BSD-3-Clause")

    version("0.4.0", sha256="be21c558e34d7c11b0f6aeb50956c09520bffcd02b7fce9c6f8e8531a401a1c8")

    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-pytest@4.6:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
