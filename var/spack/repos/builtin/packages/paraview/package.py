# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import os
import re
import sys
from subprocess import Popen

from spack.package import *

IS_WINDOWS = sys.platform == "win32"


class Paraview(CMakePackage, CudaPackage, ROCmPackage):
    """ParaView is an open-source, multi-platform data analysis and
    visualization application. This package includes the Catalyst
    in-situ library for versions 5.7 and greater, otherwise use the
    catalyst package.

    """

    homepage = "https://www.paraview.org"
    url = "https://www.paraview.org/files/v5.7/ParaView-v5.7.0.tar.xz"
    list_url = "https://www.paraview.org/files"
    list_depth = 1
    git = "https://gitlab.kitware.com/paraview/paraview.git"

    maintainers("danlipsa", "vicentebolea", "kwryankrattiger")
    tags = ["e4s"]

    license("Apache-2.0")

    version("master", branch="master", submodules=True)
    version(
        "5.13.1",
        sha256="a16503ce37b999c2967d84234596e7bf67ac98221851a288bb1399c7e1dc2004",
        preferred=True,
    )
    version("5.13.0", sha256="886f530bebd6b24c6a7f8a5f4b1afa72c53d4737ccaa4b5fd5946b4e5a758c91")
    version("5.12.1", sha256="927f880c13deb6dde4172f4727d2b66f5576e15237b35778344f5dd1ddec863e")
    version("5.12.0", sha256="d289afe7b48533e2ca4a39a3b48d3874bfe67cf7f37fdd2131271c57e64de20d")
    version("5.11.2", sha256="5c5d2f922f30d91feefc43b4a729015dbb1459f54c938896c123d2ac289c7a1e")
    version("5.11.1", sha256="5cc2209f7fa37cd3155d199ff6c3590620c12ca4da732ef7698dec37fa8dbb34")
    version("5.11.0", sha256="9a0b8fe8b1a2cdfd0ace9a87fa87e0ec21ee0f6f0bcb1fdde050f4f585a25165")
    version("5.10.1", sha256="520e3cdfba4f8592be477314c2f6c37ec73fb1d5b25ac30bdbd1c5214758b9c2")
    version("5.10.0", sha256="86d85fcbec395cdbc8e1301208d7c76d8f48b15dc6b967ffbbaeee31242343a5")
    version("5.9.1", sha256="0d486cb6fbf55e428845c9650486f87466efcb3155e40489182a7ea85dfd4c8d")
    version("5.9.0", sha256="b03258b7cddb77f0ee142e3e77b377e5b1f503bcabc02bfa578298c99a06980d")
    version("5.8.1", sha256="7653950392a0d7c0287c26f1d3a25cdbaa11baa7524b0af0e6a1a0d7d487d034")
    version("5.8.0", sha256="219e4107abf40317ce054408e9c3b22fb935d464238c1c00c0161f1c8697a3f9")
    version("5.7.0", sha256="e41e597e1be462974a03031380d9e5ba9a7efcdb22e4ca2f3fec50361f310874")
    version("5.6.2", sha256="1f3710b77c58a46891808dbe23dc59a1259d9c6b7bb123aaaeaa6ddf2be882ea")
    version("5.6.0", sha256="cb8c4d752ad9805c74b4a08f8ae6e83402c3f11e38b274dba171b99bb6ac2460")
    version("5.5.2", sha256="64561f34c4402b88f3cb20a956842394dde5838efd7ebb301157a837114a0e2d")
    version("5.5.1", sha256="a6e67a95a7a5711a2b5f95f38ccbff4912262b3e1b1af7d6b9afe8185aa85c0d")
    version("5.5.0", sha256="1b619e326ff574de808732ca9a7447e4cd14e94ae6568f55b6581896cd569dff")
    version("5.4.1", sha256="390d0f5dc66bf432e202a39b1f34193af4bf8aad2355338fa5e2778ea07a80e4")
    version("5.4.0", sha256="f488d84a53b1286d2ee1967e386626c8ad05a6fe4e6cbdaa8d5e042f519f94a9")
    version("5.3.0", sha256="046631bbf00775edc927314a3db207509666c9c6aadc7079e5159440fd2f88a0")
    version("5.2.0", sha256="894e42ef8475bb49e4e7e64f4ee2c37c714facd18bfbb1d6de7f69676b062c96")
    version("5.1.2", sha256="ff02b7307a256b7c6e8ad900dee5796297494df7f9a0804fe801eb2f66e6a187")
    version("5.0.1", sha256="caddec83ec284162a2cbc46877b0e5a9d2cca59fb4ab0ea35b0948d2492950bb")
    version("4.4.0", sha256="c2dc334a89df24ce5233b81b74740fc9f10bc181cd604109fd13f6ad2381fc73")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "development_files",
        default=True,
        description="Install include files for Catalyst or plugins support",
    )
    variant("python", default=False, description="Enable Python support", when="@5.6:")
    variant("fortran", default=False, description="Enable Fortran support")
    variant("mpi", default=True, description="Enable MPI support")
    variant("qt", default=False, description="Enable Qt (gui) support")
    variant("opengl2", default=True, description="Enable OpenGL2 backend")
    variant("examples", default=False, description="Build examples")
    variant("hdf5", default=False, description="Use external HDF5")
    variant("shared", default=True, description="Builds a shared version of the library")
    variant("kits", default=True, description="Use module kits")
    variant("pagosa", default=False, description="Build the pagosa adaptor")
    variant("eyedomelighting", default=False, description="Enable Eye Dome Lighting feature")
    variant("nvindex", default=False, description="Enable the pvNVIDIAIndeX plugin")
    variant("tbb", default=False, description="Enable multi-threaded parallelism with TBB")
    variant("adios2", default=False, description="Enable ADIOS2 support", when="@5.8:")
    variant("visitbridge", default=False, description="Enable VisItBridge support")
    variant("raytracing", default=False, description="Enable Raytracing support")
    variant("cdi", default=False, description="Enable CDI support")
    variant(
        "openpmd",
        default=False,
        description="Enable openPMD support (w/ ADIOS2/HDF5)",
        when="@5.9: +python",
    )
    variant("catalyst", default=False, description="Enable Catalyst 1", when="@5.7:")
    variant(
        "libcatalyst",
        default=False,
        description="Enable Catalyst 2 (libcatalyst) implementation",
        when="@5.10:",
    )

    variant(
        "advanced_debug",
        default=False,
        description="Enable all other debug flags beside build_type, such as VTK_DEBUG_LEAK",
    )
    variant(
        "build_edition",
        default="canonical",
        multi=False,
        values=("canonical", "catalyst_rendering", "catalyst", "rendering", "core"),
        description="Build editions include only certain modules. "
        "Editions are listed in decreasing order of size.",
    )
    variant(
        "use_vtkm",
        default="default",
        multi=False,
        values=("default", "on", "off"),
        description="Build VTK-m with ParaView by setting PARAVIEW_USE_VTKM=ON,OFF."
        ' "default" lets the build_edition make the decision.'
        ' "on" or "off" will always override the build_edition.',
    )

    conflicts("~hdf5", when="+visitbridge")
    conflicts("+adios2", when="@:5.10 ~mpi")
    conflicts("+openpmd", when="~adios2 ~hdf5", msg="openPMD needs ADIOS2 and/or HDF5")
    conflicts("~shared", when="+cuda")
    conflicts("+cuda", when="@5.8:5.10")
    conflicts("+cuda", when="use_vtkm=off")
    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="use_vtkm=off")
    conflicts("paraview@:5.10", when="+rocm")
    # Legacy rendering dropped in 5.5
    # See commit: https://gitlab.kitware.com/paraview/paraview/-/commit/798d328c
    conflicts("~opengl2", when="@5.5:")
    # in 5.7 you cannot reduce the size of the code for Catalyst builds.
    conflicts("build_edition=catalyst_rendering", when="@:5.7")
    conflicts("build_edition=catalyst", when="@:5.7")
    conflicts("build_edition=rendering", when="@:5.7")
    conflicts("build_edition=core", when="@:5.7")
    # before 5.3.0, ParaView didn't have VTK-m
    conflicts("use_vtkm=on", when="@:5.3")
    # paraview@5.9.0 is recommended when using the xl compiler
    # See https://gitlab.kitware.com/paraview/paraview/-/merge_requests/4433
    conflicts(
        "paraview@:5.8",
        when="%xl_r",
        msg="Use paraview@5.9.0 with %xl_r. Earlier versions are not able to build with xl.",
    )

    # CUDA ARCH

    # This is (more or less) the mapping hard-coded in VTK-m logic
    # see https://gitlab.kitware.com/vtk/vtk-m/-/blob/v2.1.0/CMake/VTKmDeviceAdapters.cmake?ref_type=tags#L221-247
    supported_cuda_archs = {
        "20": "fermi",
        "21": "fermi",
        "30": "kepler",
        "32": "kepler",
        "35": "kepler",
        "37": "kepler",
        "50": "maxwel",
        "52": "maxwel",
        "53": "maxwel",
        "60": "pascal",
        "61": "pascal",
        "62": "pascal",
        "70": "volta",
        "72": "volta",
        "75": "turing",
        "80": "ampere",
        "86": "ampere",
    }

    # VTK-m and transitively ParaView does not support Tesla Arch
    for _arch in range(10, 14):
        conflicts(f"cuda_arch={_arch}", when="+cuda", msg="ParaView requires cuda_arch >= 20")

    # Starting from cmake@3.18, CUDA architecture managament can be delegated to CMake.
    # Hence, it is possible to rely on it instead of relying on custom logic updates from VTK-m for
    # newer architectures (wrt mapping).
    pattern = re.compile(r"\d+")
    for _arch in CudaPackage.cuda_arch_values:
        _number = re.match(pattern, _arch).group()
        if int(_number) > 86:
            conflicts("cmake@:3.17", when=f"cuda_arch={_arch}")

    # We only support one single Architecture
    for _arch, _other_arch in itertools.permutations(CudaPackage.cuda_arch_values, 2):
        conflicts(
            "cuda_arch={0}".format(_arch),
            when="cuda_arch={0}".format(_other_arch),
            msg="Paraview only accepts one architecture value",
        )

    depends_on("cmake@3.3:", type="build")
    depends_on("cmake@3.21:", type="build", when="+rocm")

    extends("python", when="+python")

    # VTK < 8.2.1 can't handle Python 3.8
    # This affects Paraview <= 5.7 (VTK 8.2.0)
    # https://gitlab.kitware.com/vtk/vtk/-/issues/17670
    depends_on("python@3:3.7", when="@:5.7 +python", type=("build", "run"))
    depends_on("python@3:", when="@5.8:+python", type=("build", "run"))

    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python+mpi", type=("build", "run"))

    depends_on("py-matplotlib", when="+python", type="run")
    depends_on("py-pandas@0.21:", when="+python", type="run")

    # openPMD is implemented as a Python module and provides ADIOS2 and HDF5 backends
    depends_on("openpmd-api@0.14.5: +python", when="+python +openpmd", type=("build", "run"))
    depends_on("openpmd-api +adios2", when="+openpmd +adios2", type=("build", "run"))
    depends_on("openpmd-api +hdf5", when="+openpmd +hdf5", type=("build", "run"))

    depends_on("tbb", when="+tbb")

    depends_on("mpi", when="+mpi")

    depends_on("qt@:4", when="@:5.2.0+qt")
    depends_on("qt+sql", when="+qt")
    with when("+qt"):
        depends_on("qt+opengl", when="@5.3.0:+opengl2")
        depends_on("qt~opengl", when="@5.3.0:~opengl2")

    depends_on("gl@3.2:", when="+opengl2")
    depends_on("gl@1.2:", when="~opengl2")
    depends_on("glew")
    depends_on("libxt", when="platform=linux ^[virtuals=gl] glx")

    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            requires(
                "^[virtuals=gl] glx", when="+qt", msg="Qt support requires GLX on non Windows"
            )

    depends_on("ospray@2.1:2", when="+raytracing")
    depends_on("openimagedenoise", when="+raytracing")
    depends_on("ospray +mpi", when="+raytracing +mpi")

    depends_on("cdi", when="+cdi")

    depends_on("bzip2")
    depends_on("double-conversion")
    depends_on("expat")
    depends_on("eigen@3:")
    depends_on("freetype")
    depends_on("freetype@:2.10.2", when="@:5.8")
    # depends_on('hdf5+mpi', when='+mpi')
    # depends_on('hdf5~mpi', when='~mpi')
    depends_on("hdf5+hl+mpi", when="+hdf5+mpi")
    depends_on("hdf5+hl~mpi", when="+hdf5~mpi")
    depends_on("hdf5@1.10:", when="+hdf5 @5.10:")
    depends_on("adios2+mpi", when="+adios2+mpi")
    depends_on("adios2~mpi", when="+adios2~mpi")
    depends_on("silo", when="+visitbridge")
    depends_on("silo+mpi", when="+visitbridge+mpi")
    depends_on("silo~mpi", when="+visitbridge~mpi")
    depends_on("boost", when="+visitbridge")
    depends_on("jpeg")
    depends_on("jsoncpp")
    depends_on("libogg")
    depends_on("libpng")
    depends_on("libtheora")
    depends_on("libtiff")
    depends_on("netcdf-c")
    depends_on("pegtl@2.8.3")
    depends_on("protobuf@3.4:")
    # Paraview 5.10 can't build with protobuf > 3.18
    # https://github.com/spack/spack/issues/37437
    depends_on("protobuf@3.4:3.18", when="@:5.10%oneapi")
    depends_on("protobuf@3.4:3.18", when="@:5.10%intel@2021:")
    depends_on("protobuf@3.4:3.18", when="@:5.10%xl")
    depends_on("protobuf@3.4:3.18", when="@:5.10%xl_r")
    # protobuf requires newer abseil-cpp, which in turn requires C++14,
    # but paraview uses C++11 by default. Use for 5.8+ until ParaView updates
    # its C++ standard level.
    depends_on("protobuf@3.4:3.21", when="@5.8:%gcc")
    depends_on("protobuf@3.4:3.21", when="@5.8:%clang")
    depends_on("protobuf@3.4:3.21", when="@5.11:")
    depends_on("protobuf@3.4:3.21", when="@master")
    depends_on("libxml2")
    depends_on("lz4")
    depends_on("xz")
    depends_on("zlib-api")
    depends_on("libcatalyst@2:", when="+libcatalyst")
    depends_on("hip@5.2:", when="+rocm")
    for target in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos@:3.7.01 +rocm amdgpu_target={0}".format(target),
            when="+rocm amdgpu_target={0}".format(target),
        )

    # Older builds of pugi export their symbols differently,
    # and pre-5.9 is unable to handle that.
    depends_on("pugixml@:1.10", when="@:5.8")
    depends_on("pugixml", when="@5.9:")

    # ParaView depends on cli11 due to changes in MR
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/4951
    depends_on("cli11@1.9.1", when="@5.10:")

    # ParaView depends on nlohmann-json due to changes in MR
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/8550
    depends_on("nlohmann-json", when="@5.11:")

    # ParaView depends on proj@8.1.0 due to changes in MR
    # v8.1.0 is required for VTK::GeoVis
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/8474
    depends_on("proj@8.1.0", when="@5.11:")

    patch("stl-reader-pv440.patch", when="@4.4.0")

    # Broken gcc-detection - improved in 5.1.0, redundant later
    patch("gcc-compiler-pv501.patch", when="@:5.0.1")

    # Broken installation (ui_pqExportStateWizard.h) - fixed in 5.2.0
    patch("ui_pqExportStateWizard.patch", when="@:5.1.2")

    # Broken vtk-m config. Upstream catalyst changes
    patch("vtkm-catalyst-pv551.patch", when="@5.5.0:5.5.2")

    # Broken H5Part with external parallel HDF5
    patch("h5part-parallel.patch", when="@5.7.0:5.7")

    # Broken downstream FindMPI
    patch("vtkm-findmpi-downstream.patch", when="@5.9.0")

    # Include limits header wherever needed to fix compilation with GCC 11
    patch("paraview-gcc11-limits.patch", when="@5.8:5.9 %gcc@11.1.0:")

    # Fix IOADIOS2 module to work with kits
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/8653
    patch("vtk-adios2-module-no-kit.patch", when="@5.8:5.11")

    # Patch for paraview 5.9.0%xl_r
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/7591
    patch("xlc-compilation-pv590.patch", when="@5.9.0%xl_r")

    # intel oneapi doesn't compile some code in catalyst
    patch("catalyst-etc_oneapi_fix.patch", when="@5.10.0:5.10.1%oneapi")

    # Patch for paraview 5.8: ^hdf5@1.13.2:
    # Even with ~hdf5, hdf5 is part of the dependency tree due to netcdf-c
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/9690
    patch("vtk-xdmf2-hdf51.13.1.patch", when="@5.8:5.10")
    patch("vtk-xdmf2-hdf51.13.2.patch", when="@5.8:5.11.0")
    # a patch with the same name is also applied to vtk
    # the two patches are the same but for the path to the files they patch
    patch("vtk_alias_hdf5.patch", when="@5.9.0: platform=windows")

    # Fix VTK to work with external freetype using CONFIG mode for find_package
    patch("FindFreetype.cmake.patch", when="@5.10.1:")

    # Fix VTK to remove deprecated ADIOS2 functions
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/10113
    patch("adios2-remove-deprecated-functions.patch", when="@5.10:5.11 ^adios2@2.9:")

    patch("exodusII-netcdf4.9.0.patch", when="@5.10.0:5.10.2")

    patch("kits_with_catalyst_5_12.patch", when="@5.12.0")

    generator("ninja", "make", default="ninja")
    # https://gitlab.kitware.com/paraview/paraview/-/issues/21223
    conflicts("generator=ninja", when="%xl")
    conflicts("generator=ninja", when="%xl_r")

    def url_for_version(self, version):
        _urlfmt = "http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.{3}"
        """Handle ParaView version-based custom URLs."""
        if version < Version("5.1.0"):
            return _urlfmt.format(version.up_to(2), version, "-source", "gz")
        elif version < Version("5.6.1"):
            return _urlfmt.format(version.up_to(2), version, "", "gz")
        else:
            return _urlfmt.format(version.up_to(2), version, "", "xz")

    @property
    def paraview_subdir(self):
        """The paraview subdirectory name as paraview-major.minor"""
        if self.spec.version == Version("master"):
            return "paraview-5.11"
        else:
            return "paraview-{0}".format(self.spec.version.up_to(2))

    def setup_dependent_build_environment(self, env, dependent_spec):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib
        env.set("ParaView_DIR", self.prefix)

        if self.spec.version <= Version("5.7.0"):
            env.set("PARAVIEW_VTK_DIR", join_path(lib_dir, "cmake", self.paraview_subdir))
        else:
            env.set("PARAVIEW_VTK_DIR", join_path(lib_dir, "cmake", self.paraview_subdir, "vtk"))

    def flag_handler(self, name, flags):
        if name == "ldflags" and self.spec.satisfies("%intel"):
            flags.append("-shared-intel")
            return (None, flags, None)
        # -no-ipo prevents internal compiler error from multi-file
        # optimization (https://github.com/spack/spack/issues/18192)
        if (name == "cflags" or name == "cxxflags") and self.spec.satisfies("%intel"):
            flags.append("-no-ipo")
            return (None, None, flags)

        if name in ("cflags", "cxxflags"):
            # Constrain the HDF5 API
            if self.spec.satisfies("@:5.9 +hdf5"):
                if self.spec["hdf5"].satisfies("@1.10:"):
                    flags.append("-DH5_USE_18_API")
            elif self.spec.satisfies("@5.10: +hdf5"):
                if self.spec["hdf5"].satisfies("@1.12:"):
                    flags.append("-DH5_USE_110_API")

        return flags, None, None

    def setup_run_environment(self, env):
        # paraview 5.5 and later
        # - cmake under lib/cmake/paraview-5.5
        # - libs  under lib
        # - python bits under lib/python2.8/site-packages
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        env.set("ParaView_DIR", self.prefix)

        if self.spec.version <= Version("5.7.0"):
            env.set("PARAVIEW_VTK_DIR", join_path(lib_dir, "cmake", self.paraview_subdir))
        else:
            env.set("PARAVIEW_VTK_DIR", join_path(lib_dir, "cmake", self.paraview_subdir, "vtk"))

        if self.spec.version <= Version("5.4.1"):
            lib_dir = join_path(lib_dir, self.paraview_subdir)

        env.prepend_path("LIBRARY_PATH", lib_dir)
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)

        if "+python" in self.spec:
            if self.spec.version <= Version("5.4.1"):
                pv_pydir = join_path(lib_dir, "site-packages")
                env.prepend_path("PYTHONPATH", pv_pydir)
                env.prepend_path("PYTHONPATH", join_path(pv_pydir, "vtk"))
            else:
                python_version = self.spec["python"].version.up_to(2)
                pv_pydir = join_path(lib_dir, "python{0}".format(python_version), "site-packages")
                if "+shared" in self.spec or self.spec.version <= Version("5.7.0"):
                    env.prepend_path("PYTHONPATH", pv_pydir)
                    # The Trilinos Catalyst adapter requires
                    # the vtkmodules directory in PYTHONPATH
                    env.prepend_path("PYTHONPATH", join_path(pv_pydir, "vtkmodules"))
                else:
                    env.prepend_path("PYTHONPATH", join_path(pv_pydir, "_paraview.zip"))
                    env.prepend_path("PYTHONPATH", join_path(pv_pydir, "_vtk.zip"))

    def cmake_args(self):
        """Populate cmake arguments for ParaView."""
        spec = self.spec

        def variant_bool(feature, on="ON", off="OFF"):
            """Ternary for spec variant to ON/OFF string"""
            if spec.satisfies(feature):
                return on
            return off

        def use_x11():
            """Return false if osmesa or egl are requested"""
            if (
                spec.satisfies("^[virtuals=gl] osmesa")
                or spec.satisfies("^[virtuals=gl] egl")
                or spec.satisfies("platform=windows")
            ):
                return "OFF"
            return "ON"

        rendering = variant_bool("+opengl2", "OpenGL2", "OpenGL")
        includes = variant_bool("+development_files")

        cmake_args = [
            "-DVTK_OPENGL_HAS_OSMESA:BOOL=%s" % variant_bool("^[virtuals=gl] osmesa"),
            "-DVTK_USE_X:BOOL=%s" % use_x11(),
            "-DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=%s" % includes,
            "-DBUILD_TESTING:BOOL=OFF",
            "-DOpenGL_GL_PREFERENCE:STRING=LEGACY",
            self.define_from_variant("PARAVIEW_ENABLE_VISITBRIDGE", "visitbridge"),
            self.define_from_variant("VISIT_BUILD_READER_Silo", "visitbridge"),
        ]

        if spec.satisfies("^[virtuals=gl] egl"):
            cmake_args.append("-DVTK_OPENGL_HAS_EGL:BOOL=ON")

        if spec.satisfies("@5.12:"):
            cmake_args.append("-DVTK_MODULE_USE_EXTERNAL_VTK_fast_float:BOOL=OFF")
            cmake_args.append("-DVTK_MODULE_USE_EXTERNAL_VTK_token:BOOL=OFF")

        if spec.satisfies("@5.11:"):
            cmake_args.append("-DVTK_MODULE_USE_EXTERNAL_VTK_verdict:BOOL=OFF")

        if spec.satisfies("@5.10:"):
            cmake_args.extend(
                [
                    "-DVTK_MODULE_USE_EXTERNAL_ParaView_vtkcatalyst:BOOL=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_ioss:BOOL=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_exprtk:BOOL=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_fmt:BOOL=OFF",
                ]
            )

        if spec.satisfies("@:5.7") and spec["cmake"].satisfies("@3.17:"):
            cmake_args.append("-DFPHSA_NAME_MISMATCHED:BOOL=ON")

        if spec.satisfies("@5.7:"):
            if spec.satisfies("@5.8:"):
                cmake_args.extend(
                    [
                        "-DPARAVIEW_BUILD_EDITION:STRING=%s"
                        % spec.variants["build_edition"].value.upper(),
                        "-DPARAVIEW_USE_QT:BOOL=%s" % variant_bool("+qt"),
                        "-DPARAVIEW_BUILD_WITH_EXTERNAL=ON",
                    ]
                )
                if spec.satisfies("%cce"):
                    cmake_args.append("-DVTK_PYTHON_OPTIONAL_LINK:BOOL=OFF")
            else:  # @5.7:
                cmake_args.extend(
                    [
                        "-DPARAVIEW_ENABLE_CATALYST:BOOL=ON",
                        "-DPARAVIEW_BUILD_QT_GUI:BOOL=%s" % variant_bool("+qt"),
                        "-DPARAVIEW_USE_EXTERNAL:BOOL=ON",
                    ]
                )

            cmake_args.extend(
                [
                    "-DPARAVIEW_ENABLE_EXAMPLES:BOOL=%s" % variant_bool("+examples"),
                    "-DVTK_MODULE_USE_EXTERNAL_ParaView_cgns=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_gl2ps=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_libharu=OFF",
                    "-DVTK_MODULE_USE_EXTERNAL_VTK_utf8=OFF",
                ]
            )
        else:
            cmake_args.extend(
                [
                    "-DPARAVIEW_BUILD_EXAMPLES:BOOL=%s" % variant_bool("+examples"),
                    "-DVTK_RENDERING_BACKEND:STRING=%s" % rendering,
                    "-DPARAVIEW_BUILD_QT_GUI:BOOL=%s" % variant_bool("+qt"),
                    "-DVTK_USE_SYSTEM_LIBRARIES:BOOL=ON",
                    "-DVTK_USE_SYSTEM_CGNS:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_DIY2:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_GL2PS:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_ICET:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_LIBHARU:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_NETCDFCPP:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_UTF8:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_XDMF2:BOOL=OFF",
                    "-DVTK_USE_SYSTEM_XDMF3:BOOL=OFF",
                ]
            )

        if "+adios2" in spec:
            cmake_args.extend(["-DPARAVIEW_ENABLE_ADIOS2:BOOL=ON"])

        # The assumed qt version changed to QT5 (as of paraview 5.2.1),
        # so explicitly specify which QT major version is actually being used
        if spec.satisfies("+qt"):
            cmake_args.extend(["-DPARAVIEW_QT_VERSION=%s" % spec["qt"].version[0]])
            if IS_WINDOWS:
                # Windows does not currently support Qt Quick
                cmake_args.append("-DVTK_MODULE_ENABLE_VTK_GUISupportQtQuick:STRING=NO")

        if "+fortran" in spec:
            cmake_args.append("-DPARAVIEW_USE_FORTRAN:BOOL=ON")

        # CMake flags for python have changed with newer ParaView versions
        # Make sure Spack uses the right cmake flags
        if "+python" in spec:
            py_use_opt = "USE" if spec.satisfies("@5.8:") else "ENABLE"
            py_ver_opt = "PARAVIEW" if spec.satisfies("@5.7:") else "VTK"
            py_ver_val = 3
            cmake_args.extend(
                [
                    "-DPARAVIEW_%s_PYTHON:BOOL=ON" % py_use_opt,
                    "-D%s_PYTHON_VERSION:STRING=%d" % (py_ver_opt, py_ver_val),
                ]
            )
            if spec.satisfies("@:5.6"):
                cmake_args.append("-DVTK_USE_SYSTEM_MPI4PY:BOOL=%s" % variant_bool("+mpi"))

        else:
            cmake_args.append("-DPARAVIEW_ENABLE_PYTHON:BOOL=OFF")

        if "+mpi" in spec:
            mpi_args = [
                "-DPARAVIEW_USE_MPI:BOOL=ON",
                "-DMPIEXEC:FILEPATH=%s/bin/mpiexec" % spec["mpi"].prefix,
            ]
            if not sys.platform == "win32":
                mpi_args.extend(
                    [
                        "-DMPI_CXX_COMPILER:PATH=%s" % spec["mpi"].mpicxx,
                        "-DMPI_C_COMPILER:PATH=%s" % spec["mpi"].mpicc,
                        "-DMPI_Fortran_COMPILER:PATH=%s" % spec["mpi"].mpifc,
                    ]
                )
            cmake_args.extend(mpi_args)

        cmake_args.append("-DPARAVIEW_BUILD_SHARED_LIBS:BOOL=%s" % variant_bool("+shared"))

        # VTK-m added to ParaView in 5.3.0 and up
        if spec.satisfies("@5.3.0:") and spec.variants["use_vtkm"].value != "default":
            cmake_args.append(
                "-DPARAVIEW_USE_VTKM:BOOL=%s" % spec.variants["use_vtkm"].value.upper()
            )

        if spec.satisfies("@5.8:"):
            cmake_args.append("-DPARAVIEW_USE_CUDA:BOOL=%s" % variant_bool("+cuda"))
        elif spec.satisfies("@5.7:"):
            cmake_args.append("-DVTK_USE_CUDA:BOOL=%s" % variant_bool("+cuda"))
        else:
            cmake_args.append("-DVTKm_ENABLE_CUDA:BOOL=%s" % variant_bool("+cuda"))

        # VTK-m expects cuda_arch to be the arch name vs. the arch version.
        if spec.satisfies("+cuda"):
            if spec["cmake"].satisfies("@3.18:"):
                cmake_args.append(
                    self.define(
                        "CMAKE_CUDA_ARCHITECTURES", ";".join(spec.variants["cuda_arch"].value)
                    )
                )
            else:
                # ParaView/VTK-m only accepts one arch, default to first element
                requested_arch = spec.variants["cuda_arch"].value[0]

                if requested_arch == "none":
                    cuda_arch_value = "native"
                else:
                    try:
                        cuda_arch_value = supported_cuda_archs[requested_arch]
                    except KeyError:
                        raise InstallError("Incompatible cuda_arch=" + requested_arch)

                cmake_args.append(self.define("VTKm_CUDA_Architecture", cuda_arch_value))

        if "darwin" in spec.architecture:
            cmake_args.extend(
                ["-DVTK_USE_X:BOOL=OFF", "-DPARAVIEW_DO_UNIX_STYLE_INSTALLS:BOOL=ON"]
            )

        if "+kits" in spec:
            if spec.satisfies("@5.0:5.6"):
                cmake_args.append("-DVTK_ENABLE_KITS:BOOL=ON")
            elif spec.satisfies("@5.7"):
                # cmake_args.append('-DPARAVIEW_ENABLE_KITS:BOOL=ON')
                # Kits are broken with 5.7
                cmake_args.append("-DPARAVIEW_ENABLE_KITS:BOOL=OFF")
            else:
                cmake_args.append("-DPARAVIEW_BUILD_WITH_KITS:BOOL=ON")

        if "+pagosa" in spec:
            cmake_args.append("-DPARAVIEW_BUILD_PAGOSA_ADAPTOR:BOOL=ON")

        if "+eyedomelighting" in spec:
            cmake_args.append("-DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON")

        if "+tbb" in spec:
            cmake_args.append("-DVTK_SMP_IMPLEMENTATION_TYPE=TBB")

        if "+nvindex" in spec:
            cmake_args.append("-DPARAVIEW_PLUGIN_ENABLE_pvNVIDIAIndeX:BOOL=ON")

        # Hide git from Paraview so it will not use `git describe`
        # to find its own version number
        if spec.satisfies("@5.4.0:5.4.1"):
            cmake_args.extend(["-DGIT_EXECUTABLE=FALSE"])

        # A bug that has been found in vtk causes an error for
        # intel builds for version 5.6.  This should be revisited
        # with later versions of Paraview to see if the issues still
        # arises.
        if "%intel" in spec and spec.version >= Version("5.6"):
            cmake_args.append("-DPARAVIEW_ENABLE_MOTIONFX:BOOL=OFF")

        # Encourage Paraview to use the correct Python libs
        if spec.satisfies("+python"):
            pylibdirs = spec["python"].libs.directories
            cmake_args.append("-DCMAKE_INSTALL_RPATH={0}".format(":".join(self.rpath + pylibdirs)))

        if "+advanced_debug" in spec:
            cmake_args.append("-DVTK_DEBUG_LEAKS:BOOL=ON")

        if spec.satisfies("@5.11:"):
            cmake_args.append("-DPARAVIEW_USE_HIP:BOOL=%s" % variant_bool("+rocm"))
            if "+rocm" in spec:
                archs = spec.variants["amdgpu_target"].value
                if archs != "none":
                    arch_str = ",".join(archs)
                    cmake_args.append("-DCMAKE_HIP_ARCHITECTURES=%s" % arch_str)
                cmake_args.append("-DKokkos_CXX_COMPILER=%s" % spec["hip"].hipcc)

        if "+catalyst" in spec:
            cmake_args.append("-DVTK_MODULE_ENABLE_ParaView_Catalyst=YES")
            if "+python" in spec:
                cmake_args.append("-DVTK_MODULE_ENABLE_ParaView_PythonCatalyst=YES")

        if "+libcatalyst" in spec:
            cmake_args.append("-DVTK_MODULE_ENABLE_ParaView_InSitu=YES")
            cmake_args.append("-DPARAVIEW_ENABLE_CATALYST=YES")

        cmake_args.append(self.define_from_variant("PARAVIEW_ENABLE_RAYTRACING", "raytracing"))
        # Currently only support OSPRay ray tracing
        cmake_args.append(self.define_from_variant("VTK_ENABLE_OSPRAY", "raytracing"))
        cmake_args.append(self.define_from_variant("VTKOSPRAY_ENABLE_DENOISER", "raytracing"))

        # CDI
        cmake_args.append(self.define_from_variant("PARAVIEW_PLUGIN_ENABLE_CDIReader", "cdi"))
        cmake_args.append(self.define_from_variant("PARAVIEW_PLUGIN_AUTOLOAD_CDIReader", "cdi"))

        return cmake_args

    def test_smoke_test(self):
        """Simple smoke test for ParaView"""
        spec = self.spec

        pvserver = Executable(spec["paraview"].prefix.bin.pvserver)
        pvserver("--help")

    def test_pvpython(self):
        """Test pvpython"""
        spec = self.spec

        if "~python" in spec:
            raise SkipTest("Package must be installed with +python")

        pvpython = Executable(spec["paraview"].prefix.bin.pvpython)
        pvpython("-c", "import paraview")

    def test_mpi_ensemble(self):
        """Test MPI ParaView Client/Server ensemble"""
        spec = self.spec

        if "~mpi" in spec or "~python" in spec:
            raise SkipTest("Package must be installed with +mpi and +python")

        mpirun = spec["mpi"].prefix.bin.mpirun
        pvserver = spec["paraview"].prefix.bin.pvserver
        pvpython = Executable(spec["paraview"].prefix.bin.pvpython)

        with working_dir("smoke_test_build", create=True):
            with Popen(
                [mpirun, "-np", "3", pvserver, "--mpi", "--force-offscreen-rendering"]
            ) as servers:
                pvpython(
                    "--force-offscreen-rendering",
                    "-c",
                    "from paraview.simple import *;"
                    "Connect('127.0.0.1');"
                    "sphere = Sphere(ThetaResolution=16, PhiResolution=32);"
                    "sphere_remote = servermanager.Fetch(sphere);"
                    "Show(sphere);"
                    "Render()",
                )
                servers.terminate()

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        self.test_smoke_test()
        self.test_pvpython()
        self.test_mpi_ensemble()
