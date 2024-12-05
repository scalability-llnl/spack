# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRichClick(PythonPackage):
    """The intention of rich-click is to provide attractive help output
    from click, formatted with rich, with minimal customisation required."""

    homepage = "https://github.com/ewels/rich-click"
    pypi = "rich-click/rich-click-1.5.2.tar.gz"

    license("MIT")

    version("1.5.2", sha256="a57ca70242cb8b372a670eaa0b0be48f2440b66656deb4a56e6aadc1bbb79670")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click@7:", type=("build", "run"))
    depends_on("py-rich@10.7.0:", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
