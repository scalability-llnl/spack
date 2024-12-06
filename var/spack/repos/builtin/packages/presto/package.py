# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Presto(MavenPackage):
    """Presto is a distributed SQL query engine for big data."""

    homepage = "https://prestodb.io/"
    url = "https://github.com/prestodb/presto/archive/0.239.tar.gz"

    license("Apache-2.0")

    version("0.239", sha256="cff738eecf9e4e0bb58a9b0366053a328c4ac4e72d3e8209e8c654f6e1b8985f")
    version("0.238.2", sha256="cb79311cb27695e00108c84c6e135c0b1f8ffb631013c2b25ed8565f9cf1b71f")
    version("0.238.1", sha256="4b811af887fc2dd38cfa36355d6a47c234a600f51e908dc9b59e24a5407b3620")
    version("0.238", sha256="89733c79eac750d401007bc4d1eb2d61aba725b3eaaa3421782443553799e7c9")
    version("0.237.2", sha256="3547328e1757956f8c46d4f5ad12d903f71da1ffed41bb39e6f24c4d4b056040")
    version("0.237.1", sha256="c613c04ef97cf90eb390379cc6efa9ec65aac41a3d8f4863f9567597c6a2ec21")
    version("0.237", sha256="4a19b384eb6bd8ecb020a18b8fa8f6f2105489d1891a2909f53f4e2c20c12699")
    version("0.236.1", sha256="571c74c0b84ee515750c129eb5de1fbac09cd4d028943d9df99c8e89909c83f4")
    version("0.236", sha256="6d4c1d79216d2530b64a7737a54c35e698ca738e42d77d086f036224b42b508e")
    version("0.235.1", sha256="1353b2b8526bc2a365f70e9af7005e294cfff11d53285279b2f67048bb5511a0")
