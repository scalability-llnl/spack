# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMerlin(PythonPackage):
    """Merlin Workflow for HPC."""

    homepage = "https://github.com/LLNL/merlin"
    pypi = "merlin/merlin-1.4.1.tar.gz"
    git = "https://github.com/LLNL/merlin.git"
    tags = ["radiuss"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.10.3", sha256="6edaf17b502db090cef0bc53ae0118c55f77d7a16f43c7a235e0dd1770decadb")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-cached-property", type=("build", "run"))
    depends_on("py-celery@5.0.3:+redis+sqlalchemy", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-cryptography", type=("build", "run"))
    depends_on("py-maestrowf@1.1.9:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-parse", type=("build", "run"))
    depends_on("py-psutil@5.1.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.1.2:", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-redis@4.3.4:", type=("build", "run"))
