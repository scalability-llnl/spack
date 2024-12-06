# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPandocfilters(PythonPackage):
    """A python module for writing pandoc filters"""

    homepage = "https://github.com/jgm/pandocfilters"
    pypi = "pandocfilters/pandocfilters-1.4.2.tar.gz"

    license("BSD-3-Clause")

    version("1.5.0", sha256="0b679503337d233b4339a817bfc8c50064e2eff681314376a47cb582305a7a38")
    version("1.4.2", sha256="b3dd70e169bb5449e6bc6ff96aea89c5eea8c5f6ab5e207fc2f521a2cf4a0da9")

    depends_on("python@2.7:2,3.4:", type=("build", "run"), when="@1.5.0:")
    depends_on("py-setuptools", type="build")
