# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYajl(PythonPackage):
    """Python bindings for the Yajl JSON encoder/decoder library."""

    homepage = "https://github.com/rtyler/py-yajl"
    pypi = "yajl/yajl-0.3.5.tar.gz"

    version("0.3.5", sha256="432321ea613692a4782a2368a300f57b59c64a3c8508c7465af3fdc045e7bcc2")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
