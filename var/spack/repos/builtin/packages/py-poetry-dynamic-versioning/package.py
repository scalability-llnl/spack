# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryDynamicVersioning(PythonPackage):
    """Plugin for Poetry to enable dynamic versioning based on VCS tags."""

    homepage = "https://github.com/mtkennerly/poetry-dynamic-versioning"
    pypi = "poetry_dynamic_versioning/poetry_dynamic_versioning-1.4.0.tar.gz"

    license("MIT")

    version("1.4.0", sha256="725178bd50a22f2dd4035de7f965151e14ecf8f7f19996b9e536f4c5559669a7")
    version("0.19.0", sha256="a11a7eba6e7be167c55a1dddec78f52b61a1832275c95519ad119c7a89a7f821")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")

    depends_on("py-dunamai@1.12:1", type=("build", "run"))
    depends_on("py-tomlkit@0.4:", type=("build", "run"))
    depends_on("py-jinja2@2.11.1:3", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/p/{0}/{0}-{1}.tar.gz"
        if version >= Version("1"):
            letter = "poetry_dynamic_versioning"
        else:
            letter = "poetry-dynamic-versioning"
        return url.format(letter, version)
