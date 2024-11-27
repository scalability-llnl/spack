# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCloudpickle(PythonPackage):
    """Extended pickling support for Python objects."""

    homepage = "https://github.com/cloudpipe/cloudpickle"
    pypi = "cloudpickle/cloudpickle-0.5.2.tar.gz"

    license("BSD-3-Clause")

    version("3.0.0", sha256="996d9a482c6fb4f33c1a35335cf8afd065d2a56e973270364840712d9131a882")
    version("2.2.1", sha256="d89684b8de9e34a2a43b3460fbca07d09d6e25ce858df4d5a44240403b6178f5")
    version("2.2.0", sha256="3f4219469c55453cfe4737e564b67c2a149109dabf7f242478948b895f61106f")
    version("1.6.0", sha256="9bc994f9e9447593bd0a45371f0e7ac7333710fcf64a4eb9834bf149f4ef2f32")
    version("1.2.1", sha256="603244e0f552b72a267d47a7d9b347b27a3430f58a0536037a290e7e0e212ecf")
    version("1.1.1", sha256="7d43c4d0c7e9735ee8a352c96f84031dabd6676170c4e5e0585a469cc4769f22")
    version("0.5.2", sha256="b0e63dd89ed5285171a570186751bc9b84493675e99e12789e9a5dc5490ef554")

    depends_on("python@3.5:", type=("build", "run"), when="@1.6.0:")
    depends_on("python@3.6:", type=("build", "run"), when="@2.2.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@3:")
    depends_on("py-setuptools", type="build", when="@:2")
    depends_on("py-flit-core", type="build", when="@3:")
