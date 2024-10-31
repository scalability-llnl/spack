# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Yoda(AutotoolsPackage):
    """YODA - Yet more Objects for Data Analysis"""

    homepage = "https://yoda.hepforge.org/"
    url = "https://yoda.hepforge.org/downloads/?f=YODA-1.8.3.tar.bz2"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    version("2.0.0", sha256="680f43dabebb3167ce1c5dee72d1c2c285c3190751245aa51e3260a005a99575")
    version(
        "1.9.10",
        sha256="0a708ee9d704945d3387cc437b15ffddf382c70fe5bab39ed2bdbf83c2c28c6f",
        preferred=True,
    )
    version("1.9.9", sha256="ebcad55369a1cedcee3a2de059407c851652ba44495113f5c09d8c2e57f516aa")
    version("1.9.8", sha256="7bc3062468abba50aff3ecb8b22ce677196036009890688ef4533aaa7f92e6e4")
    version("1.9.7", sha256="8d07bb04dcb79364858718a18203452d8d9fa00029fa94239eafa8529032b8ff")
    version("1.9.6", sha256="21523fa2f6b6c8f3348959f3a948734a930ca25951d3c9190b4424e13735f2a4")
    version("1.9.5", sha256="59191a0e9afa8db53ffaa2079f8532e5b13de1be622703d6f7060d3610528b6b")
    version("1.9.0", sha256="9a55de12ffebbe41d1704459c5c9289eeaf0f0eb6a4d0104ea222d7ab889fdf4")
    version("1.8.5", sha256="4c2e6b8571fc176271515a309b45687a2981af1b07ff3f00d0b035a597aa32fd")
    version("1.8.4", sha256="9d24a41c9b7cc6eb14cab0a48f65d2fca7ec9d794afe0922ceb158d0153c150e")
    version("1.8.3", sha256="d9dd0ea5e0f630cdf4893c09a40c78bd44455777c2125385ecc26fa9a2acba8a")
    version("1.8.2", sha256="89558c11cf9b88b0899713e5b4bf8781fdcecc480ff155985ebbf148c6d80bdb")
    version("1.8.1", sha256="51472e12065b9469f13906f0dc609e036d0c1dbd2a8e445e7d654aba73660112")
    version("1.8.0", sha256="82c62bbaedb4b6b7d50cd42ce5409d453d46c1cc6724047db5efa74d34dd6dc5")
    version("1.7.7", sha256="cfb64b099a79ec4d138792f0b464a8fbb04c4345143f77bbdca07acb744628ce")
    version("1.7.6", sha256="864a1459c82676c991fcaed931263a415e815e3c9dc2cad2f94bda6fa4d112e5")
    version("1.7.5", sha256="7b1dc7bb380d0fbadce12072f5cc21912c115e826182a3922d864e7edea131db")
    version("1.7.4", sha256="3df316b89e9c0052104f8956e4f7d26c0b0b05cdace7d908be35c383361e3a71")
    version("1.7.3", sha256="ebf6094733823e9cc2d1586aff06db2d8999c74a47e666baf305322f62c48058")
    version("1.7.2", sha256="7f093cf947824ec118767c7c1999a50ea9343c173cf8c5062e3800ba54c2943e")
    version("1.7.1", sha256="edd7971ecd272314309c800395200b07cf68547cbac3378a02d0b8c9ac03027b")
    version("1.7.0", sha256="b3d6bfb0c52ed87cd240cee5e93e09102832d9ef32505d7275f4d3191a35ce3b")
    version("1.6.7", sha256="2abf378573832c201bc6a9fecfff5b2006fc98c7a272540326cda8eb5bd95e16")
    version("1.6.6", sha256="cf172a496d9108b93420530ea91055d07ecd514d2894d78db46b806530e91d21")
    version("1.6.5", sha256="1477fe754cfe2e4e06aa363a773accf18aab960a8b899968b77834368cac14c5")
    version("1.6.4", sha256="4c01f43c18b7b2e71f61dea0bb8c6fdc099c8e1a66256c510652884c4ffffbca")
    version("1.6.3", sha256="1dd7e334fe54a05ff911d9e227d395abc5efd29e29d60187a036b2201f97da19")
    version("1.6.2", sha256="5793cd1320694118423888801ca520f2719565fde04699ee69e1751f47cb57a8")
    version("1.6.1", sha256="ec3f4cc4eb57f94fb431cc37db10eb831f025df95ffd9e516b8009199253c62b")
    version("1.6.0", sha256="2920ef2588268484b650dc08438664a3539b79c65a9e80d58e3771bb699e2a6b")
    version("1.5.9", sha256="1a19cc8c34c08f1797a93d355250e682eb85d62d4ab277b6714d7873b4bdde75")
    version("1.5.8", sha256="011c5be5cc565f8baf02e7ebbe57a57b4d70dc6a528d5b0102700020bbf5a973")
    version("1.5.7", sha256="f775df11b034154b8f5d43f12007692c3314672e60d3e554b3928fe5b0f00c29")
    version("1.5.6", sha256="050e17b1b80658213281a2e4112dfecc0096f01f269cd739d601b2fd0e790a0c")
    version("1.5.5", sha256="ce45df6248c6c50633953048240513dc52ca5c9144ef69ea72ada2df23bc4918")
    version("1.5.4", sha256="c41853a1f3aa0794875ae09c1ba4348942eb890e798ac7cee6e3505a9b68b678")
    version("1.5.3", sha256="1220ac0ae204c3ed6b22a6a35c30d9b5c1ded35a1054cff131861b4a919d4904")
    version("1.5.2", sha256="ec113c53a6174b174aaea8f45802cc419184ce056123b93ab8d3f80fc1bd4986")
    version("1.5.1", sha256="a8b088b3ede67d560e40f91f4f99be313f21841c46ce2f657af7692a7bbe3276")
    version("1.5.0", sha256="2c2b77344854fac937a8ef07c0928c50829ff4c69bcad6e0afb92da611b7dd18")
    version("1.4.0", sha256="e76a129f7c2b72b53525fe0b712606eeeab0dc145daa070ebf0728f0384eaf48")
    version("1.3.1", sha256="274e196d009e3aac6dd1f2db876de9613ca1a3c21ec3364bc3662f5493bc9747")
    version("1.3.0", sha256="d63197d5940b481ecb06cf4703d9c0b49388f32cad61ccae580d1b80312bd215")
    version("1.2.1", sha256="e86964e91e4fbbba443d2848f55c028001de4713dcc64c40339389de053e7d8b")
    version("1.2.0", sha256="143fa86cd7965d26d3897a5752307bfe08f4866c2f9a9f226a393127d19ee353")
    version("1.1.0", sha256="5d2e8f3c1cddfb59fe651931c7c605fe0ed067864fa86047aed312c6a7938e01")
    version("1.0.7", sha256="145c27d922c27a4e1d6d50030f4ddece5f03d6c309a5e392a5fcbb5e83e747ab")
    version("1.0.6", sha256="357732448d67a593e5ff004418f2a2a263a1401ffe84e021f8a714aa183eaa21")
    version("1.0.5", sha256="ba72bc3943a1b39fa63900570948199cf5ed5c7523f2c4af4740e51b098f1794")
    version("1.0.4", sha256="697fe397c69689feecb2a731e19b2ff85e19343b8198c4f18a7064c4f7123950")
    version("1.0.3", sha256="6a1d1d75d9d74da457726ea9463c1b0b6ba38d4b43ef54e1c33f885e70fdae4b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("root", default=False, description="Enable ROOT interface")

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("zlib-api")
    depends_on("boost", when="@:1.6.0", type=("build", "run"))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@:1.6.0", type=("build", "run"))
    depends_on("py-cython@0.18:", type="build", when="@:1.4.0")
    depends_on("py-cython@0.20:", type="build", when="@1.4.0:1.6.5")
    depends_on("py-cython@0.23.5:", type="build", when="@1.6.5:1.8.0")
    depends_on("py-cython@0.24:", type="build", when="@1.8.0:")
    depends_on("py-matplotlib", when="@1.3.0:", type=("build", "run"))
    depends_on("root", type=("build", "link", "run"), when="+root")

    extends("python")

    patch("yoda-1.5.5.patch", level=0, when="@1.5.5")
    patch("yoda-1.5.9.patch", level=0, when="@1.5.9")
    patch("yoda-1.6.1.patch", level=0, when="@1.6.1")
    patch("yoda-1.6.2.patch", level=0, when="@1.6.2")
    patch("yoda-1.6.3.patch", level=0, when="@1.6.3")
    patch("yoda-1.6.4.patch", level=0, when="@1.6.4")
    patch("yoda-1.6.5.patch", level=0, when="@1.6.5")
    patch("yoda-1.6.6.patch", level=0, when="@1.6.6")
    patch("yoda-1.6.7.patch", level=0, when="@1.6.7")

    conflicts(
        "%gcc@10:",
        when="@:1.8.5",
        msg="yoda up to 1.8.5 is missing a <limits> include in AnalysisObject.h."
        "Use version 1.9.0 or later, or patch earlier versions if needed.",
    )

    def configure_args(self):
        args = []
        if self.spec.satisfies("@:1.6.0"):
            args.append("--with-boost=" + self.spec["boost"].prefix)

        args.extend(self.enable_or_disable("root"))

        return args
