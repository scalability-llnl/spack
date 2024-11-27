# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBlessed(PythonPackage):
    """Blessed is a thin, practical wrapper around terminal capabilities in
    Python."""

    homepage = "https://github.com/jquast/blessed"
    pypi = "blessed/blessed-1.15.0.tar.gz"

    license("MIT")

    version("1.19.0", sha256="4db0f94e5761aea330b528e84a250027ffe996b5a94bf03e502600c9a5ad7a61")
    version("1.18.1", sha256="8b09936def6bc06583db99b65636b980075733e13550cb6af262ce724a55da23")
    version("1.18.0", sha256="1312879f971330a1b7f2c6341f2ae7e2cbac244bfc9d0ecfbbecd4b0293bc755")
    version("1.17.12", sha256="580429e7e0c6f6a42ea81b0ae5a4993b6205c6ccbb635d034b4277af8175753e")
    version("1.17.11", sha256="7d4914079a6e8e14fbe080dcaf14dee596a088057cdc598561080e3266123b48")
    version("1.17.10", sha256="58b9464609f54e2eca5f5926db590a5b01fefef882844ce05064f483b8f96c26")
    version("1.17.9", sha256="0d497a5be8a808b7300c00bf8303e7ba9fd11f6063a67bb924a475e5bfa7a9bb")
    version("1.17.8", sha256="7671d057b2df6ddbefd809009fb08feb2f8d2d163d240b5e765088a90519b2f1")
    version("1.17.7", sha256="0329a3d1db91328986a6dfd36475dbc498c867090f0433cdcc1a45a5eb2067e4")
    version("1.17.6", sha256="a9a774fc6eda05248735b0d86e866d640ca2fef26038878f7e4d23f7749a1e40")
    version("1.17.5", sha256="926916492220af741657ec4668aba95f54a8c32445e765cfa38c7ccd3343cc6f")
    version("1.17.4", sha256="320a619c83298a9c9d632dbd8fafbb90ba9a38b83c7e64726c572fb186dd0781")
    version("1.17.3", sha256="cc38547175ae0a3a3d4e5dcc7e7478a5a6bf0a6b5f4d9c6b2e5eadbe4475cb0e")
    version("1.17.0", sha256="38632d60dd384de9e9be0ee5b6e1c6130f96efd0767c6ca530a453da36238c25")
    version("1.16.1", sha256="a222783b09f266cf76f5a01f4dfd9de79650f07cbefe2cbc67ec7bb9577c1dfa")
    version("1.16.0", sha256="34b78e9b56c2ba2f6a9a625cc989d6cf4ae8ae87dcc4ed8ad144660ae4cf7784")
    version("1.15.0", sha256="777b0b6b5ce51f3832e498c22bc6a093b6b5f99148c7cbf866d26e2dec51ef21")

    depends_on("py-setuptools", type="build")
    depends_on("py-wcwidth@0.1.4:", type=("build", "run"))
    depends_on("py-six@1.9.0:", type=("build", "run"))
