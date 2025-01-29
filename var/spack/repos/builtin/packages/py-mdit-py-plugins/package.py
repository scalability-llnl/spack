# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMditPyPlugins(PythonPackage):
    """Collection of core plugins for markdown-it-py"""

    homepage = "https://github.com/executablebooks/mdit-py-plugins/"
    git = "https://github.com/executablebooks/mdit-py-plugins/"
    pypi = "mdit-py-plugins/mdit_py_plugins-0.4.2.tar.gz"

    license("MIT")

    version("0.4.2", sha256="5f2cd1fdb606ddf152d37ec30e46101a60512bc0e5fa1a7002c36647b09e26b5")
    version("0.3.5", sha256="eee0adc7195e5827e17e02d2a258a2ba159944a0748f59c5099a4a27f78fcf6a")
    version("0.3.1", sha256="3fc13298497d6e04fe96efdd41281bfe7622152f9caa1815ea99b5c893de9441")
    version("0.2.8", sha256="5991cef645502e80a5388ec4fc20885d2313d4871e8b8e320ca2de14ac0c015f")

    def url_for_version(self, version):
        prefix = self.url.rsplit("/", maxsplit=1)[0]
        package = "mdit-py-plugins" if version < Version("2.0.0") else "mdit_py_plugins"
        return f"{prefix}/{package}-{version}.tar.gz"

    depends_on("python@3.6:3", when="@:0.2", type=("build", "run"))
    depends_on("python@3.7:3", when="@0.3", type=("build", "run"))
    depends_on("python@3.8:3", when="@0.4:", type=("build", "run"))

    depends_on("py-setuptools", when="@:0.2", type="build")
    depends_on("py-flit-core@3.4:3", when="@0.3:", type="build")

    depends_on("py-markdown-it-py@1.0:1", when="@:0.2", type=("build", "run"))
    depends_on("py-markdown-it-py@1.0:2", when="@0.3", type=("build", "run"))
    depends_on("py-markdown-it-py@1.0:3", when="@0.4:", type=("build", "run"))
