# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CodarCheetah(PythonPackage):
    """CODAR Cheetah:
    The CODAR Experiment Harness for Exascale science applications.
    """

    maintainers("kshitij-v-mehta")

    homepage = "https://github.com/CODARcode/cheetah"
    url = "https://github.com/CODARcode/cheetah/archive/v1.1.0.tar.gz"
    git = "https://github.com/CODARcode/cheetah.git"

    version("develop", branch="dev")
    version("1.1.0", sha256="519a47e4fc5b124b443839fde10b8b72120ab768398628df43e0b570a266434c")
    version("1.0.0", sha256="1f935fbc1475a654f3b6d2140d8b2a6079a65c8701655e544ba1fab3a7c1bc19")
    version("0.5", sha256="f37a554741eff4bb8407a68f799dd042dfc4df525e84896cad70fccbd6aca6ee")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
