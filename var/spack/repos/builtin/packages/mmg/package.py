# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.build_systems.cmake
from spack.package import *
from spack.util.executable import which


class Mmg(CMakePackage):
    """Mmg is an open source software for simplicial remeshing.
    It provides 3 applications and 4 libraries:
    - the mmg2d application and the libmmg2d library: adaptation
      and optimization of a two-dimensional triangulation and
      generation of a triangulation from a set of points or
      from given boundary edges
    - the mmgs application and the libmmgs library: adaptation
      and optimization of a surface triangulation and isovalue
      discretization
    - the mmg3d application and the libmmg3d library: adaptation
      and optimization of a tetrahedral mesh and implicit domain
      meshing
    - the libmmg library gathering the libmmg2d, libmmgs and
      libmmg3d libraries.
    """

    homepage = "https://www.mmgtools.org/"
    url = "https://github.com/MmgTools/mmg/archive/v5.3.13.tar.gz"

    license("LGPL-3.0-or-later")

    version("5.7.3", sha256="b0a9c5ad6789df369a68f94295df5b324b6348020b73bcc395d32fdd44abe706")
    version("5.7.2", sha256="4c396dd44aec69e0a171a04f857e28aad2e0bbfb733b48b6d81a2c6868e86840")
    version("5.7.1", sha256="27c09477ebc080f54919f76f8533a343936677c81809fe37ce4e2d62fa97237b")
    version("5.6.0", sha256="bbf9163d65bc6e0f81dd3acc5a51e4a8c47a7fdae849abc26277e01154fe2437")
    version("5.5.2", sha256="58e3b866101e6f0686758e16bcf9fb5fb06c85184533fc5054ef1c8adfd4be73")
    version("5.4.0", sha256="2b5cc505018859856766be901797ff5d4789f89377038a0211176a5571039750")
    version("5.3.13", sha256="d9a5925b69b0433f942ab2c8e55659d9ccea758743354b43d54fdf88a6c3c191")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("scotch", default=True, description="Enable SCOTCH library support")
    variant("doc", default=False, description="Build documentation")
    variant("vtk", default=False, when="@5.5.0:", description="Enable VTK I/O support")

    depends_on("scotch", when="+scotch")
    depends_on("doxygen", when="+doc")
    depends_on("vtk", when="+vtk")


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        shared_active = self.spec.satisfies("+shared")
        return [
            self.define_from_variant("USE_SCOTCH", "scotch"),
            self.define_from_variant("USE_VTK", "vtk"),
            self.define("BUILD_SHARED_LIBS", shared_active),
            self.define("LIBMMG3D_SHARED", shared_active),
            self.define("LIBMMG2D_SHARED", shared_active),
            self.define("LIBMMGS_SHARED", shared_active),
            self.define("LIBMMG_SHARED", shared_active),
            self.define("LIBMMG3D_STATIC", not shared_active),
            self.define("LIBMMG2D_STATIC", not shared_active),
            self.define("LIBMMGS_STATIC", not shared_active),
            self.define("LIBMMG_STATIC", not shared_active),
        ]

    # parmmg requires this for its build
    @run_after("install")
    def install_source(self):
        prefix = self.spec.prefix
        cp = which("cp")
        cp("-r", os.path.join(self.stage.source_path, "src"), prefix)
        cp("-r", os.path.join(self.build_directory, "src"), prefix)
