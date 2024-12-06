# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCoveralls(PythonPackage):
    """coveralls.io is a service for publishing your coverage stats online."""

    homepage = "https://coveralls-python.readthedocs.io/en/latest/index.html"
    pypi = "coveralls/coveralls-3.0.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("3.0.1", sha256="cbb942ae5ef3d2b55388cb5b43e93a269544911535f1e750e1c656aef019ce60")

    variant("pyyaml", default=False, description="Enable useage of pyyaml")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@3.10:", type=("build", "run"), when="+pyyaml")
    depends_on("py-coverage@4.1:5", type=("build", "run"))
    depends_on("py-docopt@0.6.1:", type=("build", "run"))
    depends_on("py-pyyaml@1.0.0:", type=("build", "run"))
