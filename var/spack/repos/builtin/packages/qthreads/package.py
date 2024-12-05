# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


def is_integer(x):
    """Any integer value"""

    try:
        return float(x).is_integer()
    except ValueError:
        return False


class Qthreads(AutotoolsPackage):
    """The qthreads API is designed to make using large numbers of
    threads convenient and easy, and to allow portable access to
    threading constructs used in massively parallel shared memory
    environments. The API maps well to both MTA-style threading and
    PIM-style threading, and we provide an implementation of this
    interface in both a standard SMP context as well as the SST
    context. The qthreads API provides access to full/empty-bit
    (FEB) semantics, where every word of memory can be marked
    either full or empty, and a thread can wait for any word to
    attain either state."""

    homepage = "http://www.cs.sandia.gov/qthreads/"

    test_requires_compiler = True
    test_base_path = join_path("test", "basics")

    tags = ["e4s"]

    version("1.18", sha256="d1a808b35d3af0012194a8f3afe72241dfcffca7e88a7104fa02a46c73022880")
    version("1.17", sha256="b17efb3c94c2027b8edd759584f4b1fa1e2725f1878a7a098d7bc58ad38d82f1")
    version("1.16", sha256="923d58f3ecf7d838a18c3616948ea32ddace7196c6805518d052c51a27219970")
    version("1.15", sha256="3ac2dc24debff004a2998933de5724b1e14e1ae262fa9942acbb01f77819a23b")
    version("1.14", sha256="16f15e5b2e35b6329a857d24c283a1e43cd49921ee49a1446d4f31bf9c6f5cf9")
    version("1.12", sha256="2c13a5f6f45bc2f22038d272be2e748e027649d3343a9f824da9e86a88b594c9")
    version("1.11", sha256="dbde6c7cb7de7e89921e47363d09cecaebf775c9d090496c2be8350355055571")
    version("1.10", sha256="29fbc2e54bcbc814c1be13049790ee98c505f22f22ccee34b7c29a4295475656")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("restrict.patch", when="@:1.10")
    patch("trap.patch", when="@:1.10")

    variant("hwloc", default=True, description="hwloc support")
    variant("spawn_cache", default=False, description="enables worker specific cache of spawns")
    variant(
        "scheduler",
        default="nemesis",
        values=("nemesis", "lifo", "mutexfifo", "mtsfifo", "sherwood", "distrib", "nottingham"),
        multi=False,
        description="Specify which scheduler policy to use",
    )
    variant("static", default=True, description="Build static library")
    variant(
        "stack_size",
        default=4096,
        description="Specify number of bytes to use in a stack",
        values=is_integer,
    )

    depends_on("hwloc@1.0:1", when="@:1.15 +hwloc")
    depends_on("hwloc@1.5:2", when="@1.16: +hwloc")

    def url_for_version(self, version):
        # if version is greater than 1.17, use new default
        if version >= Version("1.17"):
            url_fmt = (
                "https://github.com/Qthreads/qthreads/releases/download/{0}/qthread-{0}.tar.gz"
            )
        # otherwise, use .bz2 file format
        else:
            url_fmt = (
                "https://github.com/Qthreads/qthreads/releases/download/{0}/qthread-{0}.tar.bz2"
            )
        return url_fmt.format(version)

    def configure_args(self):
        spec = self.spec
        if "+hwloc" in self.spec:
            args = [
                "--enable-guard-pages",
                "--with-topology=hwloc",
                "--with-hwloc=%s" % spec["hwloc"].prefix,
            ]
        else:
            args = ["--with-topology=no"]

        if "+spawn_cache" in self.spec:
            args.append("--enable-spawn-cache")
        else:
            args.append("--disable-spawn-cache")

        if "+static" in self.spec:
            args.append("--enable-static=yes")
        else:
            args.append("--enable-static=no")

        args.append("--with-default-stack-size=%s" % self.spec.variants["stack_size"].value)

        args.append("--with-scheduler=%s" % self.spec.variants["scheduler"].value)
        return args

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [join_path("test", "argparsing.h"), self.test_base_path])

    def _build_and_run_test(self, test):
        """Build and run the test."""
        test_root = install_test_root(self)
        options = [
            f"-I{self.prefix.include}",
            f"-I{join_path(test_root, 'test')}",
            join_path(test_root, self.test_base_path, f"{test}.c"),
            "-o",
            test,
            f"-L{self.prefix.lib}",
            "-lqthread",
            f"{self.compiler.cc_rpath_arg}{self.prefix.lib}",
        ]
        cc = which(os.environ["CC"])
        cc(*options)

        exe = which(join_path(".", test))
        exe()

    def test_hello_world(self):
        """build and run hello_world"""
        self._build_and_run_test("hello_world")

    def test_hello_world_multi(self):
        """build and run hello_world_multi"""
        self._build_and_run_test("hello_world_multi")

    def test_qthread_id(self):
        """build and run qthread_id"""
        self._build_and_run_test("qthread_id")
