# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangcodes(PythonPackage):
    """Tools for labeling human languages with IETF language tags"""

    homepage = "https://github.com/rspeer/langcodes"
    pypi = "langcodes/langcodes-3.3.0.tar.gz"

    license("MIT")

    version("3.3.0", sha256="794d07d5a28781231ac335a1561b8442f8648ca07cd518310aeb45d6f0807ef6")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
