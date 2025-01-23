# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDacite(PythonPackage):
    """Simple creation of data classes from dictionaries."""

    homepage = "https://github.com/konradhalas/dacite"
    pypi = "dacite/dacite-1.8.0.tar.gz"

    license("MIT")

    version("1.8.0", sha256="6257a5e505b61a8cafee7ef3ad08cf32ee9b885718f42395d017e0a9b4c6af65")

    depends_on("python@3.6:")

    depends_on("py-setuptools", type="build")
