# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Strace(AutotoolsPackage):
    """Strace is a diagnostic, debugging and instructional userspace
    utility for Linux. It is used to monitor and tamper with interactions
    between processes and the Linux kernel, which include system calls,
    signal deliveries, and changes of process state."""

    homepage = "https://strace.io"
    url = "https://github.com/strace/strace/releases/download/v6.11/strace-6.11.tar.xz"

    maintainers("michaelkuhn")

    license("BSD-3-Clause")

    version("6.11", sha256="83262583a3529f02c3501aa8b8ac772b4cbc03dc934e98bab6e4883626e283a5")
    version("5.19", sha256="aa3dc1c8e60e4f6ff3d396514aa247f3c7bf719d8a8dc4dd4fa793be786beca3")
    version("5.17", sha256="5fb298dbd1331fd1e1bc94c5c32395860d376101b87c6cd3d1ba9f9aa15c161f")
    version("5.12", sha256="29171edf9d252f89c988a4c340dfdec662f458cb8c63d85431d64bab5911e7c4")
    version("5.11", sha256="ffe340b10c145a0f85734271e9cce56457d23f21a7ea5931ab32f8cf4e793879")
    version("5.10", sha256="fe3982ea4cd9aeb3b4ba35f6279f0b577a37175d3282be24b9a5537b56b8f01c")
    version("5.9", sha256="39473eb8465546c3e940fb663cb381eba5613160c7302794699d194a4d5d66d9")
    version("5.8", sha256="df4a669f7fff9cc302784085bd4b72fab216a426a3f72c892b28a537b71e7aa9")
    version("5.7", sha256="b284b59f9bcd95b9728cea5bd5c0edc5ebe360af73dc76fbf6334f11c777ccd8")
    version("5.6", sha256="189968eeae06ed9e20166ec55a830943c84374676a457c9fe010edc7541f1b01")
    version("5.5", sha256="9f58958c8e59ea62293d907d10572e352b582bd7948ed21aa28ebb47e5bf30ff")
    version("5.4", sha256="f7d00514d51290b6db78ad7a9de709baf93caa5981498924cbc9a744cfd2a741")
    version("5.3", sha256="6c131198749656401fe3efd6b4b16a07ea867e8f530867ceae8930bbc937a047")
    version("5.2", sha256="d513bc085609a9afd64faf2ce71deb95b96faf46cd7bc86048bc655e4e4c24d2")
    version("5.1", sha256="f5a341b97d7da88ee3760626872a4899bf23cf8dee56901f114be5b1837a9a8b")
    version("5.0", sha256="3b7ad77eb2b81dc6078046a9cc56eed5242b67b63748e7fc28f7c2daf4e647da")
    version("4.21", sha256="5c7688db44073e94c59a5627744e5699454419824cc8166e8bcfd7ec58375c37")

    variant("mpers", default=False, description="Enable multiple personalities support")

    depends_on("c", type="build")
    depends_on("gawk", when="+mpers", type="build")

    conflicts("platform=darwin", msg="strace runs only on Linux")
    conflicts("platform=windows", msg="strace runs only on Linux")

    def configure_args(self):
        args = []
        if self.spec.satisfies("+mpers"):
            args.append("--enable-mpers=yes")
        else:
            args.append("--enable-mpers=no")
        return args
