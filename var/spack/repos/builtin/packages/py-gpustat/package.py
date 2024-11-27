# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGpustat(PythonPackage):
    """An utility to monitor NVIDIA GPU status and usage."""

    homepage = "https://github.com/wookayin/gpustat"
    pypi = "gpustat/gpustat-0.6.0.tar.gz"

    license("MIT")

    version("1.0.0b1", sha256="a25c460c5751180265814f457249ba5100baf7a055b23ad762a4e3ab3f6496dd")
    version(
        "0.6.0",
        sha256="f69135080b2668b662822633312c2180002c10111597af9631bb02e042755b6c",
        preferred=True,
    )

    depends_on("python@3.4:", when="@1.0.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", when="@0.6.0", type="build")
    depends_on("py-pytest-runner@5:", when="@1:", type="build")
    depends_on("py-six@1.7:", type=("build", "run"))
    depends_on("py-nvidia-ml-py3@7.352.0:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-blessings@1.6:", when="@0.6.0", type=("build", "run"))
    depends_on("py-blessed@1.17.1:", when="@1.0.0:", type=("build", "run"))
