# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dock(Package):
    """DOCK is a molecular docking program used in drug discovery.

    This program, given a protein binding site and a small molecule, tries
    to predict the correct binding mode of the small molecule in the binding
    site, and the associated binding energy."""

    homepage = "http://dock.compbio.ucsf.edu/DOCK_6/index.htm"
    url = "file://{0}/dock.6.9_source.tar.gz".format(os.getcwd())
    maintainers("snehring")
    manual_download = True

    version("6.9", sha256="c2caef9b4bb47bb0cb437f6dc21f4c605fd3d0d9cc817fa13748c050dc87a5a8")

    variant("mpi", default=True, description="Enable mpi")

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("mpi", when="+mpi")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+mpi"):
            env.set("MPICH_HOME", self.spec["mpi"].prefix)

    def install(self, spec, prefix):
        compiler_targets = {"gcc": "gnu", "intel": "intel", "pgi": "pgi", "sgi": "sgi"}

        if self.compiler.name not in compiler_targets:
            template = "Unsupported compiler {0}! Supported compilers: {1}"
            err = template.format(self.compiler.name, ", ".join(list(compiler_targets.keys())))

            raise InstallError(err)

        if self.compiler.name == "pgi" and "+mpi" in spec:
            raise InstallError("Parallel output is not supported with pgi.")

        with working_dir("install"):
            sh_args = ["./configure", compiler_targets[self.compiler.name]]
            config_source = compiler_targets[self.compiler.name]

            if spec.satisfies("+mpi"):
                sh_args.append("parallel")
                config_source = config_source + ".parallel"

            if self.spec.satisfies("@6.9%gcc@10:"):
                # Versions of gcc before 10 treat mismatched arguments as a warning
                # 10+ makes it an error. This makes it a warning again
                filter_file(
                    r"(-fno-second-underscore)", r"\1 -fallow-argument-mismatch", config_source
                )

            which("sh")(*sh_args)
            which("make")("YACC=bison -o y.tab.c")

        mkdirp(prefix.bin)
        install_tree("bin", prefix.bin)
