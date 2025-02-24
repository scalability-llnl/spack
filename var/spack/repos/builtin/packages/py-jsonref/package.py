# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonref(PythonPackage):
    """An implementation of JSON Reference for Python"""

    homepage = "https://github.com/gazpachoking/jsonref"
    pypi = "jsonref/jsonref-0.2.tar.gz"

    license("MIT")

    version("0.2", sha256="f3c45b121cf6257eafabdc3a8008763aed1cd7da06dbabc59a9e4d2a5e4e6697")

    depends_on("py-setuptools", type="build")
