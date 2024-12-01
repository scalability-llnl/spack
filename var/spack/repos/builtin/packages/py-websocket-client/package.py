# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWebsocketClient(PythonPackage):
    """WebSocket client for Python. hybi13 is supported."""

    homepage = "https://github.com/websocket-client/websocket-client.git"
    pypi = "websocket-client/websocket-client-0.57.0.tar.gz"

    license("Apache-2.0")

    version("1.8.0", sha256="3239df9f44da632f96012472805d40a23281a991027ce11d2f45a6f24ac4c3da")
    version("1.7.0", sha256="10e511ea3a8c744631d3bd77e61eb17ed09304c413ad42cf6ddfa4c7787e8fe6")
    version("1.6.4", sha256="b3324019b3c28572086c4a319f91d1dcd44e6e11cd340232978c684a7650d0df")
    version("1.6.3", sha256="3aad25d31284266bcfcfd1fd8a743f63282305a364b8d0948a43bd606acc652f")
    version("1.5.1", sha256="3f09e6d8230892547132177f575a4e3e73cfdf06526e20cc02aa1c3b47184d40")
    version("1.4.1", sha256="f9611eb65c8241a67fb373bef040b3cf8ad377a9f6546a12b620b6511e8ea9ef")
    version("1.2.1", sha256="8dfb715d8a992f5712fff8c843adae94e22b22a99b2c5e6b0ec4a1a981cc4e0d")
    version("0.57.0", sha256="d735b91d6d1692a6a181f2a8c9e0238e5f6373356f561bb9dc4c7af36f452010")
    version("0.56.0", sha256="1fd5520878b68b84b5748bb30e592b10d0a91529d5383f74f4964e72b297fd3a")
    version("0.48.0", sha256="18f1170e6a1b5463986739d9fd45c4308b0d025c1b2f9b88788d8f69e8a5eb4a")

    depends_on("python@3.8:", when="@1.6.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Historical dependencies
    depends_on("py-six", type=("build", "run"), when="@:1.2.0")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/w/{0}/{0}-{1}.tar.gz"
        if self.spec.satisfies("@0.59.0:1.7"):
            letter = "websocket-client"
        else:
            letter = "websocket_client"
        return url.format(letter, version)
