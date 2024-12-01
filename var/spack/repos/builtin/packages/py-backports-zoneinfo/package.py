# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsZoneinfo(PythonPackage):
    """Backport of the standard library zoneinfo module"""

    homepage = "https://github.com/pganssle/zoneinfo"
    pypi = "backports.zoneinfo/backports.zoneinfo-0.2.1.tar.gz"

    license("Apache-2.0")

    version("0.2.1", sha256="fadbfe37f74051d024037f223b8e001611eac868b5c5b06144ef4d8b799862f2")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@40.8.0:", type="build")
