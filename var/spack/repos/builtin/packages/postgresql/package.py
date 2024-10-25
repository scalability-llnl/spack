# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Postgresql(AutotoolsPackage):
    """PostgreSQL is a powerful, open source object-relational database system.
    It has more than 15 years of active development and a proven architecture
    that has earned it a strong reputation for reliability, data integrity, and
    correctness."""

    homepage = "https://www.postgresql.org/"
    url = "https://ftp.postgresql.org/pub/source/v9.3.4/postgresql-9.3.4.tar.bz2"
    list_url = "http://ftp.postgresql.org/pub/source"
    list_depth = 1

    license("PostgreSQL")

    version("16.4", sha256="971766d645aa73e93b9ef4e3be44201b4f45b5477095b049125403f9f3386d6f")
    version("16.3", sha256="331963d5d3dc4caf4216a049fa40b66d6bcb8c730615859411b9518764e60585")
    version("15.8", sha256="4403515f9a69eeb3efebc98f30b8c696122bfdf895e92b3b23f5b8e769edcb6a")
    version("15.2", sha256="99a2171fc3d6b5b5f56b757a7a3cb85d509a38e4273805def23941ed2b8468c7")
    version("14.13", sha256="59aa3c4b495ab26a9ec69f3ad0a0228c51f0fe6facf3634dfad4d1197d613a56")
    version("14.0", sha256="ee2ad79126a7375e9102c4db77c4acae6ae6ffe3e082403b88826d96d927a122")
    version("13.16", sha256="c9cbbb6129f02328204828066bb3785c00a85c8ca8fd329c2a8a53c1f5cd8865")
    version("13.1", sha256="12345c83b89aa29808568977f5200d6da00f88a035517f925293355432ffe61f")
    version("12.20", sha256="2d543af3009fec7fd5af35f7a70c95085d3eef6b508e517aa9493e99b15e9ea9")
    version("12.2", sha256="ad1dcc4c4fc500786b745635a9e1eba950195ce20b8913f50345bb7d5369b5de")
    version("11.2", sha256="2676b9ce09c21978032070b6794696e0aa5a476e3d21d60afc036dc0a9c09405")
    version("11.1", sha256="90815e812874831e9a4bf6e1136bf73bc2c5a0464ef142e2dfea40cda206db08")
    version("11.0", sha256="bf9bba03d0c3902c188af12e454b35343c4a9bf9e377ec2fe50132efb44ef36b")
    version("10.7", sha256="bfed1065380c1bba927bfe51f23168471373f26e3324cbad859269cc32733ede")
    version("10.6", sha256="68a8276f08bda8fbefe562faaf8831cb20664a7a1d3ffdbbcc5b83e08637624b")
    version("10.5", sha256="6c8e616c91a45142b85c0aeb1f29ebba4a361309e86469e0fb4617b6a73c4011")
    version("10.4", sha256="1b60812310bd5756c62d93a9f93de8c28ea63b0df254f428cd1cf1a4d9020048")
    version("10.3", sha256="6ea268780ee35e88c65cdb0af7955ad90b7d0ef34573867f223f14e43467931a")
    version("10.2", sha256="fe32009b62ddb97f7f014307ce9d0edb6972f5a698e63cb531088e147d145bad")
    version("10.1", sha256="3ccb4e25fe7a7ea6308dea103cac202963e6b746697366d72ec2900449a5e713")
    version("10.0", sha256="712f5592e27b81c5b454df96b258c14d94b6b03836831e015c65d6deeae57fd1")
    version("9.6.12", sha256="2e8c8446ba94767bda8a26cf5a2152bf0ae68a86aaebf894132a763084579d84")
    version("9.6.11", sha256="38250adc69a1e8613fb926c894cda1d01031391a03648894b9a6e13ff354a530")
    version("9.5.3", sha256="7385c01dc58acba8d7ac4e6ad42782bd7c0b59272862a3a3d5fe378d4503a0b4")
    version("9.3.4", sha256="9ee819574dfc8798a448dc23a99510d2d8924c2f8b49f8228cd77e4efc8a6621")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("client_only", default=False, description="Build and install client only.")
    variant("threadsafe", default=False, description="Build with thread safe.")
    variant(
        "lineedit",
        default="readline",
        values=("readline", "libedit", "none"),
        multi=False,
        description="Line editing library",
    )
    variant("python", default=False, description="Enable Python bindings.")
    variant("perl", default=False, description="Enable Perl bindings.")
    variant("tcl", default=False, description="Enable Tcl bindings.")
    variant("gssapi", default=False, description="Build with GSSAPI functionality.")
    variant("xml", default=False, description="Build with XML support.")
    variant("icu", default=True, description="Build with ICU support.", when="@16:")

    depends_on("icu4c", when="@16: +icu")
    depends_on("readline", when="lineedit=readline")
    depends_on("libedit", when="lineedit=libedit")
    depends_on("openssl")
    depends_on("tcl", when="+tcl")
    depends_on("perl+opcode", when="+perl")
    depends_on("python", when="+python")
    depends_on("libxml2", when="+xml")

    @property
    def command(self):
        return Executable(self.prefix.bin.pg_config)

    def configure_args(self):
        spec = self.spec
        args = ["--with-openssl"]

        args.extend(self.enable_or_disable("thread-safety", variant="threadsafe"))

        if spec.variants["lineedit"].value == "libedit":
            args.append("--with-libedit-preferred")
        elif spec.variants["lineedit"].value == "none":
            args.append("--without-readline")

        if spec.satisfies("+gssapi"):
            args.append("--with-gssapi")

        if spec.satisfies("+python"):
            args.append("--with-python")

        if spec.satisfies("+perl"):
            args.append("--with-perl")

        if spec.satisfies("+tcl"):
            args.append("--with-tcl")

        if spec.satisfies("+xml"):
            args.append("--with-libxml")

        if spec.satisfies("~icu"):
            args.append("--without-icu")

        return args

    def install(self, spec, prefix):
        if spec.satisfies("+client_only"):
            for subdir in ("bin", "include", "interfaces", "pl"):
                with working_dir(os.path.join("src", subdir)):
                    make("install")
        else:
            super().install(spec, prefix)

    def setup_run_environment(self, env):
        spec = self.spec

        if spec.satisfies("+perl"):
            env.prepend_path("PERL5LIB", self.prefix.lib)
        if spec.satisfies("+tcl"):
            env.prepend_path("TCLLIBPATH", self.prefix.lib)
        if spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        spec = self.spec

        if spec.satisfies("+perl"):
            env.prepend_path("PERL5LIB", self.prefix.lib)
        if spec.satisfies("+tcp"):
            env.prepend_path("TCLLIBPATH", self.prefix.lib)
        if spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        spec = self.spec

        if spec.satisfies("+perl"):
            env.prepend_path("PERL5LIB", self.prefix.lib)
        if spec.satisfies("+tcl"):
            env.prepend_path("TCLLIBPATH", self.prefix.lib)
        if spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.prefix.lib)

    @property
    def libs(self):
        stat_libs = [
            "libecpg_compat",
            "libecpg",
            "libpgcommon",
            "libpgcommon_shlib",
            "libpgfeutils",
            "libpgport",
            "libpgport_shlib",
            "libpgtypes",
            "libpq",
        ]
        fl_stat = find_libraries(stat_libs, self.prefix, shared=False, recursive=True)

        dyn_libs = [
            "libecpg_compat",
            "libecpg",
            "libpgtypes",
            "libpq",
            "libpqwalreceiver",
            "plpgsql",
            "pgoutput",
        ]
        if "+perl" in self.spec:
            dyn_libs.append("plperl")
        if "+python" in self.spec:
            dyn_libs.append("plpython")
        if "+tcl" in self.spec:
            dyn_libs.append("pltcl")

        fl_dyn = find_libraries(dyn_libs, self.prefix, shared=True, recursive=True)

        return fl_dyn + fl_stat
