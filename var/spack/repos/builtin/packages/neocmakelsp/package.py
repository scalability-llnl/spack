# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Neocmakelsp(CargoPackage):
    """Another cmake lsp"""

    homepage = "https://neocmakelsp.github.io/"
    url = "https://github.com/neocmakelsp/neocmakelsp/archive/refs/tags/v0.8.6.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("0.8.6", sha256="4ed270190eb08f5571da036fb0f91d53c1c3e09bf4631f77f2133d56fd8e2437")
    version("0.8.5", sha256="3f3cb8736468bd0a9e9199b6913ae8b6f323d6ecdab932ba1da16a091a8b0de1")
    version("0.8.4", sha256="cf395c16d14d16ad54deda0fc6d2e9f1160163417c716ad18030e611947f9600")
    version("0.8.3", sha256="b679394030b670ed57be3b75c9818ef5ee4fa2eb2b8e7bd16a1e254feccd1a0e")
    version("0.8.2", sha256="f463d20a28735bf131449f9e5ba790d24ee11badc6f017c3b99f803200c50f8c")
    version("0.8.1", sha256="23d2fd6f6bd0152dad9b6bdf9b5d6932d97ccd106bfb47d6d6fee563ea5a7eec")
    version("0.8.0", sha256="7fbe5501d36885e7a93b8d2122eb8506e6fa7d75d43718f0ee0fab09bc7ee5e8")
    version("0.7.9", sha256="d1b6219e19f1ab630fbcb6d3179fcac5dc8dca1b7af355bb7516bc4345ce461b")
    version("0.7.8", sha256="1026ab9f7c60b2c9f880df12830f2927b28b50a06bb5732d5047aefe22fa9b2f")
    version("0.7.7", sha256="9c761a54ae8a6b298eabc9b7cb215fceafd27e9193eb61e1d69cd7a5dc6dd1c1")
