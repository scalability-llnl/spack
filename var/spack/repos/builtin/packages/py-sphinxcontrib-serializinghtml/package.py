# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribSerializinghtml(PythonPackage):
    """sphinxcontrib-serializinghtml is a sphinx extension which outputs
    "serialized" HTML files (json and pickle)."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-serializinghtml/sphinxcontrib_serializinghtml-1.1.3.tar.gz"

    # 'sphinx' requires 'sphinxcontrib-serializinghtml' at build-time, but
    # 'sphinxcontrib-serializinghtml' requires 'sphinx' at run-time. Don't bother trying
    # to import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version("1.1.9", sha256="0c64ff898339e1fac29abd2bf5f11078f3ec413cfe9c046d3120d7ca65530b54")
    version("1.1.5", sha256="aa5f6de5dfdf809ef505c4895e51ef5c9eac17d0f287933eb49ec495280b6952")
    version("1.1.3", sha256="c0efb33f8052c04fd7a26c0a07f1678e8512e0faec19f4aa8f2473a8b81d5227")

    depends_on("python@3.9:", when="@1.1.6:", type=("build", "run"))
    depends_on("py-flit-core@3.7:", when="@1.1.6:", type="build")

    # Circular dependency
    # depends_on("py-sphinx@5:", when="@1.1.6:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools", when="@:1.1.5", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/s/sphinxcontrib-serializinghtml/sphinxcontrib{}serializinghtml-{}.tar.gz"
        if version >= Version("1.1.6"):
            separator = "_"
        else:
            separator = "-"
        return url.format(separator, version)
