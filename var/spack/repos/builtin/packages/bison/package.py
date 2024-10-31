# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *


class Bison(AutotoolsPackage, GNUMirrorPackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "https://www.gnu.org/software/bison/"
    gnu_mirror_path = "bison/bison-3.6.4.tar.gz"

    tags = ["build-tools"]

    executables = ["^bison$"]

    license("GPL-3.0-or-later")

    version("3.8.2", sha256="06c9e13bdf7eb24d4ceb6b59205a4f67c2c7e7213119644430fe82fbd14a0abb")
    version("3.8.1", sha256="ce318a47196155fb7c26912b513102f3d0e14757c2e495e34608757b61339c5c")
    version("3.8", sha256="d5d184d421aee15603939973a6b0f372f908edfb24c5bc740697497021ad9458")
    version("3.7.6", sha256="69dc0bb46ea8fc307d4ca1e0b61c8c355eb207d0b0c69f4f8462328e74d7b9ea")
    version("3.7.5", sha256="151cb5f12716e3fe93a27a317cd44878329659f275b342779bfaef4a526bbf70")
    version("3.7.4", sha256="fbabc7359ccd8b4b36d47bfe37ebbce44805c052526d5558b95eda125d1677e2")
    version("3.7.3", sha256="104fe912f2212ab4e4a59df888a93b719a046ffc38d178e943f6c54b1f27b3c7")
    version("3.7.2", sha256="415cd91044517bbfd8d135dea24e054501db238a5515edd9cdbb795ba3e82a84")
    version("3.7.1", sha256="1dd952839cf0d5a8178c691eeae40dc48fa50d18dcce648b1ad9ae0195367d13")
    version("3.7", sha256="492ad61202de893ca21a99b621d63fa5389da58804ad79d3f226b8d04b803998")
    version("3.6.4", sha256="8183de64b5383f3634942c7b151bf2577f74273b2731574cdda8a8f3a0ab13e9")
    version("3.6.3", sha256="4b4c4943931e811f1073006ce3d8ee022a02b11b501e9cbf4def3613b24a3e63")
    version("3.6.2", sha256="e28ed3aad934de2d1df68be209ac0b454f7b6d3c3d6d01126e5cd2cbadba089a")
    version("3.6.1", sha256="1120f8bfe2cc13e5e1e3f671dc41b1a535ca5a75a70d5b349c19da9d4389f74d")
    version("3.6", sha256="f630645e330bde5847266cc5c8194f0135ced75cced150358d9abe572b95f81c")
    version("3.5.3", sha256="34e201d963156618a0ea5bc87220f660a1e08403dd3c7c7903d4f38db3f40039")
    version("3.5.2", sha256="b4dbb6dd080f4db7f344f16506502973ca2b15f15c7dbbd1c1c278a456d094fa")
    version("3.5.1", sha256="4cef2322d96751be1c0d04f3e57adbb30e7fea83af9c00f98efa6e7509296f25")
    version("3.5", sha256="0b36200b9868ee289b78cefd1199496b02b76899bbb7e84ff1c0733a991313d1")
    version("3.4.2", sha256="ff3922af377d514eca302a6662d470e857bd1a591e96a2050500df5a9d59facf")
    version("3.4.1", sha256="7007fc89c216fbfaff5525359b02a7e5b612694df5168c74673f67055f015095")
    version("3.3.2", sha256="0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1")
    version("3.0.5", sha256="cd399d2bee33afa712bac4b1f4434e20379e9b4099bce47189e09a7675a2d566")
    version("3.0.4", sha256="b67fd2daae7a64b5ba862c66c07c1addb9e6b1b05c5f2049392cfd8a2172952e")
    version("2.7", sha256="19bbe7374fd602f7a6654c131c21a15aebdc06cc89493e8ff250cb7f9ed0a831")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("color", default=False, description="Enable experimental colored output", when="@3.4:")

    # https://lists.gnu.org/archive/html/bug-bison/2019-08/msg00008.html
    patch("parallel.patch", when="@3.4.2")

    provides("yacc")

    depends_on("gettext", when="+color")
    depends_on("m4@1.4.6:", type=("build", "run"))
    depends_on("diffutils", type="build")

    patch("pgi.patch", when="@3.0.4")
    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    patch("nvhpc-3.6.patch", when="@3.6.0:3.6 %nvhpc")
    patch("nvhpc-3.7.patch", when="@3.7.0:3.7 %nvhpc")

    conflicts("%intel@:14", when="@3.4.2:", msg="Intel 14 has immature C11 support")
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
            "see https://github.com/spack/spack/issues/37172"
        ),
    )

    if sys.platform == "darwin" and macos_version() >= Version("10.13"):
        patch("secure_snprintf.patch", level=0, when="@3.0.4")

    build_directory = "spack-build"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"bison \(GNU Bison\)\s+(\S+)", output)
        return match.group(1) if match else None
