# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bird(AutotoolsPackage):
    """The BIRD project aims to develop a dynamic IP routing daemon with
    full support of all modern routing protocols, easy to use
    configuration interface and powerful route filtering language,
    primarily targeted on (but not limited to) Linux and other UNIX-like
    systems and distributed under the GNU General Public License."""

    homepage = "https://bird.network.cz/"
    url = "https://gitlab.nic.cz/labs/bird/-/archive/v2.0.2/bird-v2.0.2.tar.gz"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("2.15.1", sha256="5a4cf55c4767192aa57880ac5f6763e5b8c26f688ab5934df96e3615c4b0a1e1")
    version("2.15", sha256="485b731ed0668b0da4f5110ba8ea98d248e10b25421820feca5dcdd94ab98a29")
    version("2.14", sha256="22823b20d31096fcfded6773ecc7d9ee6da0339ede805422647c04127c67472f")
    version("2.13.1", sha256="4a55c469f5d2984b62eef929343815b75a7b19132b8c3f40b41f8f66e27d3078")
    version("2.13", sha256="db3df5dd84de98c2a61f8415c9812876578d6ba159038d853b211700e43dbae1")
    version("2.0.12", sha256="70ef51cbf2b7711db484225da5bdf0344ba31629a167148bfe294f61f07573f6")
    version("2.0.11", sha256="a2a1163166def10e014c6f832d6552b00ab46714024613c76cd6ebc3cd3e51c4")
    version("2.0.10", sha256="8e053a64ed3e2c681fcee33ee31e61c7a5df32f94644799f283d294108e83722")
    version("2.0.9", sha256="912d5c1bbefffd6198b10688ef6e16d0b9dfb2886944f481fc38b4d869ffd2c4")
    version("2.0.8", sha256="4d0eeea762dcd4422e1e276e2ed123cfed630cf1cce017b50463d79fcf2fff0c")
    version("2.0.7", sha256="d0c6aeaaef3217d6210261a49751fc662838b55fec92f576e20938917dbf89ab")
    version("2.0.6", sha256="61518120c76bbfe0b52eff614e7580a1d973e66907df5aeac83fe344aa30595a")
    version("2.0.5", sha256="f20dc822fc95aa580759c9b83bfd6c7c2e8504d8d0602cee118db1447054f5d0")
    version("2.0.4", sha256="8c191b87524db3ff587253f46f94524ad2a89efdec8a12c800544a5fb01a2861")
    version("2.0.3", sha256="54ec151518564f87e81de4ac19376689e5ba8dd9129f1e9a79086db3df0931f8")
    version("2.0.2", sha256="e1e9ac92faf5893890c478386fdbd3c391ec2e9b911b1dfccec7b7fa825e9820")
    version("2.0.1", sha256="c222968bb017e6b77d14f4e778f437b84f4ccae686355a3ad8e88799285e7636")

    # fix multiple definitions with extern rta_dest_names
    patch(
        "https://gitlab.nic.cz/labs/bird/-/commit/4bbc10614f3431c37e6352f5a6ea5c693c31021e.diff",
        sha256="ab891b10dab2fa17a3047cd48e082cccc14f958f4255dcae771deab1330da7c8",
        when="@:2.0.7",
    )
    # fix linker errors due to undefined behavior on signals
    patch(
        "https://gitlab.nic.cz/labs/bird/-/commit/24493e9169d3058958ab3ec4d2b02c5753954981.diff",
        sha256="ea49dea1c503836feea127c605b99352b1e353df490d63873af09973cf2b3d14",
        when="@:2.0.6",
    )

    depends_on("c", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("ncurses")
    depends_on("readline")
