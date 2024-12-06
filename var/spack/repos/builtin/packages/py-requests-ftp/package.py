# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsFtp(PythonPackage):
    """FTP Transport Adapter for Requests.."""

    homepage = "https://github.com/Lukasa/requests-ftp"
    pypi = "requests-ftp/requests-ftp-0.3.1.tar.gz"

    license("Apache-2.0")

    version("0.3.1", sha256="7504ceb5cba8a5c0135ed738596820a78c5f2be92d79b29f96ba99b183d8057a")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests", type=("build", "run"))
