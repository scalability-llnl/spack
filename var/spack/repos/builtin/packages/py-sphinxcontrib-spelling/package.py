# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribSpelling(PythonPackage):
    """A spelling checker for Sphinx-based documentation"""

    homepage = "https://sphinxcontrib-spelling.readthedocs.io"
    pypi = "sphinxcontrib-spelling/sphinxcontrib-spelling-8.0.0.tar.gz"

    maintainers("rbberger")

    license("BSD-2-Clause")

    version("8.0.0", sha256="199d0a16902ad80c387c2966dc9eb10f565b1fb15ccce17210402db7c2443e5c")

    depends_on("python@3.7:")
    depends_on("py-sphinx@3:")
    depends_on("py-pyenchant@3.1.1:")
