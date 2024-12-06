# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGxformat2(PythonPackage):
    """Galaxy Workflow Format 2 Descriptions"""

    homepage = "https://github.com/galaxyproject/gxformat2"
    pypi = "gxformat2/gxformat2-0.16.0.tar.gz"
    # note that requirements.txt is missing from the tarball. it can be found on github.

    license("MIT")

    version("0.16.0", sha256="16ff5aae1456e0a65c1ed644537e66626ea047a567c8eda19d2a2eb0b20fb752")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-bioblend", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-schema-salad@8.2:", type=("build", "run"))
