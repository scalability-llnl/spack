# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYacman(PythonPackage):
    """A YAML configuration manager."""

    homepage = "https://github.com/databio/yacman"
    pypi = "yacman/yacman-0.8.4.tar.gz"

    license("BSD-2-Clause")

    version("0.8.4", sha256="807972d7f9251f71401fc4ff6c01734ccdad1f92cefd1fd251336a2a094608bd")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-attmap@0.13.0:", type=("build", "run"))
    depends_on("py-jsonschema@3.2.0:", type=("build", "run"))
    depends_on("py-oyaml", type=("build", "run"))
    depends_on("py-pyyaml@3.13:", type=("build", "run"))
    depends_on("py-ubiquerg@0.6.1:", type=("build", "run"))
