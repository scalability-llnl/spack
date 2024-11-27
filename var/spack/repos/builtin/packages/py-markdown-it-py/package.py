# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMarkdownItPy(PythonPackage):
    """Markdown parser, done right.
    100% CommonMark support, extensions, syntax plugins & high speed"""

    homepage = "https://github.com/executablebooks/markdown-it-py"
    git = "https://github.com/executablebooks/markdown-it-py"
    pypi = "markdown-it-py/markdown-it-py-1.1.0.tar.gz"

    license("MIT")

    version("3.0.0", sha256="e3f60a94fa066dc52ec76661e37c851cb232d92f9886b15cb560aaada2df8feb")
    version("2.2.0", sha256="7c9a5e412688bc771c67432cbfebcdd686c93ce6484913dccf06cb5a0bea35a1")
    version("1.1.0", sha256="36be6bb3ad987bfdb839f5ba78ddf094552ca38ccbd784ae4f74a4e1419fc6e3")

    variant("linkify", default=False, description="Linkify support")

    depends_on("python@3.8:", when="@2.1:", type=("build", "run"))
    depends_on("python@3.6:3", when="@:2.0", type=("build", "run"))
    depends_on("py-flit-core@3.4:3", when="@2.1:", type="build")

    depends_on("py-mdurl@0.1:0", when="@2:", type=("build", "run"))

    depends_on("py-linkify-it-py@1.0", when="@1.1.0+linkify", type=("build", "run"))
    depends_on("py-linkify-it-py@1:2", when="@2.2:+linkify", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools", when="@:2.0", type="build")
    depends_on("py-attrs@19:21", when="@:2.0", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@:2 ^python@:3.7", type=("build", "run"))
