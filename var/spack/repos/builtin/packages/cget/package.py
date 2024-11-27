# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cget(PythonPackage):
    """Cmake package retrieval."""

    homepage = "https://github.com/pfultz2/cget"
    pypi = "cget/cget-0.1.9.tar.gz"

    license("BSL-1.0")

    version("0.2.0", sha256="835009ba6d623a36eee8056975d7cdbeebb0e0091a058b572ed433fb12ae18e8")
    version("0.1.9", sha256="2a7913b601bec615208585eda7e69998a43cc17080d36c2ff2ce8742c9794bf6")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("py-click@6.6:", type=("build", "run"))
