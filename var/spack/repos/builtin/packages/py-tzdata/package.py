# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTzdata(PythonPackage):
    """Provider of IANA time zone data."""

    homepage = "https://github.com/python/tzdata"
    pypi = "tzdata/tzdata-2023.3.tar.gz"

    license("Apache-2.0")

    version("2023.3", sha256="11ef1e08e54acb0d4f95bdb1be05da659673de4acbd21bf9c69e94cc5e907a3a")

    depends_on("py-setuptools@40.8:", type="build")
