# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.package import *


class Automake(AutotoolsPackage, GNUMirrorPackage):
    """Automake -- make file builder part of autotools"""

    homepage = "https://www.gnu.org/software/automake/"
    gnu_mirror_path = "automake/automake-1.15.tar.gz"

    license("GPL-2.0-or-later")

    version("1.16.5", sha256="07bd24ad08a64bc17250ce09ec56e921d6343903943e99ccf63bbf0705e34605")
    version("1.16.3", sha256="ce010788b51f64511a1e9bb2a1ec626037c6d0e7ede32c1c103611b9d3cba65f")
    version("1.16.2", sha256="b2f361094b410b4acbf4efba7337bdb786335ca09eb2518635a09fb7319ca5c1")
    version("1.16.1", sha256="608a97523f97db32f1f5d5615c98ca69326ced2054c9f82e65bade7fc4c9dea8")
    version("1.15.1", sha256="988e32527abe052307d21c8ca000aa238b914df363a617e38f4fb89f5abf6260")
    version("1.15", sha256="7946e945a96e28152ba5a6beb0625ca715c6e32ac55f2e353ef54def0c8ed924")
    version("1.14.1", sha256="814c2333f350ce00034a1fe718e0e4239998ceea7b0aff67e9fd273ed6dfc23b")
    version("1.13.4", sha256="4c93abc0bff54b296f41f92dd3aa1e73e554265a6f719df465574983ef6f878c")
    version("1.11.6", sha256="53dbf1945401c43f4ce19c1971baecdbf8bc32e0f37fa3f49fe7b6992d0d2030")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("perl+threads", type=("build", "run"))

    build_directory = "spack-build"

    tags = ["build-tools"]

    executables = ["^automake$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU automake\)\s+(\S+)", output)
        return match.group(1) if match else None

    def patch(self):
        # The full perl shebang might be too long
        files_to_be_patched_fmt = "bin/{0}.in"
        if self.spec.satisfies("@:1.15.1"):
            files_to_be_patched_fmt = "t/wrap/{0}.in"

        if self.spec.satisfies("@1.16.3:"):
            shebang_string = "^#!@PERL@"
        else:
            shebang_string = "^#!@PERL@ -w"

        for file in ("aclocal", "automake"):
            filter_file(
                shebang_string, "#!/usr/bin/env perl", files_to_be_patched_fmt.format(file)
            )

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # Automake is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = ["aclocal", "automake"]
        for name in executables:
            setattr(module, name, self._make_executable(name))
