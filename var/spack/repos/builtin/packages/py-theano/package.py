# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTheano(PythonPackage, CudaPackage):
    """Optimizing compiler for evaluating mathematical expressions on CPUs
    and GPUs."""

    homepage = "https://theano-pymc.readthedocs.io/en/latest/"
    pypi = "Theano/Theano-0.8.2.tar.gz"
    git = "https://github.com/Theano/Theano.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.0.5", sha256="6e9439dd53ba995fcae27bf20626074bfc2fff446899dc5c53cb28c1f9202e89")
    version("1.0.4", sha256="35c9bbef56b61ffa299265a42a4e8f8cb5a07b2997dabaef0f8830b397086913")
    version("1.0.2", sha256="6768e003d328a17011e6fca9126fbb8a6ffd3bb13cb21c450f3e724cca29abde")
    version("1.0.1", sha256="88d8aba1fe2b6b75eacf455d01bc7e31e838c5a0fb8c13dde2d9472495ff4662")
    version("0.8.2", sha256="7463c8f7ed1a787bf881f36d38a38607150186697e7ce7e78bfb94b7c6af8930")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6:2.8,3.3:", type=("build", "run"))

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy@1.9.1:", type=("build", "run"))
    depends_on("py-scipy@0.14:", type=("build", "run"))
    depends_on("py-six@1.9.0:", type=("build", "run"))

    depends_on("blas")

    depends_on("cuda", when="+cuda")
    depends_on("cudnn", when="+cuda")
    depends_on("py-pygpu", when="+cuda", type=("build", "run"))
    depends_on("libgpuarray", when="+cuda")
