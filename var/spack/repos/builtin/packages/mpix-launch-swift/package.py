# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MpixLaunchSwift(MakefilePackage):
    """Library that allows a child MPI application to be launched
    inside a subset of processes in a parent MPI application.
    """

    homepage = "https://bitbucket.org/kshitijvmehta/mpix_launch_swift"
    git = "https://kshitijvmehta@bitbucket.org/kshitijvmehta/mpix_launch_swift.git"

    version("develop", branch="envs")

    depends_on("c", type="build")  # generated

    depends_on("stc")
    depends_on("tcl")
    depends_on("mpi")
    depends_on("swig", type="build")

    def install(self, spec, prefix):
        install_tree(".", prefix)
