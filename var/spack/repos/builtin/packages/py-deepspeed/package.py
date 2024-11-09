# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepspeed(PythonPackage):
    """DeepSpeed library.

    DeepSpeed enables world's most powerful language models like MT-530B and BLOOM. It is an
    easy-to-use deep learning optimization software suite that powers unprecedented scale and
    speed for both training and inference.
    """

    homepage = "http://deepspeed.ai/"
    pypi = "deepspeed/deepspeed-0.10.0.tar.gz"

    license("Apache-2.0")

    version("0.10.0", sha256="afb06a97fde2a33d0cbd60a8357a70087c037b9f647ca48377728330c35eff3e")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-hjson", type=("build", "run"))
    depends_on("ninja", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging@20:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-py-cpuinfo", type=("build", "run"))
    depends_on("py-pydantic@:1", type=("build", "run"))
    # https://github.com/microsoft/DeepSpeed/issues/2830
    depends_on("py-torch+distributed", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
