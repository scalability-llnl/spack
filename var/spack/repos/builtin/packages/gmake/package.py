# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Gmake(Package, GNUMirrorPackage):
    """GNU Make is a tool which controls the generation of executables and
    other non-source files of a program from the program's source files."""

    homepage = "https://www.gnu.org/software/make/"
    gnu_mirror_path = "make/make-4.2.1.tar.gz"
    maintainers("haampie")

    license("GPL-3.0-only")

    # Stable releases
    version("4.4.1", sha256="dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3")
    version("4.4", sha256="581f4d4e872da74b3941c874215898a7d35802f03732bdccee1d4a7979105d18")
    version("4.3", sha256="e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19")
    version("4.2.1", sha256="e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7")
    version("4.1", sha256="9fc7a9783d3d2ea002aa1348f851875a2636116c433677453cc1d1acc3fc4d55")
    version(
        "4.0",
        deprecated=True,
        sha256="fc42139fb0d4b4291929788ebaf77e2a4de7eaca95e31f3634ef7d4932051f69",
    )

    depends_on("c", type="build")  # generated

    variant("guile", default=False, description="Support GNU Guile for embedded scripting")

    with when("+guile"):
        depends_on("guile@:2.0", when="@:4.2")
        depends_on("guile@:3.0")
        depends_on("pkgconfig", type="build")

    patch(
        "https://src.fedoraproject.org/rpms/make/raw/519a7c5bcbead22e6ea2d2c2341d981ef9e25c0d/f/make-4.2.1-glob-fix-2.patch",
        level=1,
        sha256="fe5b60d091c33f169740df8cb718bf4259f84528b42435194ffe0dd5b79cd125",
        when="@4.2.1",
    )
    patch(
        "https://src.fedoraproject.org/rpms/make/raw/519a7c5bcbead22e6ea2d2c2341d981ef9e25c0d/f/make-4.2.1-glob-fix-3.patch",
        level=1,
        sha256="ca60bd9c1a1b35bc0dc58b6a4a19d5c2651f7a94a4b22b2c5ea001a1ca7a8a7f",
        when="@:4.2.1",
    )

    # Avoid symlinking GNUMakefile to GNUMakefile
    build_directory = "spack-build"

    # See https://savannah.gnu.org/bugs/?57962
    patch("findprog-in-ignore-directories.patch", when="@4.3")

    tags = ["build-tools"]

    executables = ["^make$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU Make (\S+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        return [
            "--with-guile" if self.spec.satisfies("+guile") else "--without-guile",
            "--disable-nls",
            # configure needs make to enable dependency tracking, disable explicitly
            "--disable-dependency-tracking",
        ]

    def install(self, spec, prefix):
        configure = Executable(join_path(self.stage.source_path, "configure"))
        with working_dir(self.build_directory, create=True):
            configure(f"--prefix={prefix}", *self.configure_args())
            if spec.satisfies("@:4.2.1"):  # generated files in build dir
                build_sh = join_path(".", "build.sh")
                config_h = join_path(".", "config.h")
            else:  # generated files in source dir
                build_sh = join_path(self.stage.source_path, "build.sh")
                config_h = join_path("src", "config.h")
            # The default CXX value should be generic, not CXX from the current build as it points
            # to the compiler wrapper by absolute path.
            filter_file(r"^#define MAKE_CXX .*$", "#undef MAKE_CXX", config_h)
            Executable(build_sh)()
            os.mkdir(prefix.bin)
            install("make", prefix.bin)
            os.symlink("make", prefix.bin.gmake)

    def setup_dependent_package(self, module, dspec):
        module.make = MakeExecutable(
            self.spec.prefix.bin.make, determine_number_of_jobs(parallel=dspec.package.parallel)
        )
