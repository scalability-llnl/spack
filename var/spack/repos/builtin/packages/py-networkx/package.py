# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetworkx(PythonPackage):
    """NetworkX is a Python package for the creation, manipulation, and study
    of the structure, dynamics, and functions of complex networks."""

    homepage = "https://networkx.github.io/"
    pypi = "networkx/networkx-2.4.tar.gz"
    git = "https://github.com/networkx/networkx.git"

    license("BSD-3-Clause")

    version("3.1", sha256="de346335408f84de0eada6ff9fafafff9bcda11f0a0dfaa931133debb146ab61")
    version("3.0", sha256="9a9992345353618ae98339c2b63d8201c381c2944f38a2ab49cb45a4c667e412")
    version("2.8.6", sha256="bd2b7730300860cbd2dafe8e5af89ff5c9a65c3975b352799d87a6238b4301a6")
    version("2.7.1", sha256="d1194ba753e5eed07cdecd1d23c5cd7a3c772099bd8dbd2fea366788cf4de7ba")
    version("2.6.3", sha256="c0946ed31d71f1b732b5aaa6da5a0388a345019af232ce2f49c766e2d6795c51")
    version("2.5.1", sha256="109cd585cac41297f71103c3c42ac6ef7379f29788eb54cb751be5a663bb235a")
    version("2.5", sha256="7978955423fbc9639c10498878be59caf99b44dc304c2286162fd24b458c1602")
    version("2.4", sha256="f8f4ff0b6f96e4f9b16af6b84622597b5334bf9cae8cf9b2e42e7985d5c95c64")
    version("2.3", sha256="8311ddef63cf5c5c5e7c1d0212dd141d9a1fe3f474915281b73597ed5f1d4e3d")
    version("2.2", sha256="45e56f7ab6fe81652fb4bc9f44faddb0e9025f469f602df14e3b2551c2ea5c8b")
    version("2.1", sha256="64272ca418972b70a196cb15d9c85a5a6041f09a2f32e0d30c0255f25d458bb1")
    version("2.0", sha256="cd5ff8f75d92c79237f067e2f0876824645d37f017cfffa5b7c9678cae1454aa")
    version("1.11", sha256="0d0e70e10dfb47601cbb3425a00e03e2a2e97477be6f80638fef91d54dd1e4b8")
    version("1.10", sha256="ced4095ab83b7451cec1172183eff419ed32e21397ea4e1971d92a5808ed6fb8")

    variant("default", default=True, description="Enable installation of default dependencies.")

    # variant would be available for earlier versions as well, but then the
    # dependencies increase a lot
    variant(
        "extra",
        default=False,
        when="@2.5:",
        description="Optional requirements that may require extra steps to install",
    )

    depends_on("python@3.8:", when="@2.7:", type=("build", "run"))
    depends_on("python@3.7:", when="@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    with when("+default"):
        # From requirements/default.txt
        depends_on("py-numpy@1.20:", when="@3:", type=("build", "run"))
        depends_on("py-numpy@1.19:", when="@2.8.6:", type=("build", "run"))
        # https://github.com/networkx/networkx/pull/7390
        depends_on("py-numpy@:1", when="@:3.2", type=("build", "run"))
        depends_on("py-scipy@1.8:", when="@2.8.6:", type=("build", "run"))
        depends_on("py-matplotlib@3.4:", when="@2.8.6:", type=("build", "run"))
        depends_on("py-pandas@1.3:", when="@2.8.6:", type=("build", "run"))

        # Historical dependencies
        depends_on("py-decorator@4.3.0:4", when="@2.5.1:2.5", type=("build", "run"))
        depends_on("py-decorator@4.3.0:", when="@2.2:2.4", type=("build", "run"))
        depends_on("py-decorator@4.1.0:", when="@2.0:2.1", type=("build", "run"))
        depends_on("py-decorator@3.4.0:", when="@:1", type=("build", "run"))

    with when("+extra"):
        # From requirements/extra.txt
        depends_on("py-lxml@4.6:", when="@2.7:", type=("build", "run"))
        depends_on("py-lxml@4.5:", when="@2.6:", type=("build", "run"))
        depends_on("py-pygraphviz@1.10:", when="@3:", type=("build", "run"))
        depends_on("py-pygraphviz@1.9:", when="@2.7:", type=("build", "run"))
        depends_on("py-pygraphviz@1.7:", when="@2.6:", type=("build", "run"))
        depends_on("py-pygraphviz@1.5:1", type=("build", "run"))
        depends_on("py-pydot@1.4.2:", when="@2.7:", type=("build", "run"))
        depends_on("py-pydot@1.4.1:", type=("build", "run"))
        depends_on("py-sympy@1.10:", when="@2.8:", type=("build", "run"))

    def url_for_version(self, version):
        ext = "tar.gz"
        if Version("2.0") <= version <= Version("2.3"):
            ext = "zip"

        url = "https://pypi.io/packages/source/n/networkx/networkx-{0}.{1}"
        return url.format(version, ext)
