# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIsaRwval(PythonPackage):
    """Metadata tracking tools help to manage an increasingly diverse set
    of life science, environmental and biomedical experiments
    """

    homepage = "https://github.com/ISA-tools/isa-rwval"
    pypi = "isa-rwval/isa-rwval-0.10.10.tar.gz"

    version("0.10.10", sha256="3e9fcf37d5e5ff7e92cf28069ecd95d1e62a4025c2d667519da382e5c2258e51")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-networkx@2.5", type=("build", "run"))
