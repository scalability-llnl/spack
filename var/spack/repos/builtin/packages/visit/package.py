# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Visit(CMakePackage):
    """VisIt is an Open Source, interactive, scalable, visualization,
    animation and analysis tool.
    """

    ############################
    # Suggestions for building:
    ############################
    # cyrush note:
    #
    # Out of the box, VisIt's python 2 requirement will cause
    # spack spec constraint errors due Qt + Mesa build
    # dependencies.
    #
    # You can avoid this using:
    #
    # linux:
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0
    #
    # linux w/o opengl: (add mesa as opengl if system lacks system opengl )
    #
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \
    #                      ^mesa+opengl
    #
    # macOS:
    #  spack install visit ^python+shared ^glib@2.56.3 ^py-setuptools@44.1.0 \
    #                      ^qt~framework
    #
    # Rpath issues undermine qwt (not qt) when a build as a framework
    # VisIt's osxfixup resolves this for us in other cases,
    # but we can't use osxfixup with spack b/c it will undermine other libs.
    #
    # Even with these changes, VisIt's Python CLI does not work on macOS,
    # there is a linking issue related to OpenSSL.
    # (dyld: Symbol not found: _GENERAL_NAME_free - which comes from OpenSSL)
    #
    ############################
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    git = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.2.1/visit3.2.1.tar.gz"

    tags = ["radiuss"]

    maintainers("cyrush")

    extendable = True

    executables = ["^visit$"]

    version("develop", branch="develop")
    version("3.3.3", sha256="cc67abb7585e23b51ad576e797df4108641ae6c8c5e80e5359a279c729769187")
    version("3.3.2", sha256="0ae7c38287598e8d7d238cf284ea8be1096dcf13f58a7e9e444a28a32c085b56")
    version("3.3.1", sha256="2e969d3146b559fb833e4cdfaefa72f303d8ad368ef325f68506003f7bc317b9")
    version(
        "3.3.0",
        sha256="1a7485146133ac5f1e330d9029697750046ef8d9e9de23a6c2a3685c1c5f4aac",
        deprecated=True,
    )
    version("3.2.2", sha256="d19ac24c622a3bc0a71bc9cd6e5c9860e43f39e3279672129278b6ebce8d0ead")
    version("3.2.1", sha256="779d59564c63f31fcbfeff24b14ddd6ac941b3bb7d671d31765a770d193f02e8")
    version("3.1.1", sha256="0b60ac52fd00aff3cf212a310e36e32e13ae3ca0ddd1ea3f54f75e4d9b6c6cf0")
    version("3.0.1", sha256="a506d4d83b8973829e68787d8d721199523ce7ec73e7594e93333c214c2c12bd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    root_cmakelists_dir = "src"
    generator("ninja")

    variant("gui", default=True, description="Enable VisIt's GUI")
    variant("adios2", default=True, description="Enable ADIOS2 file format")
    variant("hdf5", default=True, description="Enable HDF5 file format")
    variant("netcdf", default=True, description="Enable NetCDF file format")
    variant("silo", default=True, description="Enable Silo file format")
    variant("python", default=True, description="Enable Python support")
    variant("mpi", default=True, description="Enable parallel engine")
    variant("vtkm", default=False, description="Enable VTK-m support")
    variant("conduit", default=True, description="Enable Conduit support")
    variant("mfem", default=True, description="Enable MFEM support")
    variant("plugins", default=True, description="Enable plugin development (xml2cmake)")

    patch("spack-changes-3.1.patch", when="@3.1.0:3.2.2")
    patch("spack-changes-3.0.1.patch", when="@3.0.1")
    patch("nonframework-qwt.patch", when="^qt~framework platform=darwin")
    patch("parallel-hdf5.patch", when="@3.0.1:3.2.2+hdf5+mpi")
    patch("parallel-hdf5-3.3.patch", when="@3.3.0:+hdf5+mpi")
    patch("cmake-findvtkh-3.3.patch", when="@3.3.0:3.3.2+vtkm")
    patch("cmake-findjpeg.patch", when="@3.1.0:3.2.2")
    patch("cmake-findjpeg-3.3.patch", when="@3.3.0")
    # add missing QT header includes for the QSurfaceFormat class
    # (needed to fix "incomplete type" compiler errors)
    patch("0001-fix-missing-header-includes-for-QSurfaceFormat.patch", when="@3.3.3+gui")

    # Fix pthread and librt link errors
    patch("visit32-missing-link-libs.patch", when="@3.2")

    # Fix const-correctness in VTK interface
    patch("vtk-8.2-constcorrect.patch", when="@3.3.3 ^vtk@8.2.1a")

    conflicts(
        "+gui", when="^[virtuals=gl] osmesa", msg="GUI cannot be activated with OSMesa front-end"
    )

    depends_on("cmake@3.14.7:", type="build")
    depends_on("mpi", when="+mpi")

    # VTK flavors
    depends_on("vtk@8.1:8 +opengl2")
    depends_on("vtk +qt", when="+gui")
    depends_on("vtk +python", when="+python")
    depends_on("vtk +mpi", when="+mpi")
    depends_on("vtk ~mpi", when="~mpi")

    # Necessary VTK patches
    depends_on("vtk", patches=[patch("vtk_compiler_visibility.patch")], when="^vtk@8")
    depends_on(
        "vtk",
        patches=[patch("vtk_rendering_opengl2_x11.patch")],
        when="platform=linux ^[virtuals=gl] glx ^vtk@8",
    )
    depends_on("vtk", patches=[patch("vtk_wrapping_python_x11.patch")], when="+python ^vtk@8")

    depends_on("glu")
    depends_on("gl")

    # VisIt doesn't work with later versions of qt.
    depends_on("qt+gui+opengl@5:5.14", when="+gui")
    depends_on("qwt+opengl", when="+gui")

    # python@3.8 doesn't work with VisIt.
    depends_on("python@3.2:3.7,3.9:", when="@:3.2 +python")
    depends_on("python@3.2:", when="@3.3: +python")
    extends("python", when="+python")

    # VisIt uses the hdf5 1.8 api
    # set the API version later on down in setup_build_environment
    depends_on("hdf5@1.8:", when="+hdf5")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    depends_on("hdf5~mpi", when="+hdf5~mpi")

    # Enable netCDF library based on MPI variant and OLD C++ interface
    depends_on("netcdf-c+mpi", when="+netcdf+mpi")
    depends_on("netcdf-c~mpi", when="+netcdf~mpi")
    depends_on("netcdf-cxx", when="+netcdf")

    # VisIt uses Silo's 'ghost zone' data structures, which are only available
    # in v4.10+ releases: https://wci.llnl.gov/simulation/computer-codes/silo/releases/release-notes-4.10
    # Silo versions < 4.11 do not build successfully with Spack
    depends_on("silo@4.11: +shared", when="+silo")
    depends_on("silo+hdf5", when="+silo+hdf5")
    depends_on("silo~hdf5", when="+silo~hdf5")
    depends_on("silo+mpi", when="+silo+mpi")
    depends_on("silo~mpi", when="+silo~mpi")

    depends_on("conduit@0.8.3:", when="+conduit")
    depends_on("conduit+python", when="+conduit")
    depends_on("conduit+hdf5", when="+conduit+hdf5")
    depends_on("conduit~hdf5", when="+conduit~hdf5")
    depends_on("conduit+mpi", when="+conduit+mpi")
    depends_on("conduit~mpi", when="+conduit~mpi")

    depends_on("mfem@4.4:", when="+mfem")
    depends_on("mfem+shared+exceptions+fms+conduit", when="+mfem")
    depends_on("libfms@0.2:", when="+mfem")

    with when("+adios2"):
        depends_on("adios2")
        # adios 2.8 removed adios2_taustubs (https://github.com/visit-dav/visit/issues/19209)
        depends_on("adios2@:2.7.1")
        depends_on("adios2+hdf5", when="+hdf5")
        depends_on("adios2~hdf5", when="~hdf5")
        depends_on("adios2+mpi", when="+mpi")
        depends_on("adios2~mpi", when="~mpi")
        depends_on("adios2+python", when="+python")
        depends_on("adios2~python", when="~python")

    # For version 3.3.0 through 3.3.2, we used vtk-h to utilize vtk-m.
    # For version starting with 3.3.3 we use vtk-m directly.
    depends_on("vtk-m@1.7.0+testlib~cuda", when="@3.3.0:3.3.2+vtkm")
    depends_on("vtk-h@0.8.1+shared~mpi~openmp~cuda", when="@3.3.0:3.3.2+vtkm")
    depends_on("vtk-m@1.9.0+testlib~cuda", when="@3.3.3:+vtkm")

    # This patch prevents vtk-m from throwing an exception whenever any
    # vtk-m operations are performed.
    depends_on("vtk-m", patches=[patch("vtk-m_transport_tag_topology_field_in.patch")])

    depends_on("zlib-api")

    @when("@3:,develop")
    def patch(self):
        # Some of VTK's targets don't create explicit libraries, so there is no
        # 'vtktiff'. Instead, replace with the library variable defined from
        # VTK's module flies (e.g. lib/cmake/vtk-8.1/Modules/vtktiff.cmake)
        for filename in find("src", "CMakeLists.txt"):
            filter_file(r"\bvtk(tiff|jpeg|png)", r"${vtk\1_LIBRARIES}", filename)

        # NetCDF components are in separate directories using Spack, which is
        # not what Visit's CMake logic expects
        if "+netcdf" in self.spec:
            filter_file(r"(set\(NETCDF_CXX_DIR)", r"#\1", "src/CMake/FindNetcdf.cmake")

    def flag_handler(self, name, flags):
        if name in ("cflags", "cxxflags"):
            # NOTE: This is necessary in order to allow VisIt to compile a couple
            # of lines of code with 'const char*' to/from 'char*' conversions.
            if "@3:%gcc" in self.spec:
                flags.append("-fpermissive")

            # VisIt still uses the hdf5 1.8 api
            if "+hdf5" in self.spec and "@1.10:" in self.spec["hdf5"]:
                flags.append("-DH5_USE_18_API")

        elif name == "ldlibs":
            # Python support is missing a pthread dependency
            if "@3 +python" in self.spec:
                flags.append("-lpthread")

        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("CMAKE_SKIP_COMPATIBILITY_TESTS", True),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
            self.define("VTK_MAJOR_VERSION", spec["vtk"].version[0]),
            self.define("VTK_MINOR_VERSION", spec["vtk"].version[1]),
            self.define("VISIT_VTK_DIR", spec["vtk"].prefix),
            self.define("VISIT_ZLIB_DIR", spec["zlib-api"].prefix),
            self.define("VISIT_JPEG_DIR", spec["jpeg"].prefix),
            self.define("VISIT_USE_GLEW", False),
            self.define("VISIT_CONFIG_SITE", "NONE"),
        ]

        # Provide the plugin compilation environment so as to extend VisIt
        args.append(self.define_from_variant("VISIT_INSTALL_THIRD_PARTY", "plugins"))

        if "@3.1: platform=darwin" in spec:
            args.append(self.define("FIXUP_OSX", False))

        if "+python" in spec:
            args.extend(
                [
                    self.define("VISIT_PYTHON_FILTERS", True),
                    self.define("VISIT_PYTHON_SCRIPTING", True),
                    self.define("PYTHON_DIR", spec["python"].home),
                ]
            )
        else:
            args.extend(
                [
                    self.define("VISIT_PYTHON_FILTERS", False),
                    self.define("VISIT_PYTHON_SCRIPTING", False),
                ]
            )

        if "+gui" in spec:
            qt_bin = spec["qt"].prefix.bin
            qmake_exe = os.path.join(qt_bin, "qmake")
            args.extend(
                [
                    self.define("VISIT_SERVER_COMPONENTS_ONLY", False),
                    self.define("VISIT_ENGINE_ONLY", False),
                    self.define("VISIT_LOC_QMAKE_EXE", qmake_exe),
                    self.define("VISIT_QT_DIR", spec["qt"].prefix),
                    self.define("VISIT_QWT_DIR", spec["qwt"].prefix),
                ]
            )
        else:
            args.extend(
                [
                    self.define("VISIT_SERVER_COMPONENTS_ONLY", True),
                    self.define("VISIT_ENGINE_ONLY", True),
                ]
            )

        # OpenGL args
        args.extend(
            [
                self.define("VISIT_USE_X", "glx" in spec),
                self.define("VISIT_MESAGL_DIR", "IGNORE"),
                self.define("VISIT_OPENGL_DIR", "IGNORE"),
                self.define("VISIT_OSMESA_DIR", "IGNORE"),
                self.define("OpenGL_GL_PREFERENCE", "LEGACY"),
                self.define("OPENGL_INCLUDE_DIR", spec["gl"].headers.directories[0]),
                self.define("OPENGL_gl_LIBRARY", spec["gl"].libs[0]),
                self.define("OPENGL_glu_LIBRARY", spec["glu"].libs[0]),
            ]
        )
        if spec.satisfies("^[virtuals=gl] osmesa"):
            args.extend(
                [
                    self.define("HAVE_OSMESA", True),
                    self.define("OSMESA_LIBRARIES", spec["osmesa"].libs[0]),
                    self.define("OPENGL_gl_LIBRARY", spec["osmesa"].libs[0]),
                ]
            )

        if "+hdf5" in spec:
            args.append(self.define("HDF5_DIR", spec["hdf5"].prefix))
            if "+mpi" in spec and "+mpi" in spec["hdf5"]:
                args.append(self.define("VISIT_HDF5_MPI_DIR", spec["hdf5"].prefix))

        if "+netcdf" in spec:
            args.extend(
                [
                    self.define("NETCDF_DIR", spec["netcdf-c"].prefix),
                    self.define("NETCDF_CXX_DIR", spec["netcdf-cxx"].prefix),
                ]
            )

        if "+silo" in spec:
            args.append(self.define("VISIT_SILO_DIR", spec["silo"].prefix))

        if "+conduit" in spec:
            args.extend(
                [
                    self.define("VISIT_CONDUIT_DIR", spec["conduit"].prefix),
                    self.define("CONDUIT_VERSION", spec["conduit"].version),
                ]
            )

        if "+adios2" in spec:
            args.extend([self.define("VISIT_ADIOS2_DIR", spec["adios2"].prefix)])

        if "+mfem" in spec:
            args.extend(
                [
                    self.define("VISIT_MFEM_DIR", spec["mfem"].prefix),
                    self.define("VISIT_FMS_DIR", spec["libfms"].prefix),
                    self.define("VISIT_MFEM_INCDEP", "CONDUIT_INCLUDE_DIR;FMS_INCLUDE_DIR"),
                ]
            )

        if "+mpi" in spec:
            args.extend(
                [
                    self.define("VISIT_PARALLEL", True),
                    self.define("VISIT_MPI_COMPILER", spec["mpi"].mpicxx),
                ]
            )
        else:
            args.append(self.define("VISIT_PARALLEL", False))

        if "@3.3.0:3.3.2 +vtkm" in spec:
            args.append(self.define("VISIT_VTKM_DIR", spec["vtk-m"].prefix))
            args.append(self.define("VISIT_VTKH_DIR", spec["vtk-h"].prefix))

        if "@3.3.3: +vtkm" in spec:
            lib_dirs = [spec["libx11"].prefix.lib]
            if self.spec.satisfies("^vtkm+rocm"):
                lib_dirs.append(spec["hip"].prefix.lib)
            args.append(self.define("VISIT_VTKM_DIR", spec["vtk-m"].prefix))
            args.append(
                self.define(
                    "CMAKE_EXE_LINKER_FLAGS", "".join("-L%s " % s for s in lib_dirs).strip()
                )
            )
            args.append(
                self.define(
                    "CMAKE_MODULE_LINKER_FLAGS", "".join("-L%s " % s for s in lib_dirs).strip()
                )
            )
            args.append(
                self.define(
                    "CMAKE_SHARED_LINKER_FLAGS", "".join("-L%s " % s for s in lib_dirs).strip()
                )
            )

        return args

    # https://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=executables#making-a-package-discoverable-with-spack-external-find
    # Here we are only able to determine the latest version
    # despite VisIt may have multiple versions
    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-version", output=str, error=str)
        match = re.search(r"\s*(\d[\d\.]+)\.", output)
        return match.group(1) if match else None
