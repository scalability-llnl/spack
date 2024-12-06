# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMditPyPlugins(PythonPackage):
    """Collection of core plugins for markdown-it-py"""

    homepage = "https://github.com/executablebooks/mdit-py-plugins/"
    git = "https://github.com/executablebooks/mdit-py-plugins/"
    pypi = "mdit-py-plugins/mdit-py-plugins-0.3.1.tar.gz"

    license("MIT")

    version("0.3.1", sha256="3fc13298497d6e04fe96efdd41281bfe7622152f9caa1815ea99b5c893de9441")
    version("0.2.8", sha256="5991cef645502e80a5388ec4fc20885d2313d4871e8b8e320ca2de14ac0c015f")

    depends_on("py-flit-core@3.4:3", when="@0.3.1", type=("build", "run"))
    depends_on("python@3.7:", when="@0.3.1", type=("build", "run"))
    depends_on("py-markdown-it-py@1.0:2", when="@0.3.1", type=("build", "run"))

    depends_on("py-setuptools", when="@:0.2", type="build")
    depends_on("py-markdown-it-py@1.0:1", when="@0.2.8", type=("build", "run"))
    depends_on("python@3.6:3", when="@0.2.8", type=("build", "run"))
