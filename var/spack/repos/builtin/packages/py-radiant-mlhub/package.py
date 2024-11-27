# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadiantMlhub(PythonPackage):
    """A Python client for Radiant MLHub."""

    homepage = "https://github.com/radiantearth/radiant-mlhub"
    pypi = "radiant-mlhub/radiant_mlhub-0.2.1.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("0.5.5", sha256="93cabc3c8e9ba343cdb3b0bfaec01bf7a36aae75704fabfe96c8bf5cab9fa899")
    version("0.5.3", sha256="f111983910e41f2ce40bf401ccf9e33b393e52cc1989f8f8b74c6b4e2bdd0127")
    version("0.5.2", sha256="d310afce962508a44c60f5738fef164c50e78f76c3e85813653824b39a189ca3")
    version("0.5.1", sha256="b7daff4a127e96e27c64eda66e393d9727e61a87c887f86738753486cc44fa46")
    version("0.5.0", sha256="fff788aaa5f8afcb0f6eabff4147eaaf7de375f0a43ecaf2238033fc3a62e2c2")
    version("0.4.1", sha256="1d95475ec9d4cf460d5201425ba843523b1885a9384b9c1adb81a4a1088adb0f")
    version("0.4.0", sha256="0208881601216f895a1c084a3ca9e5c46b09dbc09dca0447540192e4abb847b1")
    version("0.3.1", sha256="3a5a8e971132d5b4cd9e412c7f6d87894fc588655ae0e93006646927b1ecb902")
    version("0.3.0", sha256="dd66479f12317e7bf366abe8d692841485e9497918c30ab14cd6db9e69ce3dbb")
    version("0.2.2", sha256="0d9f634b7e29c7f7294b81a10cf712ac63251949a9c5a07aa6c64c0d5b77e1ba")
    version("0.2.1", sha256="75a2f096b09a87191238fe557dc64dda8c44156351b4026c784c848c7d84b6fb")
    version("0.2.0", sha256="4a3e4c301c5e74f282bbf77b7d65db5a1d6c2a4dc6d18637eff6e1228ca2eb9d")

    depends_on("python@3.8:", when="@0.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click@7.1.2:8", when="@0.3:", type=("build", "run"))
    depends_on("py-click@7.1.2:7.1", when="@:0.2", type=("build", "run"))
    depends_on("py-pydantic@1.9.2:1.9", when="@0.5.2:", type=("build", "run"))
    depends_on("py-pydantic@1.9:1", when="@0.5.0:0.5.1", type=("build", "run"))
    depends_on("py-pystac@1.4", when="@0.5.2:", type=("build", "run"))
    depends_on("py-pystac@1.4:1", when="@0.5.0:0.5.1", type=("build", "run"))
    depends_on("py-pystac@1.1:1", when="@0.3:0.4", type=("build", "run"))
    depends_on("py-pystac@0.5.4", when="@:0.2", type=("build", "run"))
    depends_on("py-python-dateutil@2.8.2:2.8", when="@0.5.2:", type=("build", "run"))
    depends_on("py-python-dateutil@2.8:2", when="@0.5.0:0.5.1", type=("build", "run"))
    depends_on("py-requests@2.27", when="@0.5.2:", type=("build", "run"))
    depends_on("py-requests@2.27:2", when="@0.5.0:0.5.1", type=("build", "run"))
    depends_on("py-requests@2.25:2", when="@0.3:0.4", type=("build", "run"))
    depends_on("py-requests@2.25.1:2.25", when="@:0.2", type=("build", "run"))
    depends_on("py-shapely@1.8", when="@0.5.2:", type=("build", "run"))
    depends_on("py-shapely@1.8:1", when="@0.5.0:0.5.1", type=("build", "run"))
    depends_on("py-tqdm@4.64", when="@0.5.2:", type=("build", "run"))
    depends_on("py-tqdm@4.64:4", when="@0.5.0:0.5.1", type=("build", "run"))
    depends_on("py-tqdm@4.56:4", when="@0.3:0.4", type=("build", "run"))
    depends_on("py-tqdm@4.56", when="@:0.2", type=("build", "run"))
    depends_on("py-urllib3@1.26.11:1.26", when="@0.5.5:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-typing-extensions@3.7:", when="@0.3:0.4 ^python@:3.7", type=("build", "run"))
