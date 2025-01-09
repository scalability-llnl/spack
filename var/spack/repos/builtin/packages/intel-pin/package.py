# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class IntelPin(Package):
    """Intel Pin is a dynamic binary instrumentation framework for the IA-32,
    x86-64 and MIC instruction-set architectures that enables the creation of
    dynamic program analysis tools."""

    homepage = "http://www.pintool.org"
    maintainers("matthiasdiener")

    license("MIT")

    version(
        "3.31",
        sha256="82216144e3df768f0203b671ff48605314f13266903eb42dac01b91310eba956",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-external-3.31-98869-gfa6f126a8-gcc-linux.tar.gz",
    )
    version(
        "3.30",
        sha256="be4f1130445c3fc4d83b7afad85c421d418f60013c33e8ee457bc7c9c194de1b",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.30-98830-g1d7b601b3-gcc-linux.tar.gz",
    )
    version(
        "3.29",
        sha256="45c2a68d4b2184117584a55db17b44c86f9476e9cb8109b2fae50a965b1ea64f",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.29-98790-g1a445fcd1-gcc-linux.tar.gz",
    )
    version(
        "3.28",
        sha256="5a5a3337f3f16176b97edcd3366b561936e1068fba4ebcfed4b836d81d45847b",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.28-98749-g6643ecee5-gcc-linux.tar.gz",
    )
    version(
        "3.27",
        sha256="e7d44d25668632007d5a109e5033415e91db543b8ce9e665893a05e852b67707",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.27-98718-gbeaa5d51e-gcc-linux.tar.gz",
    )
    version(
        "3.26",
        sha256="92ef29a2616b63105b8081157c24c50236e34ea6fc13e4a06fe6894bdc700478",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.26-98690-g1fc9d60e6-gcc-linux.tar.gz",
    )
    version(
        "3.25",
        sha256="43c0f441234b0e5cb65caf9714e61d3316f1e4ddf77865731121930a05865fa1",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.25-98650-g8f6168173-gcc-linux.tar.gz",
    )
    version(
        "3.24",
        sha256="0b5183155d86a8aa7cbf7da968fbb37840c48cada94faadb9053489b75d373c8",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.24-98612-g6bd5931f2-gcc-linux.tar.gz",
    )
    version(
        "3.23",
        sha256="996090dfeec7dd58db1babbc3c95f8e4abfcb9b0e1014b02ffdbc09224bb48c0",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.23-98579-gb15ab7903-gcc-linux.tar.gz",
    )
    version(
        "3.22",
        sha256="550fdc15e02d03acc6a65a918887467945b7413089fb1080e238380aad3b95eb",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.22-98547-g7a303a835-gcc-linux.tar.gz",
    )
    version(
        "3.21",
        sha256="a0bd6640d7b4a53f78cf0a2df843b034f2e2ec38e77f018d8e3ef032360b0c5c",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.21-98484-ge7cd811fd-gcc-linux.tar.gz",
    )
    version(
        "3.20",
        sha256="ca2f542eee2013471961bb683d06ccb20ef5dd8ed0d02537cf4d47f09bd616bf",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.20-98437-gf02b61307-gcc-linux.tar.gz",
    )
    version(
        "3.19",
        sha256="3af8a86c229a28ecbabba3180bd6a35e013cc3d44a7496087c15db76fd43f86f",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.19-98425-gd666b2bee-gcc-linux.tar.gz",
    )
    version(
        "3.18",
        sha256="de8ef1a0cb301764a774aa9bcaae8cba997a7dde3155ed271e52d00acceb230b",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.18-98332-gaebd7b1e6-gcc-linux.tar.gz",
    )
    version(
        "3.17",
        sha256="a9cc3df7667b70dd44e51f66ed506bcdc31d942bb7698e1d4e1f8fe5d01c80bb",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.17-98314-g0c048d619-gcc-linux.tar.gz",
    )
    version(
        "3.16",
        sha256="c61abc4a3de48016cdbac9b567630557ec3dfa9b0394cc03ee7ed17d15c791b6",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.16-98275-ge0db48c31-gcc-linux.tar.gz",
    )
    version(
        "3.15",
        sha256="51ab5a381ff477335050b20943133965c5c515d074ad6afb801a898dae8af642",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.15-98253-gb56e429b1-gcc-linux.tar.gz",
    )
    version(
        "3.14",
        sha256="6c3b477c88673e0285fcd866a37a4fa47537d461a8bf48416ae3e9667eb7529b",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.14-98223-gb010a12c6-gcc-linux.tar.gz",
    )
    version(
        "3.13",
        sha256="04a36e91f3f85119c3496f364a8806c82bb675f7536a8ab45344c9890b5e2714",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.13-98189-g60a6ef199-gcc-linux.tar.gz",
    )
    version(
        "3.11",
        sha256="aa5abca475a6e106a75e6ed4ba518fb75a57549a59f00681e6bd6e3f221bd23a",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.11-97998-g7ecce2dac-gcc-linux.tar.gz",
    )
    version(
        "3.10",
        sha256="7c8f14c3a0654bab662b58aba460403138fa44517bd40052501e8e0075b2702a",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.10-97971-gc5e41af74-gcc-linux.tar.gz",
    )
    version(
        "3.7",
        sha256="4730328795be61f1addb0e505a3792a4b4ca80b1b9405acf217beec6b5b90fb8",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.7-97619-g0d0c92f4f-gcc-linux.tar.gz",
    )
    version(
        "2.14",
        sha256="1c29f589515772411a699a82fc4a3156cad95863a29741dfa6522865d4d281a1",
        url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(".", prefix)
        mkdir(prefix.bin)
        symlink(join_path(prefix, "pin"), join_path(prefix.bin, "pin"))
