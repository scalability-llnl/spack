# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPandasDatareader(PythonPackage):
    """Up-to-date remote data access for pandas. Works for multiple versions of pandas"""

    homepage = "https://pypi.org/project/pandas-datareader"
    pypi = "pandas-datareader/pandas-datareader-0.10.0.tar.gz"
    git = "https://github.com/pydata/pandas-datareader.git"

    maintainers("climbfuji")

    license("BSD-3-Clause", checked_by="climbfuji")

    version("0.10.0", sha256="9fc3c63d39bc0c10c2683f1c6d503ff625020383e38f6cbe14134826b454d5a6")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@0.64:", type="build")
    depends_on("py-setuptools-scm@8", type="build")

    depends_on("py-lxml", type="run")
    depends_on("py-pandas@1.5.3:", type="run")
    depends_on("py-statsmodels@0.12:", type="run")
    depends_on("py-requests@2.19:", type="run")
