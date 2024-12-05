# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Moosefs(AutotoolsPackage):
    """
    MooseFS is a Petabyte Open Source Network Distributed File System. It
    is easy to deploy and maintain, fault tolerant, highly performing,
    easily scalable, POSIX compliant.
    """

    homepage = "https://github.com/moosefs/moosefs"
    url = "https://github.com/moosefs/moosefs/archive/v3.0.109.tar.gz"

    license("GPL-2.0-only")

    version("3.0.109", sha256="413349d254f75ea9b9c974a12f67225c7cbec389f8a39a68db569c0d0f6f4ef3")
    version("3.0.108", sha256="344c4b7875603fc0b091e5c80f4a5b2eda780a3d050de2ef38232e55e56b054a")
    version("3.0.107", sha256="192dca0c04f61334846e00c1193952bb0f69f3960f223a8d55016b74d72cfdb6")
    version("3.0.105", sha256="12a5bb265d774da8fc6f051c51de08105ddeaa162b2d972d491caa542e01164f")
    version("3.0.104", sha256="b3209ecd8366038ba898c4642dd6fdf2fa5d50a37345f01ed209e078700db5bb")
    version("3.0.103", sha256="c5f1f6f78c2b7d8d6563000deed704ead3deac77279cb13f9f16d7ee56ee7ff7")

    depends_on("c", type="build")  # generated

    def configure_args(self):
        args = ["--with-systemdsystemunitdir=" + self.spec["moosefs"].prefix.lib.systemd.system]
        return args
