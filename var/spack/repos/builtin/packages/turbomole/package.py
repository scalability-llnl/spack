# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

from spack.package import *


class Turbomole(Package):
    """TURBOMOLE: Program Package for ab initio Electronic Structure
    Calculations.

    Note: Turbomole requires purchase of a license to download. Go to the
    Turbomole home page, http://www.turbomole-gmbh.com, for details.
    Spack will search the current directory for this file. It is
    probably best to add this file to a Spack mirror so that it can be
    found from anywhere.  For information on setting up a Spack mirror
    see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "http://www.turbomole-gmbh.com/"
    manual_download = True

    version(
        "7.0.2",
        md5="92b97e1e52e8dcf02a4d9ac0147c09d6",
        url="file://%s/turbolinux702.tar.gz" % os.getcwd(),
    )

    variant("mpi", default=True, description="Set up MPI environment")
    variant("smp", default=False, description="Set up SMP environment")

    # Turbomole's install is odd. There are three variants
    # - serial
    # - parallel, MPI
    # - parallel, SMP
    #
    # Only one of these can be active at a time. MPI and SMP are set as
    # variants so there could be up to 3 installs per version. Switching
    # between them would be accomplished with `module swap` commands.

    def do_fetch(self, mirror_only=True):
        if "+mpi" in self.spec and "+smp" in self.spec:
            raise InstallError("Can not have both SMP and MPI enabled in the " "same build.")
        super().do_fetch(mirror_only)

    def get_tm_arch(self):
        if "TURBOMOLE" in os.getcwd():
            tm_sysname = Executable("./scripts/sysname")
            tm_arch = tm_sysname(output=str)
            return tm_arch.rstrip("\n")
        else:
            return

    def install(self, spec, prefix):
        calculate_version = "calculate_2.4_linux64"
        molecontrol_version = "MoleControl_2.5"

        tm_arch = self.get_tm_arch()

        tar = which("tar")
        dst = join_path(prefix, "TURBOMOLE")

        tar("-x", "-z", "-f", "thermocalc.tar.gz")
        with working_dir("thermocalc"):
            subprocess.call("./install<<<y", shell=True)

        install_tree("basen", join_path(dst, "basen"))
        install_tree("cabasen", join_path(dst, "cabasen"))
        install_tree(calculate_version, join_path(dst, calculate_version))
        install_tree("cbasen", join_path(dst, "cbasen"))
        install_tree("DOC", join_path(dst, "DOC"))
        install_tree("jbasen", join_path(dst, "jbasen"))
        install_tree("jkbasen", join_path(dst, "jkbasen"))
        install_tree(molecontrol_version, join_path(dst, molecontrol_version))
        install_tree("parameter", join_path(dst, "parameter"))
        install_tree("perlmodules", join_path(dst, "perlmodules"))
        install_tree("scripts", join_path(dst, "scripts"))
        install_tree("smprun_scripts", join_path(dst, "smprun_scripts"))
        install_tree("structures", join_path(dst, "structures"))
        install_tree("thermocalc", join_path(dst, "thermocalc"))
        install_tree("TURBOTEST", join_path(dst, "TURBOTEST"))
        install_tree("xbasen", join_path(dst, "xbasen"))

        install("Config_turbo_env", dst)
        install("Config_turbo_env.tcsh", dst)
        install("README", dst)
        install("README_LICENSES", dst)
        install("TURBOMOLE_702_LinuxPC", dst)

        if "+mpi" in spec:
            install_tree("bin/%s_mpi" % tm_arch, join_path(dst, "bin", "%s_mpi" % tm_arch))
            install_tree("libso/%s_mpi" % tm_arch, join_path(dst, "libso", "%s_mpi" % tm_arch))
            install_tree(
                "mpirun_scripts/%s_mpi" % tm_arch,
                join_path(dst, "mpirun_scripts", "%s_mpi" % tm_arch),
            )
        elif "+smp" in spec:
            install_tree("bin/%s_smp" % tm_arch, join_path(dst, "bin", "%s_smp" % tm_arch))
            install_tree("libso/%s_smp" % tm_arch, join_path(dst, "libso", "%s_smp" % tm_arch))
            install_tree(
                "mpirun_scripts/%s_smp" % tm_arch,
                join_path(dst, "mpirun_scripts", "%s_smp" % tm_arch),
            )
        else:
            install_tree("bin/%s" % tm_arch, join_path(dst, "bin", tm_arch))
        if "+mpi" in spec or "+smp" in spec:
            install("mpirun_scripts/ccsdf12", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/dscf", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/grad", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/mpgrad", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/pnoccsd", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/rdgrad", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/ricc2", join_path(dst, "mpirun_scripts"))
            install("mpirun_scripts/ridft", join_path(dst, "mpirun_scripts"))

    def setup_run_environment(self, env):
        molecontrol_version = "MoleControl_2.5"

        tm_arch = self.get_tm_arch()

        env.set("TURBODIR", self.prefix.TURBOMOLE)
        env.set("MOLE_CONTROL", join_path(self.prefix, "TURBOMOLE", molecontrol_version))

        env.prepend_path("PATH", self.prefix.TURBOMOLE.thermocalc)
        env.prepend_path("PATH", self.prefix.TURBOMOLE.scripts)
        if "+mpi" in self.spec:
            env.set("PARA_ARCH", "MPI")
            env.prepend_path(
                "PATH", join_path(self.prefix, "TURBOMOLE", "bin", "%s_mpi" % tm_arch)
            )
        elif "+smp" in self.spec:
            env.set("PARA_ARCH", "SMP")
            env.prepend_path(
                "PATH", join_path(self.prefix, "TURBOMOLE", "bin", "%s_smp" % tm_arch)
            )
        else:
            env.prepend_path("PATH", join_path(self.prefix, "TURBOMOLE", "bin", tm_arch))
