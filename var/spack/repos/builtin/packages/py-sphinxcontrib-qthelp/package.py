# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribQthelp(PythonPackage):
    """sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp
    document."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-qthelp/sphinxcontrib_qthelp-2.0.0.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-qthelp.git"

    # 'sphinx' requires 'sphinxcontrib-qthelp' at build-time, but
    # 'sphinxcontrib-qthelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version("2.0.0", sha256="4fe7d0ac8fc171045be623aba3e2a8f613f8682731f9153bb2e40ece16b9bbab")
    version("1.0.3", sha256="4c33767ee058b70dba89a6fc5c1892c0d57a54be67ddd3e7875a18d14cba5a72")
    version("1.0.2", sha256="79465ce11ae5694ff165becda529a600c754f4bc459778778c7017374d4d406f")

    depends_on("py-flit-core@3.7:", when="@1.0.4:", type="build")
    depends_on("py-setuptools", when="@:1.0.3", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/s/sphinxcontrib-qthelp/{}-{}.tar.gz"
        if version >= Version("1.0.4"):
            name = "sphinxcontrib_qthelp"
        else:
            name = "sphinxcontrib-qthelp"
        return url.format(name, version)
