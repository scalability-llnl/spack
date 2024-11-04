# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *

_definitions = {
    # German Meteorological Service (Deutscher Wetterdienst, DWD):
    "edzw": {
        "conflicts": {"when": "@:2.19.1,2.22.0,2.24.0:"},
        "resources": [
            {
                "when": "@2.20.0",
                "url": "http://opendata.dwd.de/weather/lib/grib/eccodes_definitions.edzw-2.20.0-1.tar.gz",
                "sha256": "a92932f8a13c33cba65d3a33aa06c7fb4a37ed12a78e9abe2c5e966402b99af4",
            },
            {
                "when": "@2.21.0",
                "url": "http://opendata.dwd.de/weather/lib/grib/eccodes_definitions.edzw-2.21.0-3.tar.bz2",
                "sha256": "046f1f6450abb3b44c31dee6229f4aab06ca0d3576e27e93e05ccb7cd6e2d9d9",
            },
            {
                "when": "@2.22.1",
                "url": "http://opendata.dwd.de/weather/lib/grib/eccodes_definitions.edzw-2.22.1-1.tar.bz2",
                "sha256": "be73102a0dcabb236bacd2a70c7b5475f673fda91b49e34df61bef0fa5ad3389",
            },
            {
                "when": "@2.23.0",
                "url": "http://opendata.dwd.de/weather/lib/grib/eccodes_definitions.edzw-2.23.0-4.tar.bz2",
                "sha256": "c5db32861c7d23410aed466ffef3ca661410d252870a3949442d3ecb176aa338",
            },
        ],
    }
}


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    homepage = "https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home"
    url = "https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2"
    git = "https://github.com/ecmwf/eccodes.git"
    list_url = "https://confluence.ecmwf.int/display/ECC/Releases"

    maintainers("skosukhin", "victoria-cherkas", "dominichofer", "climbfuji")

    license("Apache-2.0")

    version("develop", branch="develop")
    version("2.34.0", sha256="3cd208c8ddad132789662cf8f67a9405514bfefcacac403c0d8c84507f303aba")
    version("2.33.0", sha256="bdcec8ce63654ec6803400c507f01220a9aa403a45fa6b5bdff7fdcc44fd7daf")
    version("2.32.1", sha256="ad2ac1bf36577b1d35c4a771b4d174a06f522a1e5ef6c1f5e53a795fb624863e")
    version("2.32.0", sha256="b57e8eeb0eba0c05d66fda5527c4ffa84b5ab35c46bcbc9a2227142973ccb8e6")
    version("2.31.0", sha256="808ecd2c11fbf2c3f9fc7a36f8c2965b343f3151011b58a1d6e7cc2e6b3cac5d")
    version("2.25.0", sha256="8975131aac54d406e5457706fd4e6ba46a8cc9c7dd817a41f2aa64ce1193c04e")
    version("2.24.2", sha256="c60ad0fd89e11918ace0d84c01489f21222b11d6cad3ff7495856a0add610403")
    version("2.23.0", sha256="cbdc8532537e9682f1a93ddb03440416b66906a4cc25dec3cbd73940d194bf0c")
    version("2.22.1", sha256="75c7ee96469bb30b0c8f7edbdc4429ece4415897969f75c36173545242bc9e85")
    version("2.21.0", sha256="da0a0bf184bb436052e3eae582defafecdb7c08cdaab7216780476e49b509755")
    version("2.20.0", sha256="207a3d7966e75d85920569b55a19824673e8cd0b50db4c4dac2d3d52eacd7985")
    version("2.19.1", sha256="9964bed5058e873d514bd4920951122a95963128b12f55aa199d9afbafdd5d4b")
    version("2.18.0", sha256="d88943df0f246843a1a062796edbf709ef911de7269648eef864be259e9704e3")
    version("2.13.0", sha256="c5ce1183b5257929fc1f1c8496239e52650707cfab24f4e0e1f1a471135b8272")
    version("2.5.0", sha256="18ab44bc444168fd324d07f7dea94f89e056f5c5cd973e818c8783f952702e4e")
    version("2.2.0", sha256="1a4112196497b8421480e2a0a1164071221e467853486577c4f07627a702f4c3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("tools", default=False, description="Build the command line tools")
    variant("netcdf", default=False, description="Enable GRIB to NetCDF conversion tool")
    variant(
        "jp2k",
        default="openjpeg",
        values=("openjpeg", "jasper", "none"),
        description="Specify JPEG2000 decoding/encoding backend",
    )
    variant("png", default=False, description="Enable PNG support for decoding/encoding")
    variant(
        "aec", default=True, description="Enable Adaptive Entropy Coding for decoding/encoding"
    )
    variant("pthreads", default=False, description="Enable POSIX threads")
    variant("openmp", default=False, description="Enable OpenMP threads")
    variant(
        "memfs", default=False, description="Enable memory based access to definitions/samples"
    )
    variant("fortran", default=False, description="Enable the Fortran support")
    variant("shared", default=True, description="Build shared versions of the libraries")

    variant(
        "extra_definitions",
        values=any_combination_of(*_definitions.keys()),
        description="List of extra definitions to install",
    )

    depends_on("netcdf-c", when="+netcdf")
    # Cannot be built with openjpeg@2.0.x.
    depends_on("openjpeg@1.5.0:1.5,2.1.0:2.3", when="jp2k=openjpeg")
    # Additional constraint for older versions.
    depends_on("openjpeg@:2.1", when="@:2.16 jp2k=openjpeg")

    with when("jp2k=jasper"):
        depends_on("jasper")
        # jasper 3.x compat from commit 86f0b35f1a8492cb16f82fb976a0a5acd2986ac2
        depends_on("jasper@:2", when="@:2.25.0")

    depends_on("libpng", when="+png")
    depends_on("libaec", when="+aec")
    # Can be built with Python 2 or Python 3.
    depends_on("python", when="+memfs", type="build")

    depends_on("cmake@3.6:", type="build")
    depends_on("cmake@3.12:", when="@2.19:", type="build")

    depends_on("ecbuild", type="build", when="@develop")

    conflicts("+openmp", when="+pthreads", msg="Cannot enable both POSIX threads and OMP")

    conflicts(
        "+netcdf",
        when="~tools",
        msg="Cannot enable the NetCDF conversion tool " "when the command line tools are disabled",
    )

    conflicts(
        "~tools",
        when="@:2.18.0",
        msg="The command line tools can be disabled " "only starting version 2.19.0",
    )

    for center, definitions in _definitions.items():
        kwargs = definitions.get("conflicts", None)
        if kwargs:
            conflicts("extra_definitions={0}".format(center), **kwargs)
        for kwargs in definitions.get("resources", []):
            resource(
                name=center,
                destination="spack-definitions",
                placement="definitions.{0}".format(center),
                **kwargs,
            )

    # Enforce linking against the specified JPEG2000 backend, see also
    # https://github.com/ecmwf/eccodes/commit/2c10828495900ff3d80d1e570fe96c1df16d97fb
    patch("openjpeg_jasper.patch", when="@:2.16")

    # CMAKE_INSTALL_RPATH must be a semicolon-separated list.
    patch("cmake_install_rpath.patch", when="@:2.10")

    # Fix a bug preventing cmake from finding NetCDF:
    patch(
        "https://github.com/ecmwf/ecbuild/commit/3916c7d22575c45166fcc89edcbe02a6e9b81aa2.patch?full_index=1",
        sha256="9dcc4affaaa850d4b7247baa939d0f9ffedea132369f1afc3f248dbf720386c9",
        when="@:2.4.0+netcdf",
    )

    @when("%nag+fortran")
    def patch(self):
        # A number of Fortran source files assume that the kinds of integer and
        # real variables are specified in bytes. However, the NAG compiler
        # accepts such code only with an additional compiler flag -kind=byte.
        # We do not simply add the flag because all user applications would
        # have to be compiled with this flag too, which goes against one of the
        # purposes of using the NAG compiler: make sure the code does not
        # contradict the Fortran standards. The following logic could have been
        # implemented as regular patch files, which would, however, be quite
        # large. We would also have to introduce several versions of each patch
        # file to support different versions of the package.

        patch_kind_files = [
            "fortran/eccodes_f90_head.f90",
            "fortran/eccodes_f90_tail.f90",
            "fortran/grib_f90_head.f90",
            "fortran/grib_f90_tail.f90",
            "fortran/grib_types.f90",
        ]

        patch_unix_ext_files = []

        if self.run_tests:
            patch_kind_files.extend(
                [
                    "examples/F90/grib_print_data.f90",
                    "examples/F90/grib_print_data_static.f90",
                    # Files that need patching only when the extended regression
                    # tests are enabled, which we disable unconditionally:
                    # 'examples/F90/bufr_attributes.f90',
                    # 'examples/F90/bufr_expanded.f90',
                    # 'examples/F90/bufr_get_keys.f90',
                    # 'examples/F90/bufr_read_scatterometer.f90',
                    # 'examples/F90/bufr_read_synop.f90',
                    # 'examples/F90/bufr_read_temp.f90',
                    # 'examples/F90/bufr_read_tempf.f90',
                    # 'examples/F90/bufr_read_tropical_cyclone.f90',
                    # 'examples/F90/grib_clone.f90',
                    # 'examples/F90/grib_get_data.f90',
                    # 'examples/F90/grib_nearest.f90',
                    # 'examples/F90/grib_precision.f90',
                    # 'examples/F90/grib_read_from_file.f90',
                    # 'examples/F90/grib_samples.f90',
                    # 'examples/F90/grib_set_keys.f90'
                ]
            )

            patch_unix_ext_files.extend(
                [
                    "examples/F90/bufr_ecc-1284.f90",
                    "examples/F90/grib_set_data.f90",
                    "examples/F90/grib_set_packing.f90",
                    # Files that need patching only when the extended regression
                    # tests are enabled, which we disable unconditionally:
                    # 'examples/F90/bufr_copy_data.f90',
                    # 'examples/F90/bufr_get_string_array.f90',
                    # 'examples/F90/bufr_keys_iterator.f90',
                    # 'examples/F90/get_product_kind.f90',
                    # 'examples/F90/grib_count_messages_multi.f90'
                ]
            )

        kwargs = {"string": False, "backup": False, "ignore_absent": True}

        # Return the kind and not the size:
        filter_file(
            r"(^\s*kind_of_double\s*=\s*)(\d{1,2})(\s*$)",
            "\\1kind(real\\2)\\3",
            "fortran/grib_types.f90",
            **kwargs,
        )
        filter_file(
            r"(^\s*kind_of_\w+\s*=\s*)(\d{1,2})(\s*$)",
            "\\1kind(x\\2)\\3",
            "fortran/grib_types.f90",
            **kwargs,
        )

        # Replace integer kinds:
        for size, r in [(2, 4), (4, 9), (8, 18)]:
            filter_file(
                r"(^\s*integer\((?:kind=)?){0}(\).*)".format(size),
                "\\1selected_int_kind({0})\\2".format(r),
                *patch_kind_files,
                **kwargs,
            )

        # Replace real kinds:
        for size, p, r in [(4, 6, 37), (8, 15, 307)]:
            filter_file(
                r"(^\s*real\((?:kind=)?){0}(\).*)".format(size),
                "\\1selected_real_kind({0}, {1})\\2".format(p, r),
                *patch_kind_files,
                **kwargs,
            )

        # Enable getarg and exit subroutines:
        filter_file(
            r"(^\s*program\s+\w+)(\s*$)",
            "\\1; use f90_unix_env; use f90_unix_proc\\2",
            *patch_unix_ext_files,
            **kwargs,
        )

    @property
    def libs(self):
        libraries = []

        query_parameters = self.spec.last_query.extra_parameters

        if "shared" in query_parameters:
            shared = True
        elif "static" in query_parameters:
            shared = False
        else:
            shared = "+shared" in self.spec

        # Return Fortran library if requested:
        return_fortran = "fortran" in query_parameters
        # Return C library if either requested or the Fortran library is not
        # requested (to avoid overlinking) or the static libraries are
        # requested:
        return_c = "c" in query_parameters or not (return_fortran and shared)
        # Return MEMFS library only if enabled and the static libraries are
        # requested:
        return_memfs = "+memfs" in self.spec and not shared

        if return_fortran:
            libraries.append("libeccodes_f90")

        if return_c:
            libraries.append("libeccodes")

        if return_memfs:
            libraries.append("libeccodes_memfs")

        libs = find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

        if libs and len(libs) == len(libraries):
            return libs

        msg = "Unable to recursively locate {0} {1} libraries in {2}"
        raise spack.error.NoLibrariesError(
            msg.format("shared" if shared else "static", self.spec.name, self.spec.prefix)
        )

    @run_before("cmake")
    def check_fortran(self):
        if "+fortran" in self.spec and self.compiler.fc is None:
            raise InstallError("Fortran interface requires a Fortran compiler!")

    def cmake_args(self):
        jp2k = self.spec.variants["jp2k"].value

        args = [
            self.define_from_variant("ENABLE_BUILD_TOOLS", "tools"),
            self.define_from_variant("ENABLE_NETCDF", "netcdf"),
            self.define("ENABLE_JPG", jp2k != "none"),
            self.define("ENABLE_JPG_LIBJASPER", jp2k == "jasper"),
            self.define("ENABLE_JPG_LIBOPENJPEG", jp2k == "openjpeg"),
            self.define_from_variant("ENABLE_PNG", "png"),
            self.define_from_variant("ENABLE_AEC", "aec"),
            self.define_from_variant("ENABLE_ECCODES_THREADS", "pthreads"),
            self.define_from_variant("ENABLE_ECCODES_OMP_THREADS", "openmp"),
            self.define_from_variant("ENABLE_MEMFS", "memfs"),
            self.define(
                "ENABLE_PYTHON{0}".format("2" if self.spec.satisfies("@2.20.0:") else ""), False
            ),
            self.define_from_variant("ENABLE_FORTRAN", "fortran"),
            self.define("BUILD_SHARED_LIBS", "BOTH" if "+shared" in self.spec else "OFF"),
            self.define("ENABLE_TESTS", self.run_tests),
            # Examples are not installed and are just part of the test suite:
            self.define("ENABLE_EXAMPLES", self.run_tests),
            # Unconditionally disable the extended regression tests, since they
            # download additional data (~134MB):
            self.define("ENABLE_EXTRA_TESTS", False),
        ]

        if self.spec.satisfies("+netcdf"):
            # Prevent possible overriding by environment variables NETCDF_ROOT, NETCDF_DIR, and
            # NETCDF_PATH:
            args.append(self.define("NETCDF_PATH", self.spec["netcdf-c"].prefix))
            # Prevent overriding by environment variable HDF5_ROOT (starting version 2.14.0,
            # ecCodes is shipped with ecBuild 3.1.0+, which does not seem to rely on the HDF5_ROOT
            # variable):
            if self.spec.satisfies("@:2.13"):
                args.append(self.define("HDF5_ROOT", self.spec["hdf5"].prefix))

        if jp2k == "openjpeg":
            args.append(self.define("OPENJPEG_PATH", self.spec["openjpeg"].prefix))

        if self.spec.satisfies("+png"):
            args.append(self.define("ZLIB_ROOT", self.spec["zlib-api"].prefix))

        if self.spec.satisfies("+aec"):
            # Prevent overriding by environment variables AEC_DIR and AEC_PATH:
            args.append(self.define("AEC_DIR", self.spec["libaec"].prefix))

        return args

    @run_after("install")
    def install_extra_definitions(self):
        for center in self.spec.variants["extra_definitions"].value:
            if center != "none":
                center_dir = "definitions.{0}".format(center)
                install_tree(
                    join_path(self.stage.source_path, "spack-definitions", center_dir),
                    join_path(self.prefix.share.eccodes, center_dir),
                )

    def check(self):
        # https://confluence.ecmwf.int/display/ECC/ecCodes+installation
        with working_dir(self.build_directory):
            ctest()
