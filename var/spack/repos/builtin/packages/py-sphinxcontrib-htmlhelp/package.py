# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribHtmlhelp(PythonPackage):
    """sphinxcontrib-htmlhelp is a sphinx extension which outputs htmlhelp
    document."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-htmlhelp/sphinxcontrib_htmlhelp-2.1.0.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-htmlhelp.git"

    # 'sphinx' requires 'sphinxcontrib-htmlhelp' at build-time, but
    # 'sphinxcontrib-htmlhelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version("2.1.0", sha256="c9e2916ace8aad64cc13a0d233ee22317f2b9025b9cf3295249fa985cc7082e9")
    version("2.0.1", sha256="0cbdd302815330058422b98a113195c9249825d681e18f11e8b1f78a2f11efff")
    version("2.0.0", sha256="f5f8bb2d0d629f398bf47d0d69c07bc13b65f75a81ad9e2f71a63d4b7a2f6db2")
    version("1.0.2", sha256="4670f99f8951bd78cd4ad2ab962f798f5618b17675c35c5ac3b2132a14ea8422")

    depends_on("py-flit-core@3.7:", when="@2.0.2:", type="build")
    depends_on("py-setuptools@64:", when="@2.0.1", type="build")
    depends_on("py-setuptools", when="@:2.0.0", type="build")

    def url_for_version(self, version):
        url = (
            "https://files.pythonhosted.org/packages/source/s/sphinxcontrib-htmlhelp/{}-{}.tar.gz"
        )
        if version >= Version("2.0.2"):
            name = "sphinxcontrib_htmlhelp"
        else:
            name = "sphinxcontrib-htmlhelp"
        return url.format(name, version)
