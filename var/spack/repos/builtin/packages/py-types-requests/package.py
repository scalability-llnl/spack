# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesRequests(PythonPackage):
    """Typing stubs for requests."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-requests/types-requests-2.28.10.tar.gz"

    version("2.31.0.2", sha256="6aa3f7faf0ea52d728bb18c0a0d1522d9bfd8c72d26ff6f61bfc3d06a411cf40")
    version("2.28.10", sha256="97d8f40aa1ffe1e58c3726c77d63c182daea9a72d9f1fa2cafdea756b2a19f2c")

    depends_on("py-setuptools", type="build")

    depends_on("py-types-urllib3", type=("build", "run"))
    depends_on("py-types-urllib3@:1.26", when="@:2.29", type=("build", "run"))
