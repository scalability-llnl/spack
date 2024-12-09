# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class WasiSdkPrebuilt(Package):
    """
    A group of standard API specifications for software compiled to the W3C WebAssembly standard
    """

    homepage = "https://wasi.dev/"
    url = "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-14/wasi-sdk-14.0-linux.tar.gz"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("22.0", sha256="fa46b8f1b5170b0fecc0daf467c39f44a6d326b80ced383ec4586a50bc38d7b8")
    version("21.0", sha256="f2fe0723b337c484556b19d64c0f6c6044827014bfcd403d00951c65a86cfa26")
    version("20.0", sha256="7030139d495a19fbeccb9449150c2b1531e15d8fb74419872a719a7580aad0f9")
    version("19.0", sha256="d900abc826eec1955b9afd250e7cc2496338abbf6c440d86a313c06e42083fa1")
    version("17.0", sha256="8778a476af7898a51db9b78395687cc9c8b69702850da77a763711e832614dac")
    version("16.0", sha256="10df3418485e60b9283c1132102f8d3ca34b4fbe8c4649e30282ee84fe42d788")
    version("15.0", sha256="9b1f2c900a034a44e59b74843cd79b4f189342598e554029367ef0a2ac286703")
    version("14.0", sha256="8c8ebb7f71dcccbb8b1ab384499a53913b0b6d1b7b3281c3d70165e0f002e821")

    provides("wasi-sdk")

    def url_for_version(self, version):
        base = "https://github.com/WebAssembly/wasi-sdk/releases/download"
        major = version.up_to(1)
        full = version.up_to(2)
        return f"{base}/wasi-sdk-{major}/wasi-sdk-{full}-linux.tar.gz"

    def install(self, spec, prefix):
        install_tree("share/wasi-sysroot", prefix)
