# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQuantumXir(PythonPackage):
    """XIR is an intermediate representation language for quantum circuits."""

    homepage = "https://github.com/XanaduAI/xir"
    pypi = "quantum-xir/quantum-xir-0.2.2.tar.gz"

    license("Apache-2.0")

    version("0.2.2", sha256="4b6a60bd3dcddb455e33b036b320cf634c5bd772ecea031b110fc5fb2fcf8a51")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-lark-parser@0.11.0:", type=("build", "run"))
