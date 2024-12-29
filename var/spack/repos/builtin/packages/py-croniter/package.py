# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCroniter(PythonPackage):
    """croniter provides iteration for datetime object with cron like format."""

    homepage = "https://github.com/kiorky/croniter"
    pypi = "croniter/croniter-1.3.8.tar.gz"

    license("MIT")

    version("1.3.8", sha256="32a5ec04e97ec0837bcdf013767abd2e71cceeefd3c2e14c804098ce51ad6cd9")

    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil", type=("build", "run"))
