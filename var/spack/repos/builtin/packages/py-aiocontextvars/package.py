# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiocontextvars(PythonPackage):
    """This library experimentally provides the missing asyncio support for
    the contextvars backport library."""

    homepage = "https://github.com/fantix/aiocontextvars"
    pypi = "aiocontextvars/aiocontextvars-0.2.2.tar.gz"

    license("BSD-3-Clause")

    version("0.2.2", sha256="f027372dc48641f683c559f247bd84962becaacdc9ba711d583c3871fb5652aa")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")
