# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PyLhsmdu(PythonPackage):
    """Latin Hypercube Sampling with Multi-Dimensional Uniformity (LHS-MDU)
    from Deutsch and Deutsch, Latin hypercube sampling with multidimensional
    uniformity."""

    homepage = "https://github.com/sahilm89/lhsmdu"
    pypi = "lhsmdu/lhsmdu-1.1.tar.gz"
    maintainers("liuyangzhuan")

    license("MIT")

    version("1.1", sha256="4bc1df6b9cdd27bae0bff75cf1693f455ba32e4fa87ca9a932f60696607fe712")
    version("0.1", sha256="ef462054b354cd20b10c6d80876c8fdb552a8d2e23eaf74179dc91956d68d32a")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
