# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCmsml(PythonPackage):
    """Python package of the CMS Machine Learning Group."""

    homepage = "https://github.com/cms-ml/cmsml"
    pypi = "cmsml/cmsml-0.1.2.tar.gz"

    license("BSD-3-Clause")

    version("0.1.2", sha256="2e2e114323441757a64e1c24179fc6295e7bd14920b7a9c3c37128eb40ad9ceb")

    depends_on("python@2.7:2.7,3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.13:", type=("build", "run"))
