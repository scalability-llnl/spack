# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MochiMargo(AutotoolsPackage):
    """A library that provides Argobots bindings to the Mercury RPC
    implementation."""

    homepage = "https://github.com/mochi-hpc/mochi-margo"
    git = "https://github.com/mochi-hpc/mochi-margo.git"
    url = "https://github.com/mochi-hpc/mochi-margo/archive/v0.9.tar.gz"

    maintainers("carns", "mdorier", "fbudin69500")

    version("main", branch="main")
    version("0.17.0", sha256="5c456cdc2e3156f902e5068468ee6d061eb252dcfdfcb2b570726e9cf84fc2e8")
    version("0.16.0", sha256="5fb7ea3633b5bcc735e605dba27187ea893958bf86b8928184028735a338c61b")
    version("0.15.0", sha256="f962f02ddaae125eaf15bf89126ee47b4f852d366b14248d2d67a0be8f661224")
    version("0.14.1", sha256="69229a9126b76aff7fd47e25c4a8f72804f101c5c603c4e4ef93f4fb7a1b6662")
    version("0.14.0", sha256="ff0e3fa786630b63280606243c35f1ea3a25fa2ba6f08bf9065cab9fcc7fa1c7")
    version("0.13.1", sha256="cff1decb94089cd0f9c0930b02092838679827b09ce4a2f3a359d59caee28782")
    version("0.13", sha256="9a5a4aa81ceb10e010fbad6c7bb8d39d082fe6e61ed33b2b2d2b056917f401d8")
    version("0.12.1", sha256="ff9d0f8722aff17737cd63f27758314b2ed78e518cd45d1fb9f0e3b7ccbcef50")
    version("0.12", sha256="d9949423d87d74ae20b0e344fdc76cc7e0a62249f219b05297b8f44891f75a8e")
    version("0.11.1", sha256="ce4a61e2796df2a2c6efdfbd2d2c5a6be31e524f279b740a423ed932607503f3")
    version("0.11", sha256="3f9f30591127ecf3aac8a524c69cbc90fe3c8e68e263bda4c69b1e2c8d77ebdd")
    version("0.10", sha256="163be090575ee267a84320b92791d83b98e9549b03bd705a166f0b5e4df53129")
    version("0.9.10", sha256="b205b45fe200d1b2801ea3b913fa75d709af97abf470f4ad72a08d2839f03772")
    version("0.9.9", sha256="9e8fce88a6bd9c1002b4a6924c935ebb2e2024e3afe6618b17e23538335bd15d")
    version("0.9.8", sha256="a139e804bf0b2725433c256e8315a2ba896f1fb34d9057261a4b92df783ffbbb")
    version("0.9.7", sha256="ab45c5594f10d7d8cf8e67529b3972f7174b4ee5e3fbcd8446658490a884c5e2")
    version("0.9.6", sha256="fa339cc9621542fb398bb9fcd6b081d3578c75c3f398f3e6b05033f24ea63e33")
    version("0.9.5", sha256="b5c52477a82aa44a079f876cbb8166d0bce5a07a92bcf8a0c76670b245e728a3")
    version("0.9.4", sha256="4292e083c8375ab07bc6dd0b3b1ea2ce9c9dd864c27ac7f07c6913dcccecc746")
    version("0.9.3", sha256="1331423d4864349c3a9ec52b2114122659da310d5270fa1aea652e8ee48a0b3a")
    version("0.9.2", sha256="de88cd725c8ff3ec63412f3f5ed22ad1a56cb367c31b842c816ce40cba777f7c")
    version("0.9.1", sha256="3fe933f2d758ef23d582bc776e4f8cfae9bf9d0849b8b1f9d73ee024e218f2bc")
    version("0.9", sha256="a24376f66450cc8fd7a43043e189f8efce5a931585e53c1e2e41894a3e99b517")
    version("0.7", sha256="492d1afe2e7984fa638614a5d34486d2ff761f5599b5984efd5ae3f55cafde54")
    version("0.7.2", sha256="0ca796abdb82084813a5de033d92364910b5ad1a0df135534d6b1c36ef627859")
    version("0.7.1", sha256="eebbe02c47ed4c65ef1d4f23ffdc6a8aa2e2348ca6c51bfc3c4dfbf78fbfc30b")
    version("0.6", sha256="56feb718da2b155d7277a7b10b669516ebffaa034f811f3665ceed7ad0f19d1b")
    version("0.6.4", sha256="5ba1c72ee05aa9738d3dc4d6d01bd59790284c6c77b909c5d7756fe7049d6177")
    version("0.6.3", sha256="5f373cd554edd15cead58bd5d30093bd88d45039d06ff7738eb18b3674287c76")
    version("0.6.2", sha256="c6a6909439e1d3ba1a1693d8da66057eb7e4ec4b239c04bc7f19fc487c4c58da")
    version("0.6.1", sha256="80d8d15d0917b5522c31dc2d83136de2313d50ca05c71c5e5ad83c483a3214b7")
    version("0.5", sha256="d3b768b8300bc2cb87964e74c39b4e8eb9822d8a2e56fc93dc475ddcb1a868e3")
    version("0.5.2", sha256="73be3acaf012a85a91ac62824c93f5ee1ea0ffe4c25779ece19723f4baf9547d")
    version("0.5.1", sha256="6fdf58e189538e22341c8361ab069fc80fe5460a6869882359b295a890febad7")
    version("0.4.7", sha256="596d83b11fb2bd9950fd99c9ab12c14915ab2cda233084ae40ecae1e6c584333")
    version("0.4.6", sha256="b27447a2050ae61091bae3ff6b4d23a56153947f18847face9f98facbdb4e329")
    version("0.4.5", sha256="b0d02f73edf180f2393f54c5a980620b8d6dcd42b90efdea6866861824fa49cf")
    version("0.4.4", sha256="2e2e6e2a8a7d7385e2fe204c113cb149f30847f0b1f48ec8dd708a74280bd89e")
    version("0.4.3", sha256="61a634d6983bee2ffa06e1e2da4c541cb8f56ddd9dd9f8e04e8044fb38657475")
    version("0.4.2", sha256="91085e28f50e373b9616e1ae5c3c8d40a19a7d3776259592d8f361766890bcaa")

    depends_on("c", type="build")  # generated

    depends_on("json-c", when="@0.9:")
    depends_on("autoconf@2.65:", type=("build"))
    depends_on("m4", type=("build"))
    depends_on("automake", type=("build"))
    depends_on("libtool", type=("build"))
    depends_on("pkgconfig", type=("build"))
    depends_on("argobots@1.0:")
    depends_on("argobots@1.1:", when="@0.11:")
    # "breadcrumb" support not available in mercury-1.0
    depends_on("mercury@1.0.0:", type=("build", "link", "run"), when="@:0.5.1")
    depends_on("mercury@2.0.0:", type=("build", "link", "run"), when="@0.5.2:")

    # Fix pthread detection
    # https://github.com/mochi-hpc/mochi-margo/pull/177
    patch("mochi-margo-pthreads.patch", when="@0.9:0.9.7")

    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("./prepare.sh")
