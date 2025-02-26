# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Plantuml(Package):
    """PlantUML is a highly versatile tool that facilitates the rapid
    and straightforward creation of a wide array of diagrams."""

    homepage = "https://plantuml.com"
    url = "https://github.com/plantuml/plantuml/releases/download/v1.2025.1/plantuml-lgpl-1.2025.1.jar"

    maintainers("greenc-FNAL", "knoepfel", "marcpaterno")

    license("LGPL-3.0-or-later", checked_by="greenc-FNAL")

    version(
        "1.2025.1",
        sha256="b08112f0c8ac2a2085c8c4a81ac9eac7bc5a3413a492c252cad4d39e473d9d6d",
        expand=False,
    )

    depends_on("java@8.0:", type="run")
    depends_on("graphviz", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        rename(glob.glob("plantuml-*.jar")[0], "plantuml.jar")
        install("plantuml.jar", prefix.bin)
        plantuml_wrapper = join_path(os.path.dirname(__file__), "plantuml")
        install(plantuml_wrapper, prefix.bin.plantuml)

    def setup_run_environment(self, env):
        env.set("PLANTUML_JAR_LOCATION", join_path(self.prefix.bin, "plantuml.jar"))
