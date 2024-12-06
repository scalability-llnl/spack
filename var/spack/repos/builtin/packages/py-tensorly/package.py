# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorly(PythonPackage):
    """TensorLy is a Python library that aims at making tensor learning simple
    and accessible. It allows to easily perform tensor decomposition, tensor
    learning and tensor algebra. Its backend system allows to seamlessly perform
    computation with NumPy, PyTorch, JAX, MXNet, TensorFlow or CuPy, and run
    methods at scale on CPU or GPU."""

    homepage = "https://github.com/tensorly/tensorly"
    pypi = "tensorly/tensorly-0.8.1.tar.gz"

    maintainers("meyersbs")

    version("0.8.1", sha256="cf78e4ffe612feca3510214002845c6831b267b1f2c1181154d41430310b237d")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
