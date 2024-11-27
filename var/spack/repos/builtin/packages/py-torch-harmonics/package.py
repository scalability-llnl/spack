# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchHarmonics(PythonPackage):
    """A differentiable spherical harmonic transform for PyTorch."""

    homepage = "https://github.com/NVIDIA/torch-harmonics"
    pypi = "torch_harmonics/torch_harmonics-0.6.5.tar.gz"

    maintainers("adamjstewart")

    license("BSD")

    version("0.6.5", sha256="e467d04bc58eb2dc800eb21870025407d38ebcbf8df4de479bd5b4915daf987e")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-triton", type=("build", "run"))
