# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDateutils(PythonPackage):
    """Various utilities for working with date and datetime objects."""

    homepage = "https://github.com/jmcantrell/python-dateutils"
    pypi = "dateutils/dateutils-0.6.12.tar.gz"

    license("0BSD")

    version("0.6.12", sha256="03dd90bcb21541bd4eb4b013637e4f1b5f944881c46cc6e4b67a6059e370e3f1")

    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
