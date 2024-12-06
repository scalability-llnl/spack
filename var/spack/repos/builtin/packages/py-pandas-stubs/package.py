# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPandasStubs(PythonPackage):
    """These are public type stubs for pandas, following the convention of
    providing stubs in a separate package, as specified in PEP 561. The stubs
    cover the most typical use cases of pandas. In general, these stubs are
    narrower than what is possibly allowed by pandas, but follow a convention of
    suggesting best recommended practices for using pandas."""

    homepage = "https://pandas.pydata.org/"
    pypi = "pandas_stubs/pandas_stubs-2.0.2.230605.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.0.2.230605", sha256="624c7bb06d38145a44b61be459ccd19b038e0bf20364a025ecaab78fea65e858"
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-numpy@1.24.3:", type=("build", "run"))
    depends_on("py-types-pytz@2022.1.1:", type=("build", "run"))
