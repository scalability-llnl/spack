# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Openvdb(CMakePackage):
    """OpenVDB - a sparse volume data format."""

    homepage = "https://github.com/AcademySoftwareFoundation/openvdb"
    url = "https://github.com/AcademySoftwareFoundation/openvdb/archive/v10.0.0.tar.gz"
    git = "https://github.com/AcademySoftwareFoundation/openvdb.git"

    # Github account name for drew@lagrangian.xyz
    maintainers("eloop")

    license("MPL-2.0")

    version("develop", branch="develop")
    version("10.0.0", sha256="6d4f6b5ccd0f9d35a4886d9a51a98c97fa314f75bf9737c5121e91b706e2db70")
    version("9.1.0", sha256="914ee417b4607c75c95b53bc73a0599de4157c7d6a32e849e80f24e40fb64181")
    version("8.2.0", sha256="d2e77a0720db79e9c44830423bdb013c24a1cf50994dd61d570b6e0c3e0be699")
    version("8.0.1", sha256="a6845da7c604d2c72e4141c898930ac8a2375521e535f696c2cd92bebbe43c4f")
    version("7.1.0", sha256="0c3588c1ca6e647610738654ec2c6aaf41a203fd797f609fbeab1c9f7c3dc116")

    depends_on("cxx", type="build")  # generated

    # these variants were for 8.0.1 and probably could be updated...
    variant("shared", default=True, description="Build as a shared library.")
    variant("python", default=False, description="Build the pyopenvdb python extension.")
    variant("vdb_print", default=False, description="Build the vdb_print tool.")
    variant("vdb_lod", default=False, description="Build the vdb_lod tool.")
    variant("vdb_render", default=False, description="Build the vdb_render tool.")
    variant("ax", default=False, description="Build the AX extension (untested).")

    depends_on("ilmbase", when="@8:9")
    depends_on("ilmbase@2.3:3.1", when="@10:")
    depends_on("openexr", when="@8:9")
    depends_on("openexr@2.3:3.1", when="@10:")
    depends_on("intel-tbb@:2020.1", when="@:8.1")
    depends_on("intel-tbb@2021", when="@8.2:")
    depends_on("zlib-api")
    depends_on("c-blosc@1.17.0")  # depends_on('c-blosc@1.5:')
    depends_on("py-numpy", when="+python")
    depends_on("boost+iostreams+system+python+numpy", when="+python")
    depends_on("boost+iostreams+system", when="~python")
    extends("python", when="+python")

    # AX requires quite a few things, and hasn't been properly released
    # yet. I've only managed to build llvm@8.0.1 under centos8. It
    # looks like the next version of OpenVDB will support llvm@12.0.0.
    depends_on("llvm@8.0.1", when="+ax")
    depends_on("bison", when="+ax")
    depends_on("flex", when="+ax")
    depends_on("git", type="build", when="@develop")

    def cmake_args(self):
        args = [
            self.define("OPENVDB_BUILD_CORE", True),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("OPENVDB_BUILD_VDB_PRINT", "vdb_print"),
            self.define_from_variant("OPENVDB_BUILD_VDB_LOD", "vdb_lod"),
            self.define_from_variant("OPENVDB_BUILD_VDB_RENDER", "vdb_render"),
            self.define_from_variant("OPENVDB_BUILD_AX", "ax"),
            self.define_from_variant("OPENVDB_BUILD_AX_BINARIES", "ax"),
            self.define_from_variant("OPENVDB_BUILD_PYTHON_MODULE", "python"),
            self.define_from_variant("USE_NUMPY", "python"),
        ]
        return args

    # Before v8.2.0 the python extension is being installed in the
    # wrong directory by OpenVDB's cmake, instead it needs to be in
    # python_platlib. And for RHEL systems we find the dso in
    # lib64/ instead of lib/.
    @run_after("install")
    def post_install(self):
        spec = self.spec
        if "+python" in spec and spec.satisfies("@:8.0.1"):
            if sys.platform == "darwin":
                pyso = "pyopenvdb.dylib"
            else:
                pyso = "pyopenvdb.so"
            pyver = "python{0}".format(spec["python"].package.version.up_to(2))

            src = prefix.lib.join(pyver).join(pyso)
            if not os.path.isfile(src):
                src = prefix.lib64.join(pyver).join(pyso)
            assert os.path.isfile(src)
            os.rename(src, os.path.join(python_platlib, pyso))
