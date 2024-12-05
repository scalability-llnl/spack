# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTweedledum(PythonPackage):
    """tweedledum is a library for synthesis, compilation, and
    optimization of quantum circuits. The library is written to be
    scalable up to problem sizes in which quantum circuits outperform
    classical ones. Also, it is meant to be used both independently
    and alongside established tools."""

    homepage = "https://github.com/boschmitt/tweedledum"
    pypi = "tweedledum/tweedledum-1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="58d6f7a988b10c31be3faa1faf3e58288ef7e8159584bfa6ded45742f390309f")

    depends_on("cxx", type="build")  # generated
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build@0.12:", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("ninja", type="build")
    depends_on("py-wheel", type="build")
    depends_on("eigen@3.3:")
    depends_on("nlohmann-json@3.9.0:")
