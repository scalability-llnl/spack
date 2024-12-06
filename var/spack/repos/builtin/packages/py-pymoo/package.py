# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PyPymoo(PythonPackage):
    """
    Multi-Objective Optimization in Python
    """

    homepage = "https://pymoo.org"
    pypi = "pymoo/pymoo-0.5.0.tar.gz"
    maintainers("liuyangzhuan")

    license("Apache-2.0")

    version("0.5.0", sha256="2fbca1716f6b45e430197ce4ce2210070fd3b6b9ec6b17bb25d98486115272c2")
    version("0.4.2", sha256="6ec382a7d29c8775088eec7f245a30fd384b42c40f230018dea0e3bcd9aabdf1")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-autograd", type=("build", "run"))
    depends_on("py-setuptools", type="build")
