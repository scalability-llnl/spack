# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnnexremote(PythonPackage):
    """git annex special remotes made easy."""

    homepage = "https://github.com/Lykos153/AnnexRemote"
    pypi = "annexremote/annexremote-1.5.0.tar.gz"

    license("GPL-3.0-only")

    version("1.6.0", sha256="779a43e5b1b4afd294761c6587dee8ac68f453a5a8cc40f419e9ca777573ae84")
    version("1.5.0", sha256="92f32b6f5461cbaeefe0c60b32f9c1e0c1dbe4e57b8ee425affb56f4060f64ef")

    depends_on("python@3:", when="@1.6:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-future", when="@:1.5", type=("build", "run"))
