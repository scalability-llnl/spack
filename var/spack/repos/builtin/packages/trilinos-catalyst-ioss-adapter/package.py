# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TrilinosCatalystIossAdapter(CMakePackage):
    """Adapter for Trilinos Seacas Ioss and Paraview Catalyst"""

    homepage = "https://trilinos.org/"
    git = "https://github.com/trilinos/Trilinos.git"

    version("develop", branch="develop")
    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("paraview+mpi+python")
    depends_on("gl", type="run")
    requires("^[virtuals=gl] osmesa", msg="OSMesa is required for paraview")
    depends_on("py-numpy", type=("build", "run"))
    # Here we avoid paraview trying to use netcdf-c~parallel-netcdf
    # which is netcdf-c's default, even though paraview depends on 'netcdf-c'
    # without any variants. Concretizer bug?
    depends_on("netcdf-c+parallel-netcdf")

    root_cmakelists_dir = join_path(
        "packages",
        "seacas",
        "libraries",
        "ioss",
        "src",
        "visualization",
        "ParaViewCatalystIossAdapter",
    )

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.python)

    def cmake_args(self):
        spec = self.spec
        options = []

        paraview_version = "paraview-%s" % spec["paraview"].version.up_to(2)

        options.extend(
            ["-DParaView_DIR:PATH=%s" % spec["paraview"].prefix + "/lib/cmake/" + paraview_version]
        )

        return options
