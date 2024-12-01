# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsynctest(PythonPackage):
    """The package asynctest is built on top of the standard unittest module
    and cuts down boilerplate code when testing libraries for asyncio."""

    homepage = "https://asynctest.readthedocs.io"
    pypi = "asynctest/asynctest-0.13.0.tar.gz"

    license("Apache-2.0")

    version("0.13.0", sha256="c27862842d15d83e6a34eb0b2866c323880eb3a75e4485b079ea11748fd77fac")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@30.3:", type="build")
