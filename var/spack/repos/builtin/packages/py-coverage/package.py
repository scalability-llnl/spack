# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCoverage(PythonPackage):
    """Testing coverage checker for python"""

    homepage = "https://github.com/nedbat/coveragepy"
    pypi = "coverage/coverage-4.5.4.tar.gz"

    license("Apache-2.0")

    version("7.2.6", sha256="2025f913f2edb0272ef15d00b1f335ff8908c921c8eb2013536fcaf61f5a683d")
    version("6.4.4", sha256="e16c45b726acb780e1e6f88b286d3c10b3914ab03438f32117c4aa52d7f30d58")
    version("6.3.1", sha256="6c3f6158b02ac403868eea390930ae64e9a9a2a5bbfafefbb920d29258d9f2f8")
    version("6.1.2", sha256="d9a635114b88c0ab462e0355472d00a180a5fbfd8511e7f18e4ac32652e7d972")
    version("5.5", sha256="ebe78fe9a0e874362175b02371bdfbee64d8edc42a044253ddf4ee7d3c15212c")
    version("5.3", sha256="280baa8ec489c4f542f8940f9c4c2181f0306a8ee1a54eceba071a449fb870a0")
    version("5.0.4", sha256="1b60a95fc995649464e0cd48cecc8288bac5f4198f21d04b8229dc4097d76823")
    version("4.5.4", sha256="e07d9f1a23e9e93ab5c62902833bf3e4b1f65502927379148b6622686223125c")
    version("4.5.3", sha256="9de60893fb447d1e797f6bf08fdf0dbcda0c1e34c1b06c92bd3a363c0ea8c609")
    version("4.3.4", sha256="eaaefe0f6aa33de5a65f48dd0040d7fe08cac9ac6c35a56d0a7db109c3e733df")
    version("4.0a6", sha256="85c7f3efceb3724ab066a3fcccc05b9b89afcaefa5b669a7e2222d31eac4728d")

    depends_on("c", type="build")  # generated

    variant("toml", default=False, description="Enable pyproject.toml support")

    depends_on("py-setuptools", type="build")
    depends_on("py-tomli", when="@6: +toml ^python@:3.10", type=("build", "run"))
    depends_on("py-toml", when="@:5 +toml", type=("build", "run"))
