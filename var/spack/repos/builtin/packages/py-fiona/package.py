# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFiona(PythonPackage):
    """Fiona reads and writes spatial data files."""

    homepage = "https://github.com/Toblerity/Fiona"
    pypi = "fiona/fiona-1.9.5.tar.gz"
    git = "https://github.com/Toblerity/Fiona.git"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.10.1", sha256="b00ae357669460c6491caba29c2022ff0acfcbde86a95361ea8ff5cd14a86b68")
    version("1.10.0", sha256="3529fd46d269ff3f70aeb9316a93ae95cf2f87d7e148a8ff0d68532bf81ff7ae")
    version("1.9.6", sha256="791b3494f8b218c06ea56f892bd6ba893dfa23525347761d066fb7738acda3b1")
    version("1.9.5", sha256="99e2604332caa7692855c2ae6ed91e1fffdf9b59449aa8032dd18e070e59a2f7")
    version("1.9.4", sha256="49f18cbcd3b1f97128c1bb038c3451b2e1be25baa52f02ce906c25cf75af95b6")
    version("1.9.3", sha256="60f3789ad9633c3a26acf7cbe39e82e3c7a12562c59af1d599fc3e4e8f7f8f25")
    version("1.9.2", sha256="f9263c5f97206bf2eb2c010d52e8ffc54e96886b0e698badde25ff109b32952a")
    version("1.9.1", sha256="3a3725e94840a387fef48726d60db6a6791563f366939d22378a4661f8941be7")
    version("1.9.0", sha256="6e487cbfba5a849fbdf06e45169fd7e1f1662f44f3d717ab4b946046b2457eae")
    version("1.8.22", sha256="a82a99ce9b3e7825740157c45c9fb2259d4e92f0a886aaac25f0db40ffe1eea3")
    version("1.8.21", sha256="3a0edca2a7a070db405d71187214a43d2333a57b4097544a3fcc282066a58bfc")
    version("1.8.20", sha256="a70502d2857b82f749c09cb0dea3726787747933a2a1599b5ab787d74e3c143b")
    version("1.8.18", sha256="b732ece0ff8886a29c439723a3e1fc382718804bb057519d537a81308854967a")

    with default_args(type=("build", "link", "run")):
        depends_on("python@:3.10", when="@1.8.21")
        depends_on("python@:3.9", when="@:1.8.20")

        # setup.py or release notes
        depends_on("gdal@3.4:", when="@1.10:")
        depends_on("gdal@3.1:", when="@1.9:")
        depends_on("gdal@1.8:")

    with default_args(type="build"):
        depends_on("py-setuptools@67.8:", when="@1.9.5:")
        depends_on("py-setuptools@61:", when="@1.9:")
        depends_on("py-cython@3.0.2:3", when="@1.9.5:")
        depends_on("py-cython@0.29.29:0.29", when="@1.9.0:1.9.4")
        depends_on("py-cython")

    with default_args(type=("build", "run")):
        depends_on("py-attrs@19.2:", when="@1.9:")
        depends_on("py-attrs@17:")
        depends_on("py-certifi")
        depends_on("py-click@8", when="@1.9:")
        depends_on("py-click@4:")
        depends_on("py-click-plugins@1:")
        depends_on("py-cligj@0.5:")
        depends_on("py-importlib-metadata", when="@1.9.2: ^python@:3.9")

        # Historical dependencies
        depends_on("py-munch@2.3.2:", when="@1.9.0:1.9.3")
        depends_on("py-munch", when="@:1.8")
        depends_on("py-setuptools", when="@:1.9.1,1.9.5")
        depends_on("py-six", when="@1.9.4:1.9")
        depends_on("py-six@1.7:", when="@:1.8")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/{0}/{0}iona/{0}iona-{1}.tar.gz"
        if version >= Version("1.9.5"):
            letter = "f"
        else:
            letter = "F"
        return url.format(letter, version)
