# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTraitlets(PythonPackage):
    """Traitlets Python config system"""

    homepage = "https://github.com/ipython/traitlets"
    pypi = "traitlets/traitlets-5.0.4.tar.gz"

    version("5.14.3", sha256="9ed0579d3502c94b4b3732ac120375cda96f923114522847de4b3bb98b96b6b7")
    version("5.13.0", sha256="9b232b9430c8f57288c1024b34a8f0251ddcc47268927367a0dd3eeaca40deb5")
    version("5.12.0", sha256="833273bf645d8ce31dcb613c56999e2e055b1ffe6d09168a164bcd91c36d5d35")
    version("5.11.2", sha256="7564b5bf8d38c40fa45498072bf4dc5e8346eb087bbf1e2ae2d8774f6a0f078e")
    version("5.10.1", sha256="db9c4aa58139c3ba850101913915c042bdba86f7c8a0dda1c6f7f92c5da8e542")
    version("5.9.0", sha256="f6cde21a9c68cf756af02035f72d5a723bf607e862e7be33ece505abf4a3bad9")
    version("5.7.1", sha256="fde8f62c05204ead43c2c1b9389cfc85befa7f54acb5da28529d671175bb4108")
    version("5.3.0", sha256="0bb9f1f9f017aa8ec187d8b1b2a7a6626a2a1d877116baba52a129bfa124f8e2")
    version("5.1.1", sha256="059f456c5a7c1c82b98c2e8c799f39c9b8128f6d0d46941ee118daace9eb70c7")
    version("5.0.4", sha256="86c9351f94f95de9db8a04ad8e892da299a088a64fd283f9f6f18770ae5eae1b")
    version("4.3.3", sha256="d023ee369ddd2763310e4c3eae1ff649689440d4ae59d7485eb4cfbbe3e359f7")
    version("4.3.2", sha256="9c4bd2d267b7153df9152698efb1050a5d84982d3384a37b2c1f7723ba3e7835")
    version("4.3.1", sha256="ba8c94323ccbe8fd792e45d8efe8c95d3e0744cc8c085295b607552ab573724c")
    version("4.3.0", sha256="8a33cb7b1ef47f2d6dc16e9cf971217d5a4882a3541c070e78a0e8e8edcb3f82")
    version("4.2.2", sha256="7d7e3070484b2fe490fa55e0acf7023afc5ed9ddabec57405f25c355158e152a")
    version("4.2.1", sha256="76eba33c89723b8fc024f950cacaf5bf2ef37999642cc9a61f4e7c1ca5cf0ac0")
    version("4.2.0", sha256="e4c39210f2f2ff7361b86043b6512adbcf6f024b44b501f7b42fd9a23402dea9")
    version("4.1.0", sha256="440e38dfa5d2a26c086d4b427cfb7aed17d0a2dca78bce90c33354da2592af5b")
    version("4.0.0", sha256="0b140b4a94a4f1951887d9bce4650da211f79600fc9fdb422acc90c5bbe0233b")

    depends_on("py-hatchling@1.5:", when="@5.5:", type="build")
    depends_on("py-hatchling@0.25:", when="@5.2.1.post0:", type="build")
    depends_on("py-setuptools@40.8:", when="@:5.2.1.a", type="build")
    depends_on("py-ipython-genutils", when="@:5.0", type=("build", "run"))
    depends_on("py-six", when="@:4", type=("build", "run"))
    depends_on("py-decorator", when="@:4", type=("build", "run"))
