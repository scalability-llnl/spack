# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bashtop(Package):
    """Linux resource monitor."""

    homepage = "https://github.com/aristocratos/bashtop"
    url = "https://github.com/aristocratos/bashtop/archive/v0.8.17.tar.gz"

    license("Apache-2.0")

    version("0.8.17", sha256="853a7143de533437cc1654b853bc89da54ff91c629820ac45b7c8708dababf1f")
    version("0.8.16", sha256="6249e5c678fdb0a2a87d6fa13b9fe1f6bd56f7dbcaba0066d2a5275a7f9a9355")
    version("0.8.15", sha256="617aab0a23b1a9430f2ef7d51e4f89eb06c5b3f2ff40768cb6849fc2899ffc6a")
    version("0.8.14", sha256="e2e05a36a8fb3984f256af62f66562c8bd13a901e5f2ef7b7b0056ef40e57543")
    version("0.8.13", sha256="50eda3c91f36a49d7696585fce5b44ba0df53879758f30d94477010bd56c4ff1")
    version("0.8.12", sha256="1e762e40527f454da0f1d050a251a1c288cbbe49645f4ee31aa30afe44e70a0f")
    version("0.8.11", sha256="bf4b3f109819450ee52f42a32d1b46bf2524ae3b1def83fcafba1b8427c71241")
    version("0.8.10", sha256="eac071d68d2ec08869dea696b886bbc0fc33e596e9efa73563e71b4af27c0947")
    version("0.8.9", sha256="af2ba211d3bc1fbe910cd33c447686a6f39c2c731aaba54355b9e66184a0aec1")
    version("0.8.8", sha256="63e88c6f91fdfb3c5265f347e48d7a54a3ad0582407e9adbb70694eb9039ce3f")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bashtop", prefix.bin)
