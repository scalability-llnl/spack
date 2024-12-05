# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLaw(PythonPackage):
    """Build large-scale task workflows using luigi,
    remote job submission, remote targets, and environment"""

    homepage = "https://github.com/riga/law"
    pypi = "law/law-0.1.6.tar.gz"

    license("BSD-3-Clause")

    version("0.1.7", sha256="1907989263087baaae652f00b8f196ed31df57cf749d2583d90c6e6af18fb2c3")
    version("0.1.6", sha256="17c2c1837080590bff4d2e7228bfb418733f11b60e2bac8f589e68da78cf2ab8")

    depends_on("python@2.7:2,3.3:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.13:", type=("build", "run"))
    depends_on("py-luigi@2.8.2:", type=("build", "run"))
