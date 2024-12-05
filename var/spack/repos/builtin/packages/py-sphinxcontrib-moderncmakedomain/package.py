# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribModerncmakedomain(PythonPackage):
    """Sphinx Domain for Modern CMake."""

    homepage = "https://github.com/scikit-build/moderncmakedomain"
    pypi = "sphinxcontrib_moderncmakedomain/sphinxcontrib_moderncmakedomain-3.25.0.tar.gz"

    maintainers("LydDeb")

    license("BSD-3-Clause")

    version("3.27.0", sha256="51e259e91f58d17cc0fac9307fd40106aa59d5acaa741887903fc3660361d1a1")
    version("3.26.4", sha256="c4a62d586ed1a9baf1790b816fcc04c249dd3ac239bc7c7b79663951a0a463b8")
    version("3.25.0", sha256="4138e4d3f60e5c4b3982caa10033693bfc1009cdd851766754d5990d9d1e992a")

    depends_on("py-hatchling", type="build")
    depends_on("py-sphinx@2:", when="@3.27:", type=("build", "run"))
    depends_on("py-sphinx", type=("build", "run"))
