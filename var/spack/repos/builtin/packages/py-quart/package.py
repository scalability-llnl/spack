# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuart(PythonPackage):
    """A Python ASGI web microframework with the same API as
    Flask."""

    homepage = "https://gitlab.com/pgjones/quart/"
    pypi = "quart/quart-0.16.3.tar.gz"

    license("MIT")

    version("0.19.8", sha256="ef567d0be7677c99890d5c6ff30e679699fe7e5fca1a90fa3b6974edd8421794")
    version("0.16.3", sha256="16521d8cf062461b158433d820fff509f98fb997ae6c28740eda061d9cba7d5e")

    depends_on("python@3.8:", type=("build", "run"), when="@0.19:")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-aiofiles", type=("build", "run"))
    depends_on("py-blinker@1.6:", type=("build", "run"), when="@0.19:")
    depends_on("py-blinker", type=("build", "run"))
    depends_on("py-click@8.0.0:", type=("build", "run"), when="@0.18.1:")
    depends_on("py-click", type=("build", "run"))
    depends_on("py-flask@3.0.0:", type=("build", "run"), when="@0.19:")
    depends_on("py-hypercorn@0.11.2:", type=("build", "run"))
    depends_on("py-itsdangerous", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-markupsafe", type=("build", "run"), when="@0.17:")
    depends_on("py-werkzeug@3:", type=("build", "run"), when="@0.19:")
    depends_on("py-werkzeug@2:", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"), when="@0.18: ^python@:3.9")
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
    depends_on("py-typing-extensions", type=("build", "run"), when="@0.19: ^python@:3.9")
    depends_on("py-typing-extensions", type=("build", "run"), when="^python@:3.7")

    # Historical dependencies
    depends_on("py-toml", type=("build", "run"), when="@:0.17")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/q/quart/{}-{}.tar.gz"
        if self.spec.satisfies("@:0.18.3"):
            name = "Quart"
        else:
            name = "quart"
        return url.format(name, version)
