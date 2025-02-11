# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMkdocsMinifyPlugin(PythonPackage):
    """An MkDocs plugin to minify HTML, JS or CSS files prior to being written to disk."""

    pypi = "mkdocs-minify-plugin/mkdocs-minify-plugin-0.8.0.tar.gz"

    license("MIT", checked_by="lizzyd710")

    version("0.8.0", sha256="bc11b78b8120d79e817308e2b11539d790d21445eb63df831e393f76e52e753d")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-mkdocs@1.4.1:", type=("build", "run"))
    depends_on("py-htmlmin2@0.1.13:", type=("build", "run"))
    depends_on("py-jsmin@3.0.1:", type=("build", "run"))
    depends_on("py-csscompressor@0.9.5:", type=("build", "run"))
