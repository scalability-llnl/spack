# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E4sAlc(PythonPackage):
    """Container file creator, facilitating the generation of
    Dockerfiles and Singularity definition files infused with OS packages,
    spack packages and custom commands"""

    maintainers("FrederickDeny", "PlatinumCD")
    homepage = "https://github.com/E4S-Project/e4s-alc"
    git = "https://github.com/E4S-Project/e4s-alc"

    tags = ["e4s"]

    license("MIT")

    version("main", branch="main")
    version("1.0.2", commit="9eddfc61659ecab3c0253b2eac020ddb6e610b49")
    version("1.0.1", commit="262298128a4991ffc773b1bd835687fb6493311e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml@6.0:", type=("build", "run"))
