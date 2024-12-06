# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Druid(MavenPackage):
    """Druid is one of the best database connection pools
    written in JAVA. Druid provides powerful monitoring
    functionalities and more."""

    homepage = "https://github.com/alibaba/druid/"
    url = "https://github.com/alibaba/druid/archive/1.1.23.tar.gz"

    license("Apache-2.0")

    version("1.2.8", sha256="e7e3726ea6d16f98bcf027eaa8591078827d249830ff3b3ba6579d70735d0003")
    version("1.1.23", sha256="f29a0c5e60eb8a4d6fcfdf21bb4b6f54c1076a214f65190b8cdce2663cf84432")
    version("1.1.22", sha256="0bd64e518beca840cd2f79bbfa612f47defbb3366333a11cff937af4424f96ce")
    version("1.1.21", sha256="c0dae665c9fffd991dd9b9880cb69fa48f6b04608b395f380c93f59df599423e")
    version("1.1.20", sha256="2c3210482e4bde425fd758630a8ce4fdd58a1f87dff0af4b3b38fb2b5eb4521e")
    version("1.1.19", sha256="5987b9373232a9e2c1ed88d1cf9ab062b11c83440624aa470dfe5b44873029f6")
    version("1.1.18", sha256="944e0bb51d252fcb298961f51d8e9895710e48b345001095c6aca2577cb95c51")
    version("1.1.16", sha256="befe0229c47258ebf0d6256d6e74cfcc99de14533ab5c6b4eff6089e258a4219")
    version("1.1.14", sha256="236d3548d63afbe2321db55144a41d7369ed09c7e16411302a6a3d2730605ce9")

    depends_on("java@8", type=("build", "run"))
