# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
from shutil import Error, copyfile

from spack.package import *


class NetcdfFortran(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the Fortran
    distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url = "https://downloads.unidata.ucar.edu/netcdf-fortran/4.5.4/netcdf-fortran-4.5.4.tar.gz"

    maintainers("skosukhin", "WardF")

    license("Apache-2.0")

    version("4.6.1", sha256="b50b0c72b8b16b140201a020936aa8aeda5c79cf265c55160986cd637807a37a")
    version("4.6.0", sha256="198bff6534cc85a121adc9e12f1c4bc53406c403bda331775a1291509e7b2f23")
    version("4.5.4", sha256="0a19b26a2b6e29fab5d29d7d7e08c24e87712d09a5cafeea90e16e0a2ab86b81")
    version("4.5.3", sha256="123a5c6184336891e62cf2936b9f2d1c54e8dee299cfd9d2c1a1eb05dd668a74")
    version("4.5.2", sha256="b959937d7d9045184e9d2040a915d94a7f4d0185f4a9dceb8f08c94b0c3304aa")
    version("4.4.5", sha256="2467536ce29daea348c736476aa8e684c075d2f6cab12f3361885cb6905717b8")
    version("4.4.4", sha256="b2d395175f8d283e68c8be516e231a96b191ade67ad0caafaf7fa01b1e6b5d75")
    version("4.4.3", sha256="330373aa163d5931e475b5e83da5c1ad041e855185f24e6a8b85d73b48d6cda9")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enable shared library")
    variant("doc", default=False, description="Enable building docs")

    depends_on("netcdf-c")
    depends_on("netcdf-c@4.7.4:", when="@4.5.3:")  # nc_def_var_szip required
    depends_on("doxygen", when="+doc", type="build")

    # We need to use MPI wrappers when building against static MPI-enabled NetCDF and/or HDF5:
    with when("^netcdf-c~shared"):
        depends_on("mpi", when="^netcdf-c+mpi")
        depends_on("mpi", when="^netcdf-c+parallel-netcdf")
        depends_on("mpi", when="^hdf5+mpi~shared")

    # Enable 'make check' for NAG, which is too strict.
    patch("nag_testing.patch", when="@4.4.5%nag")

    # File fortran/nf_logging.F90 is compiled without -DLOGGING, which leads
    # to missing symbols in the library. Additionally, the patch enables
    # building with NAG, which refuses to compile empty source files (see also
    # comments in the patch):
    patch("logging.patch", when="@:4.4.5")

    # Prevent excessive linking to system libraries. Without this patch the
    # library might get linked to the system installation of libcurl. See
    # https://github.com/Unidata/netcdf-fortran/commit/0a11f580faebbc1c4dce68bf5135709d1c7c7cc1#diff-67e997bcfdac55191033d57a16d1408a
    patch("excessive_linking.patch", when="@4.4.5")

    # Parallel builds do not work in the fortran directory. This patch is
    # derived from https://github.com/Unidata/netcdf-fortran/pull/211
    patch("no_parallel_build.patch", when="@4.5.2")

    filter_compiler_wrappers("nf-config", relative_root="bin")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if "+pic" in self.spec:
                flags.append(self.compiler.cc_pic_flag)
        elif name == "fflags":
            if "+pic" in self.spec:
                flags.append(self.compiler.f77_pic_flag)
            if self.spec.satisfies("%gcc@10:"):
                # https://github.com/Unidata/netcdf-fortran/issues/212
                flags.append("-fallow-argument-mismatch")
            elif self.compiler.name == "cce":
                # Cray compiler generates module files with uppercase names by
                # default, which is not handled by the makefiles of
                # NetCDF-Fortran:
                # https://github.com/Unidata/netcdf-fortran/pull/221.
                # The following flag forces the compiler to produce module
                # files with lowercase names.
                flags.append("-ef")

        # Note that cflags and fflags should be added by the compiler wrapper
        # and not on the command line to avoid overriding the default
        # compilation flags set by the configure script:
        return flags, None, None

    @property
    def libs(self):
        libraries = ["libnetcdff"]

        query_parameters = self.spec.last_query.extra_parameters

        if "shared" in query_parameters:
            shared = True
        elif "static" in query_parameters:
            shared = False
        else:
            shared = "+shared" in self.spec

        libs = find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

        if libs:
            return libs

        msg = "Unable to recursively locate {0} {1} libraries in {2}"
        raise NoLibrariesError(
            msg.format("shared" if shared else "static", self.spec.name, self.spec.prefix)
        )

    def configure_args(self):
        config_args = ["--enable-static"]
        config_args += self.enable_or_disable("shared")
        config_args += self.enable_or_disable("doxygen", variant="doc")

        netcdf_c_spec = self.spec["netcdf-c"]
        if "+mpi" in netcdf_c_spec or "+parallel-netcdf" in netcdf_c_spec:
            # Prefixing with 'mpiexec -n 4' is not necessarily the correct way
            # to launch MPI programs on a particular machine (e.g. 'srun -n 4'
            # with additional arguments might be the right one). Therefore, we
            # make sure the parallel tests are not launched at all (although it
            # is the default behaviour currently):
            config_args.append("--disable-parallel-tests")
            if self.spec.satisfies("@4.5.0:4.5.2"):
                # Versions from 4.5.0 to 4.5.2 check whether the Fortran MPI
                # interface is available and fail the configuration if it is
                # not. However, the interface is needed for a subset of the test
                # programs only (the library itself does not need it), which are
                # not run by default and explicitly disabled above. To avoid the
                # configuration failure, we set the following cache variable:
                config_args.append("ac_cv_func_MPI_File_open=yes")

        if "~shared" in netcdf_c_spec:
            nc_config = which("nc-config")
            config_args.append("LIBS={0}".format(nc_config("--libs", output=str).strip()))
            if any(s in netcdf_c_spec for s in ["+mpi", "+parallel-netcdf", "^hdf5+mpi~shared"]):
                config_args.append("CC=%s" % self.spec["mpi"].mpicc)

        return config_args

    def check(self):
        make("check", parallel=self.spec.satisfies("@4.5:"))

    @run_after("install")
    def cray_module_filenames(self):
        # Cray compiler searches for module files with uppercase names by
        # default and with lowercase names when the '-ef' flag is specified.
        # To avoid warning messages when compiler user applications in both
        # cases, we create copies of all '*.mod' files in the prefix/include
        # with names in upper- and lowercase.
        if not self.spec.satisfies("%cce"):
            return

        with working_dir(self.spec.prefix.include):
            for f in glob.glob("*.mod"):
                name, ext = os.path.splitext(f)
                try:
                    # Create a copy with uppercase name:
                    copyfile(f, name.upper() + ext)
                except Error:
                    # Assume that the exception tells us that the file with
                    # uppercase name already exists. Try to create a file with
                    # lowercase name then:
                    try:
                        copyfile(f, name.lower() + ext)
                    except Error:
                        pass
