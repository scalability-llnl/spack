# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Serialbox(CMakePackage):
    """Serialbox is a serialization library and tools for C/C++, Python3 and
    Fortran. Serialbox is used in several projects for building validation
    frameworks against reference runs."""

    homepage = "https://github.com/GridTools/serialbox"
    url = "https://github.com/GridTools/serialbox/archive/v2.6.1.tar.gz"

    maintainers("skosukhin")

    license("BSD-2-Clause")

    version("2.6.1", sha256="b795ce576e8c4fd137e48e502b07b136079c595c82c660cfa2e284b0ef873342")
    version("2.6.0", sha256="9199f8637afbd7f2b3c5ba932d1c63e9e14d553a0cafe6c29107df0e04ee9fae")
    version("2.5.4", sha256="f4aee8ef284f58e6847968fe4620e222ac7019d805bbbb26c199e4b6a5094fee")
    version("2.5.3", sha256="696499b3f43978238c3bcc8f9de50bce2630c07971c47c9e03af0324652b2d5d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("c", default=True, description="enable C interface")
    variant("python", default=False, description="enable Python interface")
    variant("fortran", default=False, description="enable Fortran interface")
    variant("ftg", default=False, description="enable FortranTestGenerator frontend")
    variant("sdb", default=False, description="enable stencil debugger")
    variant("shared", default=True, description="build shared libraries")
    variant("examples", default=False, description="build the examples")
    variant("logging", default=True, description="enable the logging infrastructure")
    variant("async-api", default=True, description="enable the asynchronous API")
    variant("netcdf", default=False, description="build the NetCDF archive backend")
    variant(
        "std-filesystem",
        default=True,
        description="use std::experimental::filesystem (no dependency on " "compiled boost libs)",
    )

    depends_on("cmake@3.12:", type="build")
    # We might be provided with an external vanilla cmake, and we need one with
    # with https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5025
    depends_on("cmake@3.19:", when="%pgi", type="build")

    depends_on("boost@1.54:", type="build")
    depends_on("boost+filesystem+system", when="~std-filesystem", type=("build", "link"))

    depends_on("netcdf-c", when="+netcdf")

    # The preprocessor can be run with Python 2:
    depends_on("python", type="run")
    # The Python interface is compatible only with Python 3:
    depends_on("python@3.4:", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))

    # pp_ser fails to process source files containing Unicode character with
    # Python 3 (https://github.com/GridTools/serialbox/pull/249):
    patch("ppser_py3.patch", when="@2.2.0:")

    # NAG patches:
    patch("nag/interface.patch", when="@2.0.1:%nag+fortran")
    patch("nag/examples.patch", when="@2.3.1:%nag+fortran+examples")
    patch("nag/ftg.patch", when="@2.3.1:%nag+ftg")
    patch("nag/bool_getters.patch", when="@2.3.1:%nag@7.1:+fortran")

    # Add missing include directives
    # (part of https://github.com/GridTools/serialbox/pull/259):
    patch("missing_includes.patch", when="@:2.6.1+c")

    conflicts(
        "+ftg",
        when="~fortran",
        msg="the FortranTestGenerator frontend requires the Fortran " "interface",
    )
    conflicts(
        "+ftg",
        when="@:2.2.999",
        msg="the FortranTestGenerator frontend is supported only " "starting version 2.3.0",
    )
    conflicts("+sdb", when="~python", msg="the stencil debugger requires the Python interface")
    conflicts("+fortran", when="~c", msg="the Fortran interface requires the C interface")
    conflicts("+python", when="~c", msg="the Python interface requires the C interface")
    conflicts("+python", when="~shared", msg="the Python interface requires the shared libraries")

    def patch(self):
        # The following is implemented as a method to avoid having two sets of
        # almost identical patch files: one with the CR symbols (for versions
        # 2.5.x) and one without them (for versions 2.6.x).

        # Remove hard-coded -march=native
        # (see https://github.com/GridTools/serialbox/pull/233):
        if self.spec.satisfies("@2.0.1:2.6.0"):
            filter_file(r"^(\s*set\(CMAKE_CXX_FLAGS.*-march=native)", r"#\1", "CMakeLists.txt")

        # Do not fallback to boost::filesystem:
        if "+std-filesystem" in self.spec:
            filter_file(
                r"(message\()" r'STATUS( "std::experimental::filesystem not found).*("\))',
                r"\1FATAL_ERROR\2\3",
                "CMakeLists.txt",
            )

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters

        shared = "+shared" in self.spec

        query2libraries = {
            tuple(): ["libSerialboxCore"],
            ("c", "fortran"): ["libSerialboxFortran", "libSerialboxC", "libSerialboxCore"],
            ("c",): ["libSerialboxC", "libSerialboxCore"],
            ("fortran",): ["libSerialboxFortran", "libSerialboxC", "libSerialboxCore"],
        }

        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]

        if self.spec.satisfies("@2.5.0:2.5"):
            libraries = [
                "{0}{1}".format(name, "Shared" if shared else "Static") for name in libraries
            ]

        libs = find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

        if libs:
            return libs

        msg = "Unable to recursively locate {0} libraries in {1}"
        raise spack.error.NoLibrariesError(msg.format(self.spec.name, self.spec.prefix))

    def flag_handler(self, name, flags):
        cmake_flags = []

        if name == "cxxflags":
            # Intel (at least up to version 19.0.1, version 19.0.4 works) and
            # PGI (at least up to version 19.9, version 20.1.0 works) compilers
            # have problems with C++11 name mangling. An attempt to link to
            # libSerialboxCore leads to:
            # undefined reference to
            #     `std::experimental::filesystem::v1::__cxx11::path::
            #         _M_find_extension[abi:cxx11]() const'
            if any(
                self.spec.satisfies("{0}+std-filesystem".format(x))
                for x in ["%intel@:19.0.1", "%pgi@:19.9"]
            ):
                cmake_flags.append("-D_GLIBCXX_USE_CXX11_ABI=0")

        return flags, None, (cmake_flags or None)

    def setup_run_environment(self, env):
        # Allow for running the preprocessor directly:
        env.prepend_path("PATH", self.prefix.python.pp_ser)
        # Allow for running the preprocessor as a Python module, as well as
        # enable the Python interface in a non-standard directory:
        env.prepend_path("PYTHONPATH", self.prefix.python.pp_ser)

    def setup_dependent_package(self, module, dependent_spec):
        # Simplify the location of the preprocessor by dependent packages:
        self.spec.pp_ser = join_path(self.prefix.python.pp_ser, "pp_ser.py")

    def cmake_args(self):
        args = [
            "-DBOOST_ROOT:PATH=%s" % self.spec["boost"].prefix,
            # https://cmake.org/cmake/help/v3.15/module/FindBoost.html#boost-cmake
            self.define("Boost_NO_BOOST_CMAKE", True),
            self.define_from_variant("SERIALBOX_ENABLE_C", "c"),
            self.define_from_variant("SERIALBOX_ENABLE_PYTHON", "python"),
            self.define_from_variant("SERIALBOX_ENABLE_FORTRAN", "fortran"),
            self.define_from_variant("SERIALBOX_ENABLE_FTG", "ftg"),
            self.define_from_variant("SERIALBOX_ENABLE_SDB", "sdb"),
            self.define_from_variant("SERIALBOX_BUILD_SHARED", "shared"),
            self.define_from_variant("SERIALBOX_EXAMPLES", "examples"),
            self.define_from_variant("SERIALBOX_LOGGING", "logging"),
            self.define_from_variant("SERIALBOX_ASYNC_API", "async-api"),
            # CMake scripts of Serialbox (at least up to version 2.6.0) are
            # broken and do not instruct the compiler to link to the OpenSSL
            # libraries:
            self.define("SERIALBOX_USE_OPENSSL", False),
            self.define_from_variant("SERIALBOX_ENABLE_EXPERIMENTAL_FILESYSTEM", "std-filesystem"),
            self.define_from_variant("SERIALBOX_USE_NETCDF", "netcdf"),
            self.define("SERIALBOX_TESTING", self.run_tests),
        ]

        if "+netcdf" in self.spec:
            args.append("-DNETCDF_ROOT:PATH=%s" % self.spec["netcdf-c"].prefix)

        return args
