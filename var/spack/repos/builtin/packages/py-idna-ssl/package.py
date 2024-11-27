# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIdnaSsl(PythonPackage):
    """Patch ssl.match_hostname for Unicode(idna) domains support"""

    homepage = "https://github.com/aio-libs/idna-ssl"
    url = "https://github.com/aio-libs/idna-ssl/archive/v1.1.0.tar.gz"

    license("MIT")

    version("1.1.0", sha256="cdbefa2429a6a2fa5cbe8d2a47c677ca671e84531618d3460fc0bcfc840684c5")

    depends_on("py-setuptools", type="build")
    depends_on("py-idna@2.0:", type=("build", "run"))
