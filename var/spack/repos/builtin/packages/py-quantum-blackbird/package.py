# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQuantumBlackbird(PythonPackage):
    """Blackbird is a quantum assembly language for continuous-variable quantum
    computation, that can be used to program Xanadu’s quantum photonics
    hardware and Strawberry Fields simulator.
    """

    homepage = "https://github.com/XanaduAI/blackbird"
    pypi = "quantum-blackbird/quantum-blackbird-0.5.0.tar.gz"

    license("Apache-2.0")

    version("0.5.0", sha256="065c73bf5263ce8f9b72dcd2b434f3bfbb471f0a6907c97a617ec0c8bde01db3")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.16:", type=("build", "run"))
    depends_on("py-sympy", type=("build", "run"))
    depends_on("py-antlr4-python3-runtime@4.9.2", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
