# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchVcs(PythonPackage):
    """Hatch plugin for versioning with your preferred VCS"""

    homepage = "https://github.com/ofek/hatch-vcs"
    pypi = "hatch_vcs/hatch_vcs-0.2.0.tar.gz"

    license("MIT")

    version("0.4.0", sha256="093810748fe01db0d451fabcf2c1ac2688caefd232d4ede967090b1c1b07d9f7")
    version("0.3.0", sha256="cec5107cfce482c67f8bc96f18bbc320c9aa0d068180e14ad317bbee5a153fee")
    version("0.2.0", sha256="9913d733b34eec9bb0345d0626ca32165a4ad2de15d1ce643c36d09ca908abff")

    depends_on("py-hatchling@1.24.2:", when="@0.4:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.4:", type=("build", "run"))
    depends_on("py-hatchling@1.1:", when="@0.3:", type=("build", "run"))
    depends_on("py-setuptools-scm@6.4.0:", type=("build", "run"))
