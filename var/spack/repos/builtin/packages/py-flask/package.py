# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlask(PythonPackage):
    """A simple framework for building complex web applications."""

    homepage = "https://palletsprojects.com/p/flask/"
    pypi = "flask/flask-3.0.3.tar.gz"
    git = "https://github.com/pallets/flask.git"

    license("BSD-3-Clause")

    version("3.0.3", sha256="ceb27b0af3823ea2737928a4d99d125a06175b8512c445cbd9a9ce200ef76842")
    version("2.3.2", sha256="8c2f9abd47a9e8df7f0c3f091ce9497d011dc3b31effcf4c85a6e2b50f4114ef")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-30861
        version("2.2.2", sha256="642c450d19c4ad482f96729bd2a8f6d32554aa1e231f4f6b4e7e5264b16cca2b")
        version("2.0.2", sha256="7b2fb8e934ddd50731893bdcdb00fc8c0315916f9fcd50d22c7cc1a95ab634e2")
        version("1.1.2", sha256="4efa1ae2d7c9865af48986de8aeb8504bf32c7f3d6fdc9353d34b21f4b127060")
        version("1.1.1", sha256="13f9f196f330c7c2c5d7a5cf91af894110ca0215ac051b5844701f2bfd934d52")
        version(
            "0.12.4", sha256="2ea22336f6d388b4b242bc3abf8a01244a8aa3e236e7407469ef78c16ba355dd"
        )
        version(
            "0.12.2", sha256="49f44461237b69ecd901cc7ce66feea0319b9158743dd27a2899962ab214dac1"
        )
        version(
            "0.12.1", sha256="9dce4b6bfbb5b062181d3f7da8f727ff70c1156cbb4024351eafd426deb5fb88"
        )
        version(
            "0.11.1", sha256="b4713f2bfb9ebc2966b8a49903ae0d3984781d5c878591cf2f7b484d28756b0e"
        )

    depends_on("python@3.8:", when="@2.3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"), when="@:2")
    depends_on("py-flit-core@:3", type=("build", "run"), when="@3:")

    depends_on("py-werkzeug@3:", when="@3:", type=("build", "run"))
    depends_on("py-werkzeug@2.3.3:", when="@2.3.2:", type=("build", "run"))
    depends_on("py-werkzeug@2.2.2:", when="@2.2.2:", type=("build", "run"))
    depends_on("py-werkzeug@2:", when="@2:", type=("build", "run"))
    depends_on("py-werkzeug@0.15:", type=("build", "run"))
    depends_on("py-jinja2@3.1.2:", when="@3:", type=("build", "run"))
    depends_on("py-jinja2@3:", when="@2:", type=("build", "run"))
    depends_on("py-jinja2@2.10.1:", type=("build", "run"))
    depends_on("py-itsdangerous@2.1.2:", when="@3:", type=("build", "run"))
    depends_on("py-itsdangerous@2:", when="@2:", type=("build", "run"))
    depends_on("py-itsdangerous@0.24:", type=("build", "run"))
    depends_on("py-click@8.1.3:", when="@3:", type=("build", "run"))
    depends_on("py-click@8:", when="@2.1:", type=("build", "run"))
    depends_on("py-click@7.1.2:", when="@2:", type=("build", "run"))
    depends_on("py-click@5.1:", type=("build", "run"))
    depends_on("py-blinker@1.6.2:", when="@2.3:", type=("build", "run"))
    depends_on("py-importlib-metadata@3.6:", when="@2.1: ^python@:3.9", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/f/flask/{}-{}.tar.gz"
        if self.spec.satisfies("@:0.18.3"):
            name = "Flask"
        else:
            name = "flask"
        return url.format(name, version)
