# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParamiko(PythonPackage):
    """SSH2 protocol library"""

    homepage = "https://www.paramiko.org/"
    pypi = "paramiko/paramiko-2.7.1.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.4.0", sha256="aac08f26a31dc4dffd92821527d1682d99d52f9ef6851968114a8728f3c274d3")
    version("3.3.1", sha256="6a3777a961ac86dbef375c5f5b8d50014a1a96d0fd7f054a43bc880134b0ff77")
    version("3.3.0", sha256="ef639f5b97cf7bde57b6e1706e85b7e3f5561f632e180c6c155f53560ff1701b")
    version("3.2.0", sha256="93cdce625a8a1dc12204439d45033f3261bdb2c201648cfcdc06f9fd0f94ec29")
    version("3.1.0", sha256="6950faca6819acd3219d4ae694a23c7a87ee38d084f70c1724b0c0dbb8b75769")
    version("3.0.0", sha256="fedc9b1dd43bc1d45f67f1ceca10bc336605427a46dcdf8dec6bfea3edf57965")
    version("2.12.0", sha256="376885c05c5d6aa6e1f4608aac2a6b5b0548b1add40274477324605903d9cd49")
    version("2.9.2", sha256="944a9e5dbdd413ab6c7951ea46b0ab40713235a9c4c5ca81cfe45c6f14fa677b")
    version("2.7.1", sha256="920492895db8013f6cc0179293147f830b8c7b21fdfc839b6bad760c27459d9f")
    version("2.1.2", sha256="5fae49bed35e2e3d45c4f7b0db2d38b9ca626312d91119b3991d0ecf8125e310")

    variant("invoke", default=False, description="Enable invoke support")

    depends_on("py-setuptools", type="build")
    depends_on("py-bcrypt@3.1.3:", when="@2.7:", type=("build", "run"))
    depends_on("py-bcrypt@3.2:", when="@3:", type=("build", "run"))
    depends_on("py-cryptography@1.1:", type=("build", "run"))
    depends_on("py-cryptography@2.5:", when="@2.7:", type=("build", "run"))
    depends_on("py-cryptography@3.3:", when="@3:", type=("build", "run"))
    depends_on("py-pyasn1@0.1.7:", when="@:2.1", type=("build", "run"))
    depends_on("py-pynacl@1.0.1:", when="@2.7:", type=("build", "run"))
    depends_on("py-pynacl@1.5:", when="@3:", type=("build", "run"))
    depends_on("py-six", when="@2.9.3:2", type=("build", "run"))

    depends_on("py-invoke@1.3:", when="+invoke", type=("build", "run"))
    depends_on("py-invoke@2:", when="@3: +invoke", type=("build", "run"))
    conflicts("+invoke", when="@2.1.2")
