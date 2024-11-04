# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OclIcd(AutotoolsPackage):
    """This package aims at creating an Open Source alternative to vendor specific
    OpenCL ICD loaders."""

    homepage = "https://github.com/OCL-dev/ocl-icd"
    url = "https://github.com/OCL-dev/ocl-icd/archive/v2.2.12.tar.gz"
    maintainers("lorddavidiii")

    license("BSD-2-Clause")

    version("2.3.2", sha256="ec47d7dcd961ea06695b067e8b7edb82e420ddce03e0081a908c62fd0b8535c5")
    version("2.3.1", sha256="a32b67c2d52ffbaf490be9fc18b46428ab807ab11eff7664d7ff75e06cfafd6d")
    version("2.3.0", sha256="469f592ccd9b0547fb7212b17e1553b203d178634c20d3416640c0209e3ddd50")
    version("2.2.14", sha256="46df23608605ad548e80b11f4ba0e590cef6397a079d2f19adf707a7c2fbfe1b")
    version("2.2.13", sha256="f85d59f3e8327f15637b91e4ae8df0829e94daeff68c647b2927b8376b1f8d92")
    version("2.2.12", sha256="17500e5788304eef5b52dbe784cec197bdae64e05eecf38317840d2d05484272")
    version("2.2.11", sha256="c1865ef7701b8201ebc6930ed3ac757c7e5cb30f3aa4c1e742a6bc022f4f2292")
    version("2.2.10", sha256="d0459fa1421e8d86aaf0a4df092185ea63bc4e1a7682d3af261ae5d3fae063c7")
    version("2.2.9", sha256="88da749bc2bd75149f0bb6e72eb4a9d74401a54f4508bc730f13cc03c57a17ed")
    version("2.2.8", sha256="8a8a405c7d659b905757a358dc467f4aa3d7e4dff1d1624779065764d962a246")
    version("2.2.7", sha256="b8e68435904e1a95661c385f24d6924ed28f416985c6db5a3c7448698ad5fea2")
    version("2.2.6", sha256="4567cae92f58c1d6ecfc771c456fa95f206d8a5c7c5d6c9010ec688a9fd83750")
    version("2.2.5", sha256="50bf51f4544f83e69a5a2f564732a2adca63fbe9511430aba12f8d6f3a53ae59")
    version("2.2.4", sha256="92853137ffff393cc74f829357fdd80ac46a82b46c970e80195db86164cca316")
    version("2.2.3", sha256="46b8355d90f8cc240555e4e077f223c47b950abeadf3e1af52d6e68d2efc2ff3")

    depends_on("c", type="build")  # generated

    variant(
        "headers",
        default=False,
        description="Install also OpenCL headers to use this as OpenCL provider",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("ruby", type="build")
    depends_on("asciidoc-py3", type="build")
    depends_on("xmlto", type="build")
    depends_on("opencl-headers@3.0:", when="+headers")

    provides("opencl@:3.0", when="@2.2.13:+headers")
    provides("opencl@:2.2", when="@2.2.12+headers")
    provides("opencl@:2.1", when="@2.2.8:2.2.11+headers")
    provides("opencl@:2.0", when="@2.2.3:2.2.7+headers")

    # upstream patch to fix compatibility with the latest version of the
    # official khronos OpenCL C headers release, ie opencl-c-headers@2021.04.29
    patch(
        "https://github.com/OCL-dev/ocl-icd/commit/aed1832c81c0971ea001e12d41e04df834257f94.patch?full_index=1",
        sha256="90fef5c4b341848c82d484a2329339c4762c2451259378fbda60cc86b3216616",
        when="@2.3.0",
    )

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("@:2.2.12"):
            # https://github.com/OCL-dev/ocl-icd/issues/8
            # this is fixed in version grater than 2.2.12
            flags.append("-O2")
            # gcc-10 change the default from -fcommon to fno-common
            # This is fixed in versions greater than 2.2.12:
            # https://github.com/OCL-dev/ocl-icd/commit/4667bddd365bcc1dc66c483835971f0083b44b1d
            if self.spec.satisfies("%gcc@10:"):
                flags.append("-fcommon")
        return (flags, None, None)
