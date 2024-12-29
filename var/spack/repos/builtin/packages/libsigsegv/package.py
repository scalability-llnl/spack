# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Libsigsegv(AutotoolsPackage, GNUMirrorPackage):
    """GNU libsigsegv is a library for handling page faults in user mode."""

    homepage = "https://www.gnu.org/software/libsigsegv/"
    gnu_mirror_path = "libsigsegv/libsigsegv-2.13.tar.gz"

    test_requires_compiler = True

    license("GPL-2.0-or-later")

    version("2.14", sha256="cdac3941803364cf81a908499beb79c200ead60b6b5b40cad124fd1e06caa295")
    version("2.13", sha256="be78ee4176b05f7c75ff03298d84874db90f4b6c9d5503f0da1226b3a3c48119")
    version("2.12", sha256="3ae1af359eebaa4ffc5896a1aee3568c052c99879316a1ab57f8fe1789c390b6")
    version("2.11", sha256="dd7c2eb2ef6c47189406d562c1dc0f96f2fc808036834d596075d58377e37a18")
    version("2.10", sha256="8460a4a3dd4954c3d96d7a4f5dd5bc4d9b76f5754196aa245287553b26d2199a")

    depends_on("c", type="build")  # generated

    patch("new_config_guess.patch", when="@2.10")

    def configure_args(self):
        return ["--enable-shared"]

    extra_install_tests = "tests/.libs"

    @run_after("install")
    def setup_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, self.extra_install_tests)

    def test_smoke_test(self):
        """build and run smoke test"""
        data_dir = self.test_suite.current_test_data_dir
        prog = "smoke_test"
        src = data_dir.join("{0}.c".format(prog))

        options = [
            "-I{0}".format(self.prefix.include),
            src,
            "-o",
            prog,
            "-L{0}".format(self.prefix.lib),
            "-lsigsegv",
            "{0}{1}".format(self.compiler.cc_rpath_arg, self.prefix.lib),
        ]

        cc = which(os.environ["CC"])
        cc(*options)

        exe = which(prog)
        out = exe(output=str.split, error=str.split)
        expected = get_escaped_text_output(data_dir.join("smoke_test.out"))
        check_outputs(expected, out)
