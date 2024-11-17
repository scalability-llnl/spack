# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribApplehelp(PythonPackage):
    """sphinxcontrib-applehelp is a sphinx extension which outputs Apple
    help books."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-applehelp/sphinxcontrib_applehelp-2.0.0.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-applehelp.git"

    # 'sphinx' requires 'sphinxcontrib-applehelp' at build-time, but
    # 'sphinxcontrib-applehelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules for this package.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version("2.0.0", sha256="2f29ef331735ce958efa4734873f084941970894c6090408b079c61b2e1c06d1")
    version("1.0.4", sha256="828f867945bbe39817c210a1abfd1bc4895c8b73fcaade56d45357a348a07d7e")
    version("1.0.2", sha256="a072735ec80e7675e3f432fcae8610ecf509c5f1869d17e2eecff44389cdbc58")
    version("1.0.1", sha256="edaa0ab2b2bc74403149cb0209d6775c96de797dfd5b5e2a71981309efab3897")

    depends_on("py-flit-core@3.7:", when="@1.0.5:", type="build")
    depends_on("py-setuptools@64:", when="@1.0.4", type="build")
    depends_on("py-setuptools", when="@:1.0.3", type="build")

    def url_for_version(self, version):
        url = (
            "https://files.pythonhosted.org/packages/source/s/sphinxcontrib-applehelp/{}-{}.tar.gz"
        )
        if version >= Version("1.0.5"):
            name = "sphinxcontrib_applehelp"
        else:
            name = "sphinxcontrib-applehelp"
        return url.format(name, version)
