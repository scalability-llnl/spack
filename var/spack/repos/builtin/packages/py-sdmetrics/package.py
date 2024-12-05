# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySdmetrics(PythonPackage):
    """The SDMetrics library provides a set of dataset-agnostic
    tools for evaluating the quality of a synthetic database
    by comparing it to the real database that it is modeled
    after."""

    maintainers("Kerilk", "jke513")

    homepage = "https://github.com/sdv-dev/SDMetrics"
    pypi = "sdmetrics/sdmetrics-0.4.1.tar.gz"

    license("MIT")

    version("0.4.1", sha256="28df1cdd6988b3464306c1d189da19ee13a49023c53ca8b3db399fc9fd45fae8")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.20:1", type=("build", "run"))
    depends_on("py-pandas@1.1.3:1.1.4", type=("build", "run"))
    depends_on("py-scikit-learn@0.24:1", type=("build", "run"))
    depends_on("py-scipy@1.5.4:1", type=("build", "run"))
    depends_on("py-torch@1.8.0:1", type=("build", "run"))
    depends_on("py-copulas@0.6.0:0.6", type=("build", "run"))
    depends_on("py-rdt@0.6.1:0.6", type=("build", "run"))
    depends_on("py-pyts@0.12.0:0.12", type=("build", "run"))
