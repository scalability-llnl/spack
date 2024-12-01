# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCiSdr(PythonPackage):
    """This repository contains an implementation for the Convolutive transfer
    function Invariant Signal-to-Distortion Ratio objective for PyTorch as
    described in the publication Convolutive Transfer Function Invariant SDR
    training criteria for Multi-Channel Reverberant Speech Separation"""

    homepage = "https://github.com/fgnt/ci_sdr"
    pypi = "ci_sdr/ci_sdr-0.0.0.tar.gz"

    license("MIT")

    version("0.0.0", sha256="a1387f39ccd55cce034e2c01000a0a337b3729d8a5010b42c5381d8c820fa4bb")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-einops", type=("build", "run"))
