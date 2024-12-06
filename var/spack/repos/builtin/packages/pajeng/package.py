# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pajeng(CMakePackage):
    """PajeNG is a re-implementation of the well-known Paje visualization
    tool for the analysis of execution traces.  PajeNG comprises the
    libpaje library, and an auxiliary tool called pj_dump to transform
    Paje trace files to Comma-Separated Value (CSV). The space-time
    visualization tool called pajeng had been deprecated (removed from
    the sources) since modern tools do a better job (see pj_gantt)."""

    homepage = "https://github.com/schnorr/pajeng"
    git = "https://github.com/schnorr/pajeng.git"
    url = "https://github.com/schnorr/pajeng/archive/1.3.6.tar.gz"

    maintainers("viniciusvgp", "schnorr")

    license("GPL-3.0-only")

    version("develop", git="https://github.com/schnorr/pajeng.git")
    version("1.3.6", sha256="1a2722bfaeb0c6437fb9e8efc2592edbf14ba01172f97e01c7839ffea8b9d0b3")
    version("1.3.5", sha256="ea8ca02484de4091dcf57289724876ec17dd98e3a032dc609b7ea020ca2629eb")
    version("1.3.4", sha256="284e9a590a2861251e808542663bf1b77bc2c99650a1fbf945cd5bab65402f9e")
    version("1.3.3", sha256="42cf44003d238fd5c4ab512bdeb445fc12f7e3bd3f0526b389f080c84b83b19f")
    version("1.3.2", sha256="97154415a22f9b7f83516e988ea664b3990377d69fca859275ca48d7bfad0932")
    version("1.3.1", sha256="4bc3764aaa7e79da9a81f40c0593b646007b689e4ac20886d06f271ce0fa0a60")
    version("1.3", sha256="781b8be935e10b65470207f4f179bb1196aa6740547f9f1af0cb1c0193f11c6f")
    version("1.1", sha256="986d03e6deed20a3b9d0e076b1be9053c1bc86c8b41ca36cce3ba3b22dc6abca")
    version("1.0", sha256="4d98d1a78669290d0a2e6bfe07a1eb4ab96bd05e5ef78da96d2c3cf03b023aa0")

    depends_on("cxx", type="build")  # generated

    variant("static", default=False, description="Build as static library")
    variant("doc", default=False, description="The Paje Trace File documentation")
    variant("lib", default=True, description="Build libpaje")
    variant("tools", default=True, description="Build auxiliary tools")
    variant("gui", default=False, description="The PajeNG visualization tool")

    depends_on("boost+exception+regex")
    depends_on("flex")
    depends_on("bison")
    depends_on("qt@:4+opengl", when="@:1.3.2+gui")
    depends_on("freeglut", when="@:1.3.2+gui")
    depends_on("fmt", when="@develop")

    conflicts("+tools", when="~lib", msg="Enable libpaje to compile tools.")
    conflicts(
        "+gui",
        when="@1.3.3:",
        msg="PajeNG visualization tool is available only for versions up to 1.3.2.",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("STATIC_LINKING", "static"),
            self.define_from_variant("PAJE_DOC", "doc"),
            self.define_from_variant("PAJE_LIBRARY", "lib"),
            self.define_from_variant("PAJE_TOOLS", "tools"),
        ]

        if self.spec.satisfies("@:1.3.2"):
            args.extend(
                [
                    self.define_from_variant("PAJENG", "gui"),
                    self.define_from_variant("PAJE_UTILS_LIBRARY", "gui"),
                    self.define_from_variant("PJ_DUMP", "tools"),
                    self.define_from_variant("PJ_VALIDATE", "tools"),
                ]
            )

        return args

    @when("@1.1+lib")
    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("paje_library")
