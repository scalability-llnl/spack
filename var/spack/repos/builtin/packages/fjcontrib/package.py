# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fjcontrib(AutotoolsPackage):
    """3rd party extensions of FastJet"""

    homepage = "https://fastjet.hepforge.org/contrib/"
    url = "https://fastjet.hepforge.org/contrib/downloads/fjcontrib-1.044.tar.gz"

    tags = ["hep"]

    license("GPL-2.0-or-later")

    version("1.054", sha256="1ef922d4c45863e5fe7a3b64dc441703db6b1c2cc92d4160125dc629b05ac331")
    version("1.052", sha256="bde63c28cbdf992bedea4ddedfc3cd52c9fec241a767cc455dd4ad10e8210c39")
    version("1.051", sha256="76a2ec612c768db3eb6bbaf686d02b05ddb64dde477d185e20df563b52308473")
    version("1.045", sha256="667f15556ca371cfaf185086fb41ac579658a233c18fb1e5153382114f9785f8")
    version("1.044", sha256="de3f45c2c1bed6d7567483e4a774575a504de8ddc214678bac7f64e9d2e7e7a7")
    version("1.043", sha256="ef0f586b19ffd12f392b7facc890a73d31fc11b9f5bb727cf3743d6eb59e9993")
    version("1.042", sha256="5b052e93a371c557557fa4a293cca4b08f88ccfb6c43a4df15b2a9f38c6d8831")
    version("1.041", sha256="31e244728de7787a582479cbed606a1c2fe5fcf3ad3ba1b0134742de5107510c")
    version("1.040", sha256="8fcd261f4dec41d3fcf2d550545d7b6e8e5f54e1604615489e7a2c0e45888663")
    version("1.039", sha256="a3b88de5e43edb13cde37ed5821aaed6562eec23a774092547f397b6e0b3f088")
    version("1.038", sha256="e90d079706a0db516cfc1170b4c34aa197320d019d71db1f726764f293561b15")
    version("1.037", sha256="9d69a4a91ef60557e9cebe14952db64f35ea75c51c14e57c1d998bbed0ad6342")
    version("1.036", sha256="ecb93ae43e76dbd485b50d37c234aa039fe455d26c273247bc3c93b273dc24f2")
    version("1.035", sha256="bc33e5c8132258213cf569789cbcfc838dbed1c242bd31decc0be1f099d405b6")
    version("1.034", sha256="8aa9ff609b678c363d682afde91765f7f1145cdf203c18c3fa15c3e1a9a5bcfa")
    version("1.033", sha256="d964370b3db0703e223b42a793b07eafbb3658db1266956fd86e69ea5abab7ea")
    version("1.032", sha256="125bae5ab04384596c4bcde1c84a3189034f1e94fd99b6c1025cfac1c1795831")
    version("1.031", sha256="edb692e8e4e4bbe5401d8891ccf81bd6d26fd7c41d1ec47bd40f2c0e39be9545")
    version("1.030", sha256="e4c47bf808f2c078d6fe332ccff00716fdec618e10b7adbf9344e44c8364dba9")
    version("1.029", sha256="9147f533bf806dbef5c80f38a26f2002f4c8dfe5c2e01ce1c8edfef27ed527ed")
    version("1.028", sha256="cbc24d6e28b03f3c198103c7ae449f401f2e3b7c8a58d241e87f6a8edd30effa")
    version("1.027", sha256="8d983c1622d4163459a67d7208961061699e52e417893c045357cd0d2d6048c4")
    version("1.026", sha256="6bfe538f17fb3fbbf2c0010640ed6eeedfe4317e6b56365e727d44639f76e3d7")
    version("1.025", sha256="504ff45770e8160f1d3b842ea5962c84faeb9acd2821195b08c7e21a84402dcc")
    version("1.024", sha256="be13d4b6dfc3c6a157c521247576d01abaa90413af07a5f13b1d0e3622225116")
    version("1.023", sha256="ca8f5520ab8c934ea4458016f66d4d7b08e25e491f8fdb5393572cd411ddde03")
    version("1.022", sha256="f505c60a87283f380f083736ac411bd865750e81e59876583a9d5c4085d927ce")
    version("1.021", sha256="f4bcd9ca39399a3b7719358e757462ecc7937f73a6b625cbb164173a26847d33")
    version("1.020", sha256="1ec2041cb5e7f050e20823a31111c7e61d24c4d7ee546c9714861b16eca83a04")
    version("1.019", sha256="adec9e1d3c48fec8d6786b64d9c4e95e79129a156f0b0ed3df7e98d57882ffb2")
    version("1.018", sha256="fe9d9661cefba048b19002abec7e75385ed73a8a3f45a29718e110beab142c2c")
    version("1.017", sha256="6f711b8b7f63a9a1bdf83cc1df6f7785bd3394e96dddba12186dfb5de352362c")
    version("1.016", sha256="9301027a71098ef75c37742a2f60631b2e39eb4d6b73b18db48d31e6aed830a0")
    version("1.015", sha256="4b9d56d2b6ae56a894b64920ac9ef59013b1d0a54454e716dd98e724f9ea82c0")
    version("1.014", sha256="c8de7a0cc19be7684dcfbc3101f9cd4c9426daa3009726acd5a5cbe5e699544b")
    version("1.013", sha256="c2b4838a41431cd1c28d3a836f10c00bb84eb6eb2e6586a28badab66518107a6")
    version("1.012", sha256="9215ee5b6465fa64296a0139e727a2eb61255d50faccafaa5b241e408ae54821")
    version("1.011", sha256="7e4e62755d5905e9dc4a6ef29728c03da538cbbff381eed32a35f06934304b1d")
    version("1.010", sha256="1ae74ef44e3d8ce96fd7eb61571819e8891ff708fd468a71780e693c2081176c")
    version("1.009", sha256="dc12cce6f0468b4fab9ec4d9fbb2c3d76e942b3b6965cf609963f65c69c08d2f")
    version("1.008", sha256="8cc98d837b0579b605a4731fb69882084948e1f1d2ee20af5c8adade2434e4ed")
    version("1.007", sha256="70b9d57e5c690d9af8b5be96eefeea9f8c4c4d1a7f000fe1dac30e5aae36077f")
    version("1.006", sha256="e2b6d2c5a666eb4db6bef89ea176df4bc1cdec316f8d18594ab54eb0ce8dcbb6")
    version("1.005", sha256="265e682a05c1f5e5cf1560cc4efa99e07b211cb2add5f3a09b5be4363ab9cc7f")
    version("1.004", sha256="b397e6f822a1d539ac1f63dc8c0709a7a00eed25f4c011114be71f0b38f8f514")
    version("1.003", sha256="79b2d42b1b7a99686fa2e0d95ad39050fd974fdf5ea5066271185ae308299b72")
    version("1.002", sha256="b48d2cc0a9c2fcfe3bb7faee3217a50191be4150a62ed2f6419fd0025d2cec92")
    version("1.001", sha256="6030dfee59040d2ada4ee582254e60b9ecf4b62598129e7b0a114672cf267491")
    version("1.000", sha256="95fa36ae48f03cb941d632b0a537995fb7148a6bd028c4978fab8b7b04332c3b")
    version("0.001", sha256="51f24ad55e28fb1f9d698270602e5077c920fcf58d8ccfd274efbe829d7dd821")
    version("0.000", sha256="9486b11201e6b6e181b8a3abecd929403ae9aa67de0eb8b7353fb82ab4b89f41")

    depends_on("cxx", type="build")  # generated

    depends_on("fastjet")

    build_targets = ["all", "fragile-shared"]
    install_targets = ["install", "fragile-shared-install"]

    def configure_args(self):
        args = [
            "--fastjet-config=" + self.spec["fastjet"].prefix.bin + "/fastjet-config",
            "CXXFLAGS=-O3 -Wall -g " + self.compiler.cxx_pic_flag,
        ]
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            for target in self.build_targets:
                make(target)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            for target in self.install_targets:
                make(target)
