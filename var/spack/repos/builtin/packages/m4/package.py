# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class M4(AutotoolsPackage, GNUMirrorPackage):
    """GNU M4 is an implementation of the traditional Unix macro processor."""

    homepage = "https://www.gnu.org/software/m4/m4.html"
    gnu_mirror_path = "m4/m4-1.4.18.tar.gz"

    license("GPL-3.0-or-later")

    version("1.4.19", sha256="3be4a26d825ffdfda52a56fc43246456989a3630093cced3fbddf4771ee58a70")
    version("1.4.18", sha256="ab2633921a5cd38e48797bf5521ad259bdc4b979078034a3b790d7fec5493fab")
    version("1.4.17", sha256="3ce725133ee552b8b4baca7837fb772940b25e81b2a9dc92537aeaf733538c9e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("gnulib-pgi.patch", when="@1.4.18")
    patch("pgi.patch", when="@1.4.17")
    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    patch("nvhpc.patch", when="@1.4.18 %nvhpc")
    patch("nvhpc-1.4.19.patch", when="@1.4.19 %nvhpc")
    # Workaround bug where __LONG_WIDTH__ is not defined
    patch("nvhpc-long-width.patch", when="@1.4.19 %nvhpc")
    patch("oneapi.patch", when="@1.4.18 %oneapi")
    # from: https://github.com/Homebrew/homebrew-core/blob/master/Formula/m4.rb
    # Patch credit to Jeremy Huddleston Sequoia <jeremyhu@apple.com>
    patch("secure_snprintf.patch", when="@:1.4.18 os=highsierra")
    patch("secure_snprintf.patch", when="@:1.4.18 os=mojave")
    patch("secure_snprintf.patch", when="@:1.4.18 os=catalina")
    patch("secure_snprintf.patch", when="@:1.4.18 os=bigsur")
    # https://bugzilla.redhat.com/show_bug.cgi?id=1573342
    patch(
        "https://src.fedoraproject.org/rpms/m4/raw/5d147168d4b93f38a4833f5dd1d650ad88af5a8a/f/m4-1.4.18-glibc-change-work-around.patch",
        sha256="fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8",
        when="@1.4.18",
    )
    # from: https://www.mail-archive.com/m4-patches@gnu.org/msg01208.html
    # tests: Fix failing test checks/198.sysval with upstream patch for doc/m4.texi
    patch("checks-198.sysval.1.patch", when="@1.4.19")
    patch("checks-198.sysval.2.patch", when="@1.4.19")

    variant("sigsegv", default=True, description="Build the libsigsegv dependency")

    depends_on("diffutils", type="build")
    depends_on("libsigsegv", when="+sigsegv")

    build_directory = "spack-build"

    tags = ["build-tools"]

    executables = ["^g?m4$"]

    @when("@1.4.19")
    def patch(self):
        """skip texinfo of m4.info for patched m4.texi (patched only a test in it)"""
        timestamp = os.path.getmtime("doc/m4.info")
        os.utime("doc/m4.texi", (timestamp, timestamp))

    @classmethod
    def determine_version(cls, exe):
        # Output on macOS:
        #   GNU M4 1.4.6
        # Output on Linux:
        #   m4 (GNU M4) 1.4.18
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU M4\)?\s+(\S+)", output)
        return match.group(1) if match else None

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Inform autom4te if it wasn't built correctly (some external
        # installations such as homebrew). See
        # https://www.gnu.org/software/autoconf/manual/autoconf-2.67/html_node/autom4te-Invocation.html
        env.set("M4", self.prefix.bin.m4)

    def setup_build_environment(self, env):
        # The default optimization level for icx/icpx is "-O2",
        # but building m4 with this level breaks the build of dependents.
        # So we set it explicitely to "-O0".
        if self.spec.satisfies("%intel") or self.spec.satisfies("%oneapi"):
            env.append_flags("CFLAGS", "-O0")

    def setup_run_environment(self, env):
        env.set("M4", self.prefix.bin.m4)

    def configure_args(self):
        spec = self.spec
        args = ["--enable-c++"]

        if spec.satisfies("%cce@9:"):
            args.append("LDFLAGS=-rtlib=compiler-rt")

        if (
            spec.satisfies("%clang")
            or spec.satisfies("%aocc")
            or spec.satisfies("%arm")
            or spec.satisfies("%fj")
        ) and not spec.satisfies("platform=darwin"):
            args.append("LDFLAGS=-rtlib=compiler-rt")

        if spec.satisfies("%intel@:18"):
            args.append("CFLAGS=-no-gcc")

        if "+sigsegv" in spec:
            args.append("--with-libsigsegv-prefix={0}".format(spec["libsigsegv"].prefix))
        else:
            args.append("--without-libsigsegv-prefix")

        # https://lists.gnu.org/archive/html/bug-m4/2016-09/msg00002.html
        arch = spec.architecture
        if arch.platform == "darwin" and arch.os == "sierra" and "%gcc" in spec:
            args.append("ac_cv_type_struct_sched_param=yes")

        return args

    def test_version(self):
        """ensure m4 version matches installed spec"""
        m4 = which(self.prefix.bin.m4)
        out = m4("--version", output=str.split, error=str.split)
        assert str(self.spec.version) in out

    def test_hello(self):
        """ensure m4 hello example runs"""
        test_data_dir = self.test_suite.current_test_data_dir
        hello_file = test_data_dir.join("hello.m4")
        m4 = which(self.prefix.bin.m4)
        out = m4(hello_file, output=str.split, error=str.split)

        expected = get_escaped_text_output(test_data_dir.join("hello.out"))
        check_outputs(expected, out)
