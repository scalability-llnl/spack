# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRetrying(PythonPackage):
    """Retrying is an Apache 2.0 licensed general-purpose retrying library,
    written in Python, to simplify the task of adding retry behavior to just
    about anything."""

    homepage = "https://github.com/rholder/retrying"
    pypi = "retrying/retrying-1.3.3.tar.gz"

    license("Apache-2.0")

    version("1.3.3", sha256="08c039560a6da2fe4f2c426d0766e284d3b736e355f8dd24b37367b0bb41973b")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.7.0:", type=("build", "run"))
