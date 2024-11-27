# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Wgl(Package):
    """External WGl and Windows OpenGL emulation representation in Spack"""

    homepage = "https://learn.microsoft.com/en-us/windows/win32/opengl/wgl-and-windows-reference"
    has_code = False
    tags = ["windows", "windows-system"]
    # hard code the extension as shared lib
    libraries = ["OpenGL32.Lib"]

    # versions here are in no way related to actual WGL versions
    # (there is only one on a system at a time)
    # but instead reflects the Windows Kit version that a particular WGL library file is found in
    # Windows Kits are intended to be more or less contained environments so this allows us to
    # marshall our SDK and WDK to their respective WGLs. The purpose here is to better reflect
    # the concept of an MS build toolchain version W.R.T. to MSVC
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
    version("10.0.20348")

    variant(
        "plat", values=("x64", "x86", "arm", "arm64"), default="x64", description="Toolchain arch"
    )

    # As per https://github.com/spack/spack/pull/31748 this provisory version represents
    # an arbitrary openGL version designed for maximum compatibility with calling packages
    # this current version simply reflects the latest OpenGL vesion available at the time of
    # package creation and is set in a way that all specs currently depending on GL are
    # satisfied appropriately
    provides("gl@4.6")

    # WGL exists on all Windows systems post win 98, however the headers
    # needed to use OpenGL are found in the SDK (GL/gl.h)
    # Dep is needed to consolidate sdk version to locate header files for
    # version of SDK being used
    # Generic depends to capture handling for external versions
    depends_on("win-sdk")
    depends_on("win-sdk@10.0.19041", when="@10.0.19041")
    depends_on("win-sdk@10.0.18362", when="@10.0.18362")
    depends_on("win-sdk@10.0.17763", when="@10.0.17763")
    depends_on("win-sdk@10.0.17134", when="@10.0.17134")
    depends_on("win-sdk@10.0.16299", when="@10.0.16299")
    depends_on("win-sdk@10.0.15063", when="@10.0.15063")
    depends_on("win-sdk@10.0.14393", when="@10.0.14393")

    # WGL has no meaning on other platforms, should not be able to spec
    for plat in ["linux", "darwin"]:
        conflicts("platform=%s" % plat)

    @classmethod
    def determine_version(cls, lib):
        """Allow for WGL to be externally detectable"""
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

    def _spec_arch_to_sdk_arch(self):
        spec_arch = str(self.spec.architecture.target.family).lower()
        _64bit = "64" in spec_arch
        arm = "arm" in spec_arch
        if arm:
            return "arm64" if _64bit else "arm"
        else:
            return "x64" if _64bit else "x86"

    # As noted above, the headers neccesary to include
    @property
    def headers(self):
        return find_headers(
            "GL", root=os.path.join(self.prefix.Include, str(self.version) + ".0"), recursive=True
        )

    @property
    def libs(self):
        return find_libraries(
            "opengl32",
            shared=False,
            root=os.path.join(
                self.prefix.Lib, str(self.version) + ".0", "um", self._spec_arch_to_sdk_arch()
            ),
            recursive=True,
        )

    def install(self, spec, prefix):
        raise RuntimeError(
            "This package is not installable from Spack\
            and should be installed on the system prior to Spack use.\
                If not installed this package should be installed via\
                    the Visual Studio installer in order to use the \
                        MSVC compiler on Windows."
        )
