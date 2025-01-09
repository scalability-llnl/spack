# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIminuit(PythonPackage):
    """Interactive IPython-Friendly Minimizer based on SEAL Minuit2."""

    homepage = "http://github.com/scikit-hep/iminuit"
    pypi = "iminuit/iminuit-1.2.tar.gz"

    tags = ["hep"]

    license("MIT AND LGPL-2.0-only", checked_by="wdconinc")

    version("2.30.1", sha256="2815bfdeb8e7f78185f316b75e2d4b19d0f6993bdc5ff03352ed37b70a796360")
    version("2.29.1", sha256="474d10eb2f924b9320f6f7093e4c149d0a38c124d0419c12a07a3eca942de025")
    version("2.28.0", sha256="6646ae0b66a4760e02cd73711d460a6cf2375382b78ce8344141751595596aad")
    version("2.27.0", sha256="4ce830667730e76d20b10416a5851672c7fcc301dd1f48b9143cfd187b89ab8e")
    version("2.26.0", sha256="a51233fbf1c2e008aa584f9eea65b6c30ed56624e4dea5d4e53370ccd84c9b4e")
    version("2.25.2", sha256="3bf8a1b96865a60cedf29135f4feae09fa7c66237d29f68ded64e97a823a9b3e")
    version("2.24.0", sha256="25ab631c3c8e024b1bcc7c96f66338caac54a4a2324d55f1e3ba5617816e44fd")
    version("2.23.0", sha256="98f1589eb18d4882232ff1556d62e7ca19c91bbab7524ac8b405261a674452a1")
    version("2.22.0", sha256="e0ccc37bad8bc1bd3b9d3fa07d28d4c0407e25a888faa9b559be2d9afbd2d97c")
    version("2.21.3", sha256="fb313f0cc27e221b9b221bcd779b3a668fb4c77b0f90abfd5336833ecbdac016")
    version("2.20.0", sha256="a73fe6e02f35e3180fc01bc5c1794edf662ff1725c3bc2a4f433567799da7504")
    version("2.19.0", sha256="f4d1cbaccf115cdc4866968f649f2a37794a5c0de018de8156aa74556350a54c")
    version("2.18.0", sha256="7ee2c6a0bcdac581b38fae8d0f343fdee55f91f1f6a6cc9643fcfbcc6c2dc3e6")
    version("2.17.0", sha256="75f4a8a2bad21fda7b6bd42df7ca04120fb24636ebf9b566d259b26f2044b1d0")
    version("2.16.0", sha256="1024a519dbc8fd52d5fd2a3779fd485b09bc27c40556def8b6f91695423199d6")
    version("2.15.2", sha256="60ac7d2fe9405c9206675229273f401611d3f5dfa22942541646c4625b59f1ea")
    version("2.14.0", sha256="5920880d6ec0194411942ab6040a1930398be45669c9f60fff391e666c863417")
    version("2.13.0", sha256="e34785c2a2c0aea6ff86672fe81b80a04ac9d42a79ed8249630f2529a8f6a0fa")
    version("2.12.2", sha256="29142ed38cf986c08683dc9e912a484abc70962a4d36d7d71b7d9d872316be8e")
    version("2.11.2", sha256="8cae7917ca2d22c691e00792bfbbb812b84ac5c75120eb2ae879fb4ada41ee6c")
    version("2.10.0", sha256="93b33ca6d2ffd73e80b40e8a400ca3dbc70e05662f1bd390e2b6040279101485")
    version("2.9.0", sha256="656410ceffead79a52d3d727fdcd2bac78d7774239bef0efc3b7a86bae000ff3")
    version("2.8.4", sha256="4b09189f3094896cfc68596adc95b7f1d92772e1de1424e5dc4dd81def56e8b0")
    version("1.5.2", sha256="0b54f4d4fc3175471398b573d24616ddb8eb7d63808aa370cfc71fc1d636a1fd")
    version("1.3.7", sha256="9173e52cc4a0c0bda13ebfb862f9b074dc5de345b23cb15c1150863aafd8a26c")
    version("1.3.6", sha256="d79a197f305d4708a0e3e52b0a6748c1a6997360d2fbdfd09c022995a6963b5e")
    version("1.2", sha256="7651105fc3f186cfb5742f075ffebcc5088bf7797d8ed124c00977eebe0d1c64")

    depends_on("cxx", type="build")

    depends_on("python@3.6:", type=("build", "run"), when="@2.6.1:")
    depends_on("python@3.7:", type=("build", "run"), when="@2.17.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@2.19.0:")
    depends_on("python@3.9:", type=("build", "run"), when="@2.28.0:")
    with when("@2.22:"):
        depends_on("py-scikit-build-core@0.3:+pyproject", type="build")
        depends_on("py-scikit-build-core@0.5:+pyproject", type="build", when="@2.26:")
        depends_on("py-pybind11", type="build")
        depends_on("py-pybind11@2.12:", type="build", when="@2.26:")
    with when("@:2.21"):
        depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"), when="@1.3:1.3.6")
    depends_on("py-numpy@1.11.3:", type=("build", "run"), when="@1.3.7:")
    # https://github.com/numpy/numpy/issues/26191#issuecomment-2179127999
    depends_on("py-numpy@1.21:", type=("build", "run"), when="@2.22:")
    depends_on("py-numpy@:1", when="@:2.25", type=("build", "run"))
    depends_on("cmake@3.11:", type="build")
    depends_on("cmake@3.13:", type="build", when="@2:")
    depends_on("cmake@3.15:", type="build", when="@2.22:")

    # Historical dependencies
    with when("@:2.27"):
        depends_on("py-typing-extensions", when="@2.21: ^python@:3.8", type=("build", "run"))
        depends_on(
            "py-typing-extensions@3.7.4:", when="@2.26: ^python@:3.8", type=("build", "run")
        )
