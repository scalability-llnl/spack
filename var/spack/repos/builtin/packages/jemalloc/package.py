# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jemalloc(AutotoolsPackage):
    """jemalloc is a general purpose malloc(3) implementation that emphasizes
    fragmentation avoidance and scalable concurrency support."""

    homepage = "http://jemalloc.net/"
    url = "https://github.com/jemalloc/jemalloc/releases/download/4.0.4/jemalloc-4.0.4.tar.bz2"

    license("BSD-2-Clause")

    version("5.3.0", sha256="2db82d1e7119df3e71b7640219b6dfe84789bc0537983c3b7ac4f7189aecfeaa")
    version("5.2.1", sha256="34330e5ce276099e2e8950d9335db5a875689a4c6a56751ef3b1d8c537f887f6")
    version("5.2.0", sha256="74be9f44a60d2a99398e706baa921e4efde82bf8fd16e5c0643c375c5851e3b4")
    version("4.5.0", sha256="9409d85664b4f135b77518b0b118c549009dc10f6cba14557d170476611f6780")
    version("4.4.0", sha256="a7aea63e9718d2f1adf81d87e3df3cb1b58deb86fc77bad5d702c4c59687b033")
    version("4.3.1", sha256="f7bb183ad8056941791e0f075b802e8ff10bd6e2d904e682f87c8f6a510c278b")
    version("4.2.1", sha256="5630650d5c1caab95d2f0898de4fe5ab8519dc680b04963b38bb425ef6a42d57")
    version("4.2.0", sha256="b216ddaeb901697fe38bd30ea02d7505a4b60e8979092009f95cfda860d46acb")
    version("4.1.0", sha256="fad06d714f72adb4265783bc169c6d98eeb032d57ba02d87d1dcb4a2d933ec8e")
    version("4.0.4", sha256="3fda8d8d7fcd041aa0bebbecd45c46b28873cf37bd36c56bf44961b36d0f42d0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("stats", default=False, description="Enable heap statistics")
    variant("prof", default=False, description="Enable heap profiling")
    variant(
        "jemalloc_prefix",
        default="none",
        description="Prefix to prepend to all public APIs",
        values=None,
        multi=False,
    )
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant("documentation", default=False, description="Build documentation")
    variant("debug", default=False, description="Build debugging code")
    variant("fill", default=True, description="Enable or disable support for junk/zero filling")

    def configure_args(self):
        spec = self.spec
        args = []

        if "+stats" in spec:
            args.append("--enable-stats")
        if "+prof" in spec:
            args.append("--enable-prof")

        je_prefix = spec.variants["jemalloc_prefix"].value
        if je_prefix != "none":
            args.append("--with-jemalloc-prefix={0}".format(je_prefix))

        args += self.enable_or_disable("libs")
        args += self.enable_or_disable("documentation")
        args += self.enable_or_disable("debug")
        args += self.enable_or_disable("fill")
        return args
