# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyThrottler(PythonPackage):
    """Zero dependency Python package for easy throttling with asyncio support."""

    homepage = "https://github.com/uburuntu/throttler"
    pypi = "throttler/throttler-1.2.1.tar.gz"

    maintainers("charmoniumQ")

    license("MIT")

    version("1.2.2", sha256="d54db406d98e1b54d18a9ba2b31ab9f093ac64a0a59d730c1cf7bb1cdfc94a58")

    depends_on("py-setuptools", type="build")
