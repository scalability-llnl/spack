# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMultiAgentAlePy(PythonPackage):
    """The Multi-Agent Arcade Learning Environment"""

    homepage = "https://github.com/Farama-Foundation/Multi-Agent-ALE"
    pypi = "multi-agent-ale-py/multi-agent-ale-py-0.1.11.tar.gz"

    license("GPL 2.0", checked_by="ashim-mahara ")

    version("0.1.11", sha256="ba3ff800420f65ff354574975bdfa79035ae1597e8938b37d1df12ffc4122edb")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("cmake@3.14:", type="build")
    depends_on("ninja", type="build")
