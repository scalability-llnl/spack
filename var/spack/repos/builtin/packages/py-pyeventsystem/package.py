# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyeventsystem(PythonPackage):
    """An event driven middleware library for Python."""

    homepage = "https://github.com/cloudve/pyeventsystem"
    pypi = "pyeventsystem/pyeventsystem-0.1.0.tar.gz"

    license("MIT")

    version("0.1.0", sha256="4a3d199759a040d2cd17f8b4293cc1c3f3c2ae50ae531fb5f9f955a895fca8b9")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
