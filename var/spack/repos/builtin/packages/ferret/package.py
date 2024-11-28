# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Ferret(Package):
    """Ferret is an interactive computer visualization and analysis environment
    designed to meet the needs of oceanographers and meteorologists
    analyzing large and complex gridded data sets."""

    homepage = "https://ferret.pmel.noaa.gov/Ferret/home"
    url = "https://github.com/NOAA-PMEL/Ferret/archive/v7.6.0.tar.gz"

    maintainers("RemiLacroix-IDRIS")

    license("Unlicense")

    version("7.6.0", sha256="69832d740bd44c9eadd198a5de4d96c4c01ae90ae28c2c3414c1bb9f43e475d1")
    version("7.5.0", sha256="2a038c547e6e80e6bd0645a374c3247360cf8c94ea56f6f3444b533257eb16db")
    version("7.4", sha256="5167bb9e6ef441ae9cf90da555203d2155e3fcf929e7b8dddb237de0d58c5e5f")
    version("7.3", sha256="ae80a732c34156b5287a23696cf4ae4faf4de1dd705ff43cbb4168b05c6faaf4")
    version("7.2", sha256="21c339b1bafa6939fc869428d906451f130f7e77e828c532ab9488d51cf43095")
    version("6.96", sha256="7eb87156aa586cfe838ab83f08b2102598f9ab62062d540a5da8c9123816331a")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("datasets", default=False, description="Install Ferret standard datasets")

    depends_on("hdf5+hl")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("readline")
    depends_on("zlib-api")
    depends_on("libx11")
    depends_on("curl")

    # Make Java dependency optional with older versions of Ferret
    patch(
        "https://github.com/NOAA-PMEL/Ferret/commit/c7eb70a0b17045c8ca7207d586bfea77a5340668.patch?full_index=1",
        sha256="6dd0a6b11c103b0097fba3da06d6e655da9770e8f568a15968d9b64a0f3c2315",
        level=1,
        working_dir="FERRET",
        when="@:6",
    )

    resource(
        name="datasets",
        url="https://github.com/NOAA-PMEL/FerretDatasets/archive/v7.6.tar.gz",
        sha256="b2fef758ec1817c1c19e6225857ca3a82c727d209ed7fd4697d45c5533bb2c72",
        placement="fer_dsets",
        when="+datasets",
    )

    def url_for_version(self, version):
        if version <= Version("7.2"):
            return "ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v{0}.tar.gz".format(
                version.joined
            )
        else:
            return "https://github.com/NOAA-PMEL/Ferret/archive/v{0}.tar.gz".format(version)

    def flag_handler(self, name, flags):
        if name == "fflags" and self.spec.satisfies("%gcc@10:"):
            flags.extend(["-fallow-argument-mismatch", "-fallow-invalid-boz"])
        return (flags, None, None)

    def patch(self):
        spec = self.spec
        hdf5_prefix = spec["hdf5"].prefix
        netcdff_prefix = spec["netcdf-fortran"].prefix
        readline_prefix = spec["readline"].prefix
        libz_prefix = spec["zlib-api"].prefix

        work_dir = "FERRET" if "@:7.2" in spec else "."
        with working_dir(work_dir, create=False):
            if spec.satisfies("@7.3:"):
                copy("site_specific.mk.in", "site_specific.mk")
                copy(
                    "external_functions/ef_utility/site_specific.mk.in",
                    "external_functions/ef_utility/site_specific.mk",
                )

                filter_file(
                    r"^DIR_PREFIX.+",
                    "DIR_PREFIX = %s" % self.stage.source_path,
                    "site_specific.mk",
                )
                # Setting this to blank not to force
                # using the static version of readline
                filter_file(r"^(READLINE_(LIB)?DIR).+", "\\1 = ", "site_specific.mk")
            else:
                filter_file(r"^LIBZ_DIR.+", "LIBZ_DIR = %s" % libz_prefix, "site_specific.mk")
                filter_file(r"^JAVA_HOME.+", " ", "site_specific.mk")
                filter_file(
                    r"^READLINE_DIR.+", "READLINE_DIR = %s" % readline_prefix, "site_specific.mk"
                )

            filter_file(r"^BUILDTYPE.+", "BUILDTYPE = x86_64-linux", "site_specific.mk")
            filter_file(
                r"^INSTALL_FER_DIR.+", "INSTALL_FER_DIR = %s" % spec.prefix, "site_specific.mk"
            )
            filter_file(r"^(HDF5_(LIB)?DIR).+", "\\1 = %s" % hdf5_prefix, "site_specific.mk")
            filter_file(
                r"^(NETCDF4?_(LIB)?DIR).+", "\\1 = %s" % netcdff_prefix, "site_specific.mk"
            )

            if spec.satisfies("@:7.3"):
                # Don't force using the static version of libz
                filter_file(
                    r"\$\(LIBZ_DIR\)/lib64/libz.a", "-lz", "platform_specific.mk.x86_64-linux"
                )

                # Don't force using the static version of libgfortran
                filter_file(
                    r"-Wl,-Bstatic -lgfortran -Wl,-Bdynamic",
                    "-lgfortran",
                    "platform_specific.mk.x86_64-linux",
                )

                # This prevents the rpaths to be properly set
                # by Spack's compiler wrappers
                filter_file(r"-v --verbose", "", "platform_specific.mk.x86_64-linux")

                filter_file(
                    r"^[ \t]*LD[ \t]*=.+",
                    "LD = %s" % spack_cc,
                    "platform_specific.mk.x86_64-linux",
                )
            else:
                # Don't force using the static version of libgfortran
                filter_file(r"-static-libgfortran", "", "platform_specific.mk.x86_64-linux")

            if spec.satisfies("@:7.4"):
                compilers_spec_file = "platform_specific.mk.x86_64-linux"
            else:
                compilers_spec_file = "site_specific.mk"

            # Make sure Ferret uses Spack's compiler wrappers
            filter_file(r"^[ \t]*CC[ \t]*=.+", "CC = %s" % spack_cc, compilers_spec_file)
            filter_file(r"^[ \t]*CXX[ \t]*=.+", "CXX = %s" % spack_cxx, compilers_spec_file)
            filter_file(r"^[ \t]*FC[ \t]*=.+", "FC = %s" % spack_fc, compilers_spec_file)
            filter_file(r"^[ \t]*F77[ \t]*=.+", "F77 = %s" % spack_f77, compilers_spec_file)

            filter_file(
                r"\$\(NETCDF4?_(LIB)?DIR\).*/libnetcdff.a",
                "-L%s -lnetcdff" % spec["netcdf-fortran"].prefix.lib,
                "platform_specific.mk.x86_64-linux",
            )
            filter_file(
                r"\$\(NETCDF4?_(LIB)?DIR\).*/libnetcdf.a",
                "-L%s -lnetcdf" % spec["netcdf-c"].prefix.lib,
                "platform_specific.mk.x86_64-linux",
            )
            filter_file(
                r"\$\(HDF5_(LIB)?DIR\).*/libhdf5_hl.a",
                "-L%s -lhdf5_hl" % spec["hdf5"].prefix.lib,
                "platform_specific.mk.x86_64-linux",
            )
            filter_file(
                r"\$\(HDF5_(LIB)?DIR\).*/libhdf5.a",
                "-L%s -lhdf5" % spec["hdf5"].prefix.lib,
                "platform_specific.mk.x86_64-linux",
            )

    def install(self, spec, prefix):
        if "LDFLAGS" in env and env["LDFLAGS"]:
            env["LDFLAGS"] += " " + "-lquadmath"
        else:
            env["LDFLAGS"] = "-lquadmath"

        work_dir = "FERRET" if "@:7.2" in self.spec else "."
        with working_dir(work_dir, create=False):
            os.environ["LD_X11"] = "-L%s -lX11" % spec["libx11"].prefix.lib
            os.environ["HOSTTYPE"] = "x86_64-linux"
            make(parallel=False)
            make("install")

        if self.spec.satisfies("+datasets"):
            mkdir(self.prefix.fer_dsets)
            install_tree("fer_dsets", self.prefix.fer_dsets)

    def setup_run_environment(self, env):
        env.set("FER_DIR", self.prefix)
        env.set(
            "FER_GO", " ".join([".", self.prefix.go, self.prefix.examples, self.prefix.contrib])
        )
        env.set("FER_EXTERNAL_FUNCTIONS", self.prefix.ext_func.libs)
        env.set("FER_PALETTE", " ".join([".", self.prefix.ppl]))
        env.set("FER_FONTS", self.prefix.ppl.fonts)

        fer_data = ["."]
        fer_descr = ["."]
        fer_grids = ["."]

        if self.spec.satisfies("+datasets"):
            env.set("FER_DSETS", self.prefix.fer_dsets)

            fer_data.append(self.prefix.fer_dsets.data)
            fer_descr.append(self.prefix.fer_dsets.descr)
            fer_grids.append(self.prefix.fer_dsets.grids)

        fer_data.extend([self.prefix.go, self.prefix.examples])
        env.set("FER_DATA", " ".join(fer_data))
        env.set("FER_DESCR", " ".join(fer_descr))
        env.set("FER_GRIDS", " ".join(fer_grids))
