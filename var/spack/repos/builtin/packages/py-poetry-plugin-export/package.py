# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryPluginExport(PythonPackage):
    """Poetry plugin to export the dependencies to various formats"""

    homepage = "https://python-poetry.org/"
    pypi = "poetry-plugin-export/poetry_plugin_export-1.6.0.tar.gz"

    license("MIT")

    version("1.6.0", sha256="091939434984267a91abf2f916a26b00cff4eee8da63ec2a24ba4b17cf969a59")
    version("1.0.7", sha256="f6ac707ae227b06b2481249ed2678ff6b810b3487cac0fbb66eb0dc2bfd6ecf1")

    depends_on("python@3.8:3", when="@1.6:", type=("build", "run"))
    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1.7:1", when="@1.6", type=("build", "run"))
    depends_on("py-poetry-core@1.1:1", when="@1.0", type=("build", "run"))
    # depends_on("py-poetry@1.6:1", when="@1.6", type=("build", "run")) # circular dependency
    # depends_on("py-poetry@1.2:1", type="run") # circular dependency

    def url_for_version(self, version):
        url = (
            "https://files.pythonhosted.org/packages/source/p/poetry-plugin-export/{0}-{1}.tar.gz"
        )
        if version >= Version("1.6"):
            letter = "poetry_plugin_export"
        else:
            letter = "poetry-plugin-export"
        return url.format(letter, version)
