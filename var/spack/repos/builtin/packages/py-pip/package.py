# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

from spack.package import *


class PyPip(Package, PythonExtension):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pip.pypa.io/"
    url = "https://files.pythonhosted.org/packages/py3/p/pip/pip-20.2-py3-none-any.whl"
    list_url = "https://pypi.org/simple/pip/"

    # Requires railroad
    skip_modules = ["pip._vendor"]

    tags = ["build-tools"]

    maintainers("adamjstewart", "pradyunsg")

    license("MIT")

    version("23.1.2", sha256="3ef6ac33239e4027d9a5598a381b9d30880a1477e50039db2eac6e8a8f6d1b18")
    version("23.0", sha256="b5f88adff801f5ef052bcdef3daa31b55eb67b0fccd6d0106c206fa248e0463c")
    version("22.2.2", sha256="b61a374b5bc40a6e982426aede40c9b5a08ff20e640f5b56977f4f91fed1e39a")
    version("22.1.2", sha256="a3edacb89022ef5258bf61852728bf866632a394da837ca49eb4303635835f17")
    version("21.3.1", sha256="deaf32dcd9ab821e359cd8330786bcd077604b5c5730c0b096eda46f95c24a2d")
    version("21.1.2", sha256="f8ea1baa693b61c8ad1c1d8715e59ab2b93cd3c4769bacab84afcc4279e7a70e")
    version("20.2", sha256="d75f1fc98262dabf74656245c509213a5d0f52137e40e8f8ed5cc256ddd02923")
    version("19.3", sha256="e100a7eccf085f0720b4478d3bb838e1c179b1e128ec01c0403f84e86e0e2dfb")
    version("19.1.1", sha256="993134f0475471b91452ca029d4390dc8f298ac63a712814f101cd1b6db46676")
    version("19.0.3", sha256="bd812612bbd8ba84159d9ddc0266b7fbce712fc9bc98c82dee5750546ec8ec64")
    version("18.1", sha256="7909d0a0932e88ea53a7014dfd14522ffef91a464daaaf5c573343852ef98550")
    version("10.0.1", sha256="717cdffb2833be8409433a93746744b59505f42146e8d37de6c62b430e25d6d7")
    version("9.0.1", sha256="690b762c0a8460c303c089d5d0be034fb15a5ea2b75bdf565f40421f542fefb0")

    extends("python")
    depends_on("python@3.7:", when="@22:", type=("build", "run"))

    # Uses collections.MutableMapping
    depends_on("python@:3.9", when="@:19.1", type=("build", "run"))

    resource(
        name="pip-bootstrap",
        url="https://bootstrap.pypa.io/pip/zipapp/pip-22.3.1.pyz",
        checksum="c9363c70ad91d463f9492a8a2c89f60068f86b0239bd2a6aa77367aab5fefb3e",
        when="platform=windows ^python@:3.11",
        placement={"pip-22.3.1.pyz": "pip.pyz"},
        expand=False,
    )

    resource(
        name="pip-bootstrap",
        url="https://bootstrap.pypa.io/pip/zipapp/pip-23.1.pyz",
        checksum="d9f2fe58c472f9107964df35954f8b74e68c307497a12364b00dc28f36f96816",
        when="platform=windows ^python@3.12:",
        placement={"pip-23.1.pyz": "pip.pyz"},
        expand=False,
    )

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/p/pip/pip-{1}-{0}-none-any.whl"
        if version >= Version("21"):
            python_tag = "py3"
        else:
            python_tag = "py2.py3"
        return url.format(python_tag, version)

    def install(self, spec, prefix):
        # To build and install pip from source, you need setuptools, wheel, and pip
        # already installed. We get around this by using a pre-built wheel to install
        # itself, see:
        # https://discuss.python.org/t/bootstrapping-a-specific-version-of-pip/12306
        whl = self.stage.archive_file
        args = std_pip_args + ["--prefix=" + prefix, whl]
        if sys.platform == "win32":
            # On Windows for newer versions of pip, you must bootstrap pip first.
            # In order to achieve this, use the pip.pyz zipapp version of pip to
            # bootstrap the pip wheel install.
            args.insert(0, os.path.join(self.stage.source_path, "pip.pyz"))
        else:
            args.insert(0, os.path.join(whl, "pip"))
        python(*args)

    def setup_dependent_package(self, module, dependent_spec: Spec):
        setattr(module, "pip", python.with_default_args("-m", "pip"))
