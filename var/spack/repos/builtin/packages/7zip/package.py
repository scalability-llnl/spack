# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import platform
import re
import shutil

from spack.package import *


class _7zip(SourceforgePackage, Package):
    """7-Zip is a file archiver for Windows"""

    homepage = "https://sourceforge.net/projects/sevenzip/"
    sourceforge_mirror_path = "sevenzip/files/7z2107-src.tar.xz"
    tags = ["windows"]

    executables = ["7z"]

    license("LGPL-2.0-only")

    version("21.07", sha256="213d594407cb8efcba36610b152ca4921eda14163310b43903d13e68313e1e39")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "link_type",
        default="shared",
        description="build shared and/or static libraries",
        values=("static", "shared"),
        multi=True,
    )

    phases = ["build", "install"]

    conflicts("platform=linux")
    conflicts("platform=darwin")

    # TODO: Patch on WinSDK version 10.0.20348.0 when SDK is introduced to Spack
    # This patch solves a known bug in that SDK version on the 7zip side
    # right now patch for all versions to prevent build errors
    patch("noexcept_typedef.patch", when="platform=windows")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--help", output=str, error=str)
        match = re.search(r"7-Zip ([0-9][0-9]*.[0-9][0-9])", output)
        return match.group(1) if match else None

    def url_version(self, version):
        ver_str = str(version).replace(".", "")
        return "7z" + ver_str

    @property
    def _7z_src_dir(self):
        return os.path.join(self.stage.source_path, "CPP", "7zip")

    @property
    def plat_arch(self):
        """
        String referencing platform architecture
        filtered through 7zip's Windows build file
        """
        arch = platform.machine()
        if arch.lower() == "amd64":
            arch = "x64"
        elif arch.lower() == "i386":
            arch = "x86"
        return arch

    def is_64bit(self):
        return "64" in str(self.pkg.spec.target.family)

    def build(self, spec, prefix):
        link_type = "1" if "static" in spec.variants["link_type"].value else "0"
        nmake_args = [
            f"PLATFORM={self.plat_arch}",
            f"MY_STATIC_LINK={link_type}",
            "NEW_COMPILER=1",
        ]
        # 7zips makefile is configured in such as way that if this value is set
        # compiler paths with spaces are incorrectly parsed. Compiler will be infered
        # from VCVARs on Windows
        os.environ.pop("CC", None)
        with working_dir(self._7z_src_dir):
            nmake(*nmake_args)

    def install(self, spec, prefix):
        """7Zip exports no install target so we must hand install"""
        arch_prefix = "x64" if self.is_64bit() else "x86"
        path_roots = ["Bundles", "UI"]
        exts = ["*.exe", "*.dll"]
        with working_dir(self._7z_src_dir):
            for root in path_roots:
                pth = os.path.join(root, "*", arch_prefix)
                for ext in exts:
                    glob_str = os.path.join(pth, ext)
                    files = glob.glob(glob_str)
                    [
                        shutil.copy(
                            os.path.join(self._7z_src_dir, x),
                            os.path.join(prefix, os.path.basename(x)),
                        )
                        for x in files
                    ]
