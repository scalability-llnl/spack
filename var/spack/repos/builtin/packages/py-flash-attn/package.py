# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlashAttn(PythonPackage):
    """
    This package provides the official implementation of FlashAttention.
    """

    homepage = "https://github.com/Dao-AILab/flash-attention.git"
    pypi = "flash-attn/flash_attn-0.0.0.tar.gz"
    git = "https://github.com/Dao-AILab/flash-attention.git"

    maintainers("aurianer")

    license("BSD")

    version("main", branch="main")
    version("2.6.3", sha256="5bfae9500ad8e7d2937ebccb4906f3bc464d1bf66eedd0e4adabd520811c7b52")
    version(
        "2.5.9.post1", sha256="a92db1683a5b141a0f4371d251ae9f73e9aef629b3a58a50d0ef430266c68782"
    )
    version("2.5.8", sha256="2e5b2bcff6d5cff40d494af91ecd1eb3c5b4520a6ce7a0a8b1f9c1ed129fb402")
    version("2.5.7", sha256="7c079aef4e77c4e9a71a3cd88662362e0fe82f658db0b2dbff6f279de2a387a8")
    version("2.5.6", sha256="d25801aa060877cad997939bd7130faf620fdbeda947c3ffde5865906d430c36")
    version("2.5.5", sha256="751cee17711d006fe7341cdd78584af86a6239afcfe43b9ed11c84db93126267")
    version("2.5.4", sha256="d83bb427b517b07e9db655f6e5166eb2607dccf4d6ca3229e3a3528c206b0175")
    version("2.4.2", sha256="eb822a8c4219b610e9d734cbc8cd9ee4547f27433815a2b90dc1462766feefc1")

    depends_on("cxx", type="build")  # generated

    with default_args(type="build"):
        depends_on("py-packaging")
        depends_on("py-psutil")
        depends_on("py-setuptools")
        depends_on("ninja")

    with default_args(type=("build", "run")):
        depends_on("py-torch+cuda")
        depends_on("py-einops")

    with default_args(type=("build", "link", "run")):
        depends_on("py-pybind11")

    depends_on("python@3.7:", type=("build", "run"), when="@:2.5")
    depends_on("python@3.8:", type=("build", "run"), when="@2.6:")

    def setup_build_environment(self, env):
        # If oom error, try lowering the number of jobs with `spack install -j`
        env.set("MAX_JOBS", make_jobs)
