# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMinkowskiengine(PythonPackage, CudaPackage):
    """The MinkowskiEngine is an auto-differentiation
    library for sparse tensors."""

    homepage = "https://nvidia.github.io/MinkowskiEngine/"
    pypi = "MinkowskiEngine/MinkowskiEngine-0.5.4.tar.gz"

    maintainers("wdconinc")

    version("0.5.4", sha256="b1879c00d0b0b1d30ba622cce239886a7e3c78ee9da1064cdfe2f64c2ab15f94")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", type="link")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")
    # According to the documentation other BLAS should be possible too, but
    # they didn't work, see https://github.com/spack/spack/pull/38742
    depends_on("openblas")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-torch", type=("build", "run"))

    def install_options(self, spec, prefix):
        options = []
        if spec.satisfies("+cuda"):
            options.append("--force_cuda")
        else:
            options.append("--cpu_only")
        return options
