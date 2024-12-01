# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------------------

import os

from spack.package import *


class Cplex(Package):
    """The IBM ILOG CPLEX Optimization Studio consists of the CPLEX Optimizer
    for mathematical programming, the IBM ILOG CPLEX CP Optimizer for
    constraint programming, the Optimization Programming Language (OPL),
    and an integrated IDE."""

    homepage = "https://www.ibm.com/products/ilog-cplex-optimization-studio"
    manual_download = True

    maintainers("robgics")

    version(
        "12.10.0",
        sha256="cd530eb9c6d446bd18b5dc5a3d61070bfad92c3efd6565d2d8e31a2acfb496f7",
        expand=False,
    )
    version(
        "12.8.0",
        sha256="ce8a597a11c73a0a3d49f3fa82930c47b6ac2adf7bc6779ad197ff0355023838",
        expand=False,
    )

    phases = ["configure", "install"]

    def url_for_version(self, version):
        return "file://{0}/cplex_studio{1}.linux-x86-64.bin".format(
            os.getcwd(), version.up_to(2).joined
        )

    def configure(self, spec, prefix):
        config = {
            "LICENSE_ACCEPTED": "TRUE",
            "USER_INSTALL_DIR": prefix,
            "-fileOverwrite_{}/README.html".format(prefix): "Yes",
            "-fileOverwrite_{}/opl/oplide/oplide".format(prefix): "Yes",
            "-fileOverwrite_{}/Uninstall/symlinks-linux.sh".format(prefix): "Yes",
            "-fileOverwrite_{}/Uninstall/Uninstall.lax".format(prefix): "Yes",
        }

        # Store values requested by the installer in a file
        with open("installer.properties", "w") as input_file:
            for key in config:
                input_file.write("{0}={1}\n".format(key, config[key]))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix, "cplex/bin/x86-64_linux"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "cplex/bin/x86-64_linux"))
        env.prepend_path("MATLABPATH", join_path(self.prefix, "cplex/matlab/x86-64_linux"))
        env.prepend_path("MATLABPATH", join_path(self.prefix, "cplex/examples/src/matlab"))
        env.prepend_path("PATH", join_path(self.prefix, "cpoptimizer/bin/x86-64_linux"))
        env.prepend_path("PATH", join_path(self.prefix, "opl/oplide"))
        env.prepend_path("PATH", join_path(self.prefix, "opl/bin/x86-64_linux"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "opl/bin/x86-64_linux"))
        env.set("CPLEX_PATH", self.prefix)

    def install(self, spec, prefix):
        with open("myinstaller.sh", "w") as install_script:
            install_script.write("#!/bin/sh\n")
            install_script.write(
                "sh ./cplex_studio{0}.linux-x86-64.bin".format(spec.version.up_to(2).joined)
                + " -f "
                + join_path(self.stage.source_path, "installer.properties")
                + " -i silent\n"
            )
            install_script.write("\n")

        set_executable("./myinstaller.sh")

        installer = Executable("./myinstaller.sh")
        installer()
