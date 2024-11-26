# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Texinfo(AutotoolsPackage, GNUMirrorPackage):
    """Texinfo is the official documentation format of the GNU project.

    It was invented by Richard Stallman and Bob Chassell many years ago,
    loosely based on Brian Reid's Scribe and other formatting languages
    of the time. It is used by many non-GNU projects as well."""

    homepage = "https://www.gnu.org/software/texinfo/"
    gnu_mirror_path = "texinfo/texinfo-6.0.tar.gz"

    executables = ["^info$"]

    tags = ["build-tools"]

    license("GPL-3.0-or-later")

    version("7.1", sha256="dd5710b3a53ac002644677a06145748e260592a35be182dc830ebebb79c5d5a0")
    version("7.0.3", sha256="3cc5706fb086b895e1dc2b407aade9f95a3a233ff856273e2b659b089f117683")
    version("7.0", sha256="9261d4ee11cdf6b61895e213ffcd6b746a61a64fe38b9741a3aaa73125b35170")
    version("6.8", sha256="8e09cf753ad1833695d2bac0f57dc3bd6bcbbfbf279450e1ba3bc2d7fb297d08")
    version("6.7", sha256="a52d05076b90032cb2523673c50e53185938746482cf3ca0213e9b4b50ac2d3e")
    version("6.6", sha256="900723b220baa4672c4214a873a69ecbe1cb5f14c926a1a4bbb230ac309294cb")
    version("6.5", sha256="d34272e4042c46186ddcd66bd5d980c0ca14ff734444686ccf8131f6ec8b1427")
    version("6.3", sha256="300a6ba4958c2dd4a6d5ce60f0a335daf7e379f5374f276f6ba31a221f02f606")
    version("6.0", sha256="83d3183290f34e7f958d209d0b20022c6fe9e921eb6fe94c27d988827d4878d2")
    version("5.2", sha256="6b8ca30e9b6f093b54fe04439e5545e564c63698a806a48065c0bba16994cf74")
    version("5.1", sha256="50e8067f9758bb2bf175b69600082ac4a27c464cb4bcd48a578edd3127216600")
    version("5.0", sha256="2c579345a39a2a0bb4b8c28533f0b61356504a202da6a25d17d4d866af7f5803")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl")
    depends_on("ncurses")
    depends_on("gettext")

    # sanity check
    sanity_check_is_file = [join_path("bin", "info"), join_path("bin", "makeinfo")]

    # Fix unescaped braces in regexps.
    # Ref: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=898994
    patch("fix_unescaped_braces.patch", when="@6.3:6.5")
    patch("fix_unescaped_braces_2.patch", when="@5.1:6.0")
    patch("fix_unescaped_braces_3.patch", when="@5.0")

    # Apply this fix to perform thread-safe processing in code
    # that uses the global locale.
    # Ref: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=902771
    patch("update_locale_handling.patch", when="@6.3:6.5")

    patch("nvhpc.patch", when="%nvhpc")

    @property
    def build_targets(self):
        targets = []
        if self.spec.satisfies("@7.0:"):
            targets.append(f"CFLAGS={self.compiler.c11_flag}")
        return targets

    def setup_build_environment(self, env):
        # texinfo builds Perl XS modules internally, and by default it overrides the
        # CC that the top-level configure reports. This loses the Spack wrappers unless
        # we set PERL_EXT_CC
        env.set("PERL_EXT_CC", spack_cc)

    @classmethod
    def determine_version(cls, exe):
        # On CentOS and Ubuntu, the OS package info installs "info",
        # which satisfies spack external find, but "makeinfo" comes
        # from texinfo and may not be installed (and vice versa).
        (texinfo_path, info_exe) = os.path.split(exe)
        makeinfo_exe = os.path.join(texinfo_path, "makeinfo")
        if not os.path.exists(makeinfo_exe):
            return None
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"info \(GNU texinfo\)\s+(\S+)", output)
        return match.group(1) if match else None
