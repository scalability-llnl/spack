# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyItolapi(PythonPackage):
    """API for interacting with itol.embl.de"""

    homepage = "https://github.com/albertyw/itolapi"
    pypi = "itolapi/itolapi-4.1.2.tar.gz"

    maintainers("snehring")

    license("MIT")

    version("4.1.2", sha256="37a866a117a80d3d72a6eb6b2cba30444751c644cc6bc4242f050750375a8397")

    depends_on("py-setuptools", type="build")

    depends_on("py-requests@2", type=("build", "run"))
