# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rclone(GoPackage):
    """Rclone is a command line program to sync files and directories
    to and from various cloud storage providers"""

    homepage = "https://rclone.org"
    url = "https://github.com/rclone/rclone/releases/download/v1.57.0/rclone-v1.57.0.tar.gz"

    maintainers("alecbcs")

    license("MIT")

    version("1.68.1", sha256="c5d45b83dd008d08a0903eebf1578a11a40a77152226e22ce5e9287b9db05579")
    version("1.65.2", sha256="1305c913ac3684d02ce2bade0a23a2115c1ec03c9447d1562bb6cd9fa2573412")
    version("1.65.1", sha256="904b906cc465dd679a00487497e3891d33fca6b6e25c184400bccfb248344f39")
    version("1.65.0", sha256="45ec732d50b2517dc2c860317a3bf79867634a8143e4a441a3e399434ad6c141")
    version("1.64.2", sha256="0c74d8fb887691e04e865e3b6bc32e8af47c3e54a9922ffdbed38c8323e281c9")
    version("1.64.1", sha256="670e18960efd34bae9d1a0152a54f16ba0c6b8fad728d7ff4ea8b141ef1ed93d")
    version("1.64.0", sha256="fb08b2b7c991ade4019a561f9bb75683b8d0daa45226efbc9937639775977203")
    version("1.63.1", sha256="0d8bf8b7460681f7906096a9d37eedecc5a1d1d3ad17652e68f0c6de104c2412")
    version("1.63.0", sha256="88ed9c876b03d2cc745463903ac5233e441cd56d0d1031906bc8381af11ea0c8")
    version("1.62.2", sha256="340371f94604e6771cc4a2c91e37d1bf00a524deab520340440fb0968e783f63")
    version("1.62.1", sha256="3bb03c08f11fda276c953544487558c3c0bfe14f89796b9eaa108a334d854ed1")
    version("1.62.0", sha256="2a04a254f60255c10998f74be9d320740df82525a7d16d8ceebab57627137b44")
    version("1.61.1", sha256="34b5f52047741c7bbf54572c02cc9998489c4736a753af3c99255296b1af125d")
    version("1.59.1", sha256="db3860e4549af28d87aa83f2035a57c5d081b179e40d4c828db19c3c3545831e")
    version("1.58.1", sha256="4d1d50a5b4888aa8eca10624073759ab8376c8b1acb38a238831d40074792524")
    version("1.58.0", sha256="8e0c49fad69525d1219415d2f0651fd243ddf02291fd95e91d2b074d4858c31f")
    version("1.57.0", sha256="3a762c02c202a9142c2d5c1a3927563a556d1683abadd25d2f695e237e4ea693")
    version("1.56.2", sha256="a8813d25c4640e52495fee83e525e76283c63f01d1cce8fbb58d8486b0c20c8a")
    version("1.56.1", sha256="090b4b082caa554812f341ae26ea6758b40338836122595d6283c60c39eb5a97")
    version("1.56.0", sha256="81d2eda23ebaad0a355aab6ff030712470a42505b94c01c9bb5a9ead9168cedb")
    version("1.55.1", sha256="25da7fc5c9269b3897f27b0d946919df595c6dda1b127085fda0fe32aa59d29d")
    version("1.55.0", sha256="75accdaedad3b82edc185dc8824a19a59c30dc6392de7074b6cd98d1dc2c9040")

    depends_on("go@1.14:", type="build")
    depends_on("go@1.17:", type="build", when="@1.58:")
    depends_on("go@1.18:", type="build", when="@1.62:")
    depends_on("go@1.19:", type="build", when="@1.63:")
    depends_on("go@1.20:", type="build", when="@1.66:")
    depends_on("go@1.21:", type="build", when="@1.68:")

    @run_after("install")
    def install_completions(self):
        rclone = Executable(self.prefix.bin.rclone)

        mkdirp(bash_completion_path(self.prefix))
        mkdirp(fish_completion_path(self.prefix))
        mkdirp(zsh_completion_path(self.prefix))

        rclone("genautocomplete", "bash", str(bash_completion_path(self.prefix) / "rclone"))
        rclone("genautocomplete", "fish", str(fish_completion_path(self.prefix) / "rclone.fish"))
        rclone("genautocomplete", "zsh", str(zsh_completion_path(self.prefix) / "_rclone"))
