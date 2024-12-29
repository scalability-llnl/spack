# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Autoconf(AutotoolsPackage, GNUMirrorPackage):
    """Autoconf -- system configuration part of autotools"""

    homepage = "https://www.gnu.org/software/autoconf/"
    gnu_mirror_path = "autoconf/autoconf-2.69.tar.gz"

    license("GPL-3.0-or-later WITH Autoconf-exception-3.0", when="@2.62:", checked_by="tgamblin")
    license("GPL-2.0-or-later WITH Autoconf-exception-2.0", when="@:2.59", checked_by="tgamblin")

    version("2.72", sha256="afb181a76e1ee72832f6581c0eddf8df032b83e2e0239ef79ebedc4467d92d6e")
    version("2.71", sha256="431075ad0bf529ef13cb41e9042c542381103e80015686222b8a9d4abef42a1c")
    version("2.70", sha256="f05f410fda74323ada4bdc4610db37f8dbd556602ba65bc843edb4d4d4a1b2b7")
    version("2.69", sha256="954bd69b391edc12d6a4a51a2dd1476543da5c6bbf05a95b59dc0dd6fd4c2969")
    version("2.62", sha256="83aa747e6443def0ebd1882509c53f5a2133f502ddefa21b3de141c433914bdd")
    version("2.59", sha256="9cd05c73c5fcb1f5ccae53dd6cac36bb8cb9c7b3e97ffae5a7c05c72594c88d8")

    # https://savannah.gnu.org/support/?110396
    patch(
        "https://git.savannah.gnu.org/cgit/autoconf.git/patch/?id=05972f49ee632cd98057a3caf82ebfb9574846da",
        sha256="eaa3f69d927a853313a0b06e2117c51adab6377a2278549b05abc5df93643e16",
        when="@2.70",
    )
    # Apply long-time released and already in-use upstream patches to fix test cases:
    # tests/foreign.at (Libtool): Be tolerant of 'quote' replacing the older `quote'
    patch(
        "https://mirrors.mit.edu/gentoo-portage/dev-build/autoconf/files/autoconf-2.69-fix-libtool-test.patch",
        sha256="7793209b33013dc0f81208718c68440c5aae80e7a1c4b8d336e382525af791a7",
        when="@2.69",
    )
    # Fix bin/autoscan.in for current perl releases (reported already in January 2013)
    patch(
        "https://mirrors.mit.edu/gentoo-portage/dev-build/autoconf/files/autoconf-2.69-perl-5.26.patch",
        sha256="35c449281546376449766f92d49fc121ca50e330e60fefcfc9be2af3253082c2",
        when="@2.62:2.69 ^perl@5.17:",
    )
    # Fix bin/autoheader.in for current perl relases not having "." in @INC:
    patch(
        "https://mirrors.mit.edu/gentoo-portage/dev-build/autoconf/files/autoconf-2.69-perl-5.26-2.patch",
        sha256="a49dd5bac3b62daa0ff688ab4d508d71dbd2f4f8d7e2a02321926346161bf3ee",
        when="@2.62:2.69 ^perl@5.17:",
    )

    # Note: m4 is not a pure build-time dependency of autoconf. m4 is
    # needed when autoconf runs, not only when autoconf is built.
    depends_on("m4@1.4.8:", type=("build", "run"), when="@2.72:")
    depends_on("m4@1.4.6:", type=("build", "run"), when="@:2.71")
    depends_on("perl", type=("build", "run"))

    build_directory = "spack-build"

    tags = ["build-tools"]

    executables = [
        "^autoconf$",
        "^autoheader$",
        "^autom4te$",
        "^autoreconf$",
        "^autoscan$",
        "^autoupdate$",
        "^ifnames$",
    ]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"\(GNU Autoconf\)\s+(\S+)", output)
        return match.group(1) if match else None

    def patch(self):
        # The full perl shebang might be too long; we have to fix this here
        # because autom4te is called during the build
        patched_file = "bin/autom4te.in"

        # We save and restore the modification timestamp of the file to prevent
        # regeneration of the respective man page:
        with keep_modification_time(patched_file):
            if self.spec.satisfies("@2.70:"):
                shebang_string = "^#! @PERL@"
            else:
                shebang_string = "^#! @PERL@ -w"
            filter_file(shebang_string, "#! /usr/bin/env perl", patched_file)
        if self.version == Version("2.62"):
            # skip help2man for patched autoheader.in and autoscan.in
            touch("man/autoheader.1")
            touch("man/autoscan.1")

    # make installcheck would execute the testsuite a 2nd time, skip it
    def installcheck(self):
        pass

    @run_after("install")
    def filter_sbang(self):
        # We have to do this after install because otherwise the install
        # target will try to rebuild the binaries (filter_file updates the
        # timestamps)

        if self.spec.satisfies("@2.70:"):
            shebang_string = "#! {0}"
        else:
            shebang_string = "#! {0} -w"

        # Revert sbang, so Spack's sbang hook can fix it up
        filter_file(
            "^#! /usr/bin/env perl",
            shebang_string.format(self.spec["perl"].command.path),
            self.prefix.bin.autom4te,
            backup=False,
        )

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # Autoconf is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = [
            "autoconf",
            "autoheader",
            "autom4te",
            "autoreconf",
            "autoscan",
            "autoupdate",
            "ifnames",
        ]
        for name in executables:
            setattr(module, name, self._make_executable(name))
