# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re

from spack.package import *


class WinSdk(Package):
    """
    Windows Desktop C++ development SDK
    Spack packaged used to define search heuristics
    to locate the SDK on a filesystem
    """

    homepage = "https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/"
    has_code = False
    tags = ["windows", "windows-system"]

    # The sdk has many libraries and executables. Record one for detection purposes
    libraries = ["rcdll.dll"]

    version("10.0.22621")
    version("10.0.19041")
    version("10.0.18362")
    version("10.0.17763")
    version("10.0.17134")
    version("10.0.16299")
    version("10.0.15063")
    version("10.0.14393")
    version("10.0.10586")
    version("10.0.26639")

    variant(
        "plat", values=("x64", "x86", "arm", "arm64"), default="x64", description="Toolchain arch"
    )

    # WinSDK versions depend on compatible compilers
    # WDK versions do as well, but due to their one to one dep on the SDK
    # we can ensure that requirment here
    # WinSDK is very backwards compatible, however older
    # MSVC editions may have problems with newer SDKs
    conflicts("%msvc@:19.16.00000", when="@10.0.19041")
    conflicts("%msvc@:19.16.00000", when="@10.0.18362")
    conflicts("%msvc@:19.15.00000", when="@10.0.17763")
    conflicts("%msvc@:19.14.00000", when="@10.0.17134")
    conflicts("%msvc@:19.11.00000", when="@10.0.16299")
    conflicts("%msvc@:19.10.00000", when="@10.0.15063")
    conflicts("%msvc@:19.10.00000", when="@10.0.14393")
    conflicts("%msvc@:19.00.00000", when="@10.0.10586")

    # For now we don't support Windows development env
    # on other platforms
    for plat in ["linux", "darwin"]:
        conflicts("platform=%s" % plat)

    @classmethod
    def determine_version(cls, lib):
        """
        WinSDK that we would like to
        be discoverable externally by Spack.
        """
        # This version is found in the package's path
        # not by calling an exe or a libraries name
        version_match_pat = re.compile(r"[0-9][0-9].[0-9]+.[0-9][0-9][0-9][0-9][0-9]")
        ver_str = re.search(version_match_pat, lib)
        return ver_str if not ver_str else Version(ver_str.group())

    @classmethod
    def determine_variants(cls, libs, ver_str):
        """Allow for determination of toolchain arch for detected WGL"""
        variants = []
        for lib in libs:
            base, lib_name = os.path.split(lib)
            _, arch = os.path.split(base)
            variants.append("plat=%s" % arch)
        return variants

    def install(self, spec, prefix):
        raise RuntimeError(
            "This package is not installable from Spack\
            and should be installed on the system prior to Spack use.\
                If not installed this package should be installed via\
                    the Visual Studio installer in order to use the \
                        MSVC compiler on Windows."
            "If absolutely neccesary this SDK can be installed directly from Microsoft\
                but this approach is not recommended unless you know what you're doing \
                    or if you're on Windows 11 you have no choice for the moment."
        )
