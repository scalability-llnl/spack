# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGpyopt(PythonPackage):
    """Performs global optimization with different acquisition functions. Among
    other functionalities, it is possible to use GPyOpt to optimize physical
    experiments (sequentially or in batches) and tune the parameters of Machine
    Learning algorithms. It is able to handle large data sets via sparse
    Gaussian process models."""

    homepage = "http://sheffieldml.github.io/GPyOpt/"
    pypi = "GPyOpt/GPyOpt-1.2.6.tar.gz"

    license("BSD-3-Clause")

    version("1.2.6", sha256="e714daa035bb529a6db23c53665a762a4ab3456b9329c19ad3b03983f94c9b2a")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy@0.16:", type=("build", "run"))
    depends_on("py-gpy@1.8:", type=("build", "run"))
