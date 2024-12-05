# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonpatch(PythonPackage):
    """Library to apply JSON Patches according to RFC 6902"""

    homepage = "https://github.com/stefankoegl/python-json-patch"
    pypi = "jsonpatch/jsonpatch-1.23.tar.gz"

    license("BSD-3-Clause")

    version("1.23", sha256="49f29cab70e9068db3b1dc6b656cbe2ee4edf7dfe9bf5a0055f17a4b6804a4b9")

    depends_on("py-setuptools", type="build")
    depends_on("py-jsonpointer@1.9", type=("build", "run"))
