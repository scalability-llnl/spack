# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import is_system_path


class Silo(AutotoolsPackage):
    """Silo is a library for reading and writing a wide variety of scientific
    data to binary, disk files."""

    homepage = "https://wci.llnl.gov/simulation/computer-codes/silo"
    git = "https://github.com/LLNL/Silo.git"
    url = "https://wci.llnl.gov/sites/wci/files/2021-01/silo-4.10.2.tgz"
    maintainers("patrickb314")

    version(
        "4.11.1",
        preferred=True,
        sha256="49eddc00304aa4a19074b099559edbdcaa3532c98df32f99aa62b9ec3ea7cee2",
        url="https://github.com/LLNL/Silo/releases/download/4.11.1/silo-4.11.1.tar.xz",
    )
    version(
        "4.11.1-bsd",
        sha256="51ccfdf3c09dfc98c7858a0a6f08cc3b2a07ee3c4142ee6482ba7b24e314c2aa",
        url="https://github.com/LLNL/Silo/releases/download/4.11.1/silo-4.11.1-bsd.tar.xz",
    )
    version(
        "4.11",
        sha256="ab936c1f4fc158d9fdc4415965f7d9def7f4abeca596fe5a25bd8485654898ac",
        url="https://github.com/LLNL/Silo/releases/download/v4.11/silo-4.11.tar.gz",
    )
    version(
        "4.11-bsd",
        sha256="6d0a85a079d48fcdcc0084ecb5fc4cfdcc64852edee780c60cb244d16f4bc4ec",
        url="https://github.com/LLNL/Silo/releases/download/v4.11/silo-4.11-bsd.tar.gz",
    )
    version(
        "4.10.2",
        sha256="3af87e5f0608a69849c00eb7c73b11f8422fa36903dd14610584506e7f68e638",
        preferred=True,
    )
    version(
        "4.10.2-bsd",
        sha256="4b901dfc1eb4656e83419a6fde15a2f6c6a31df84edfad7f1dc296e01b20140e",
        url="https://wci.llnl.gov/sites/wci/files/2021-01/silo-4.10.2-bsd.tgz",
    )
    version("4.9", sha256="90f3d069963d859c142809cfcb034bc83eb951f61ac02ccb967fc8e8d0409854")
    version("4.8", sha256="c430c1d33fcb9bc136a99ad473d535d6763bd1357b704a915ba7b1081d58fb21")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("python", default=True, description="Enable Python support")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("shared", default=True, description="Build shared libraries")
    variant("silex", default=False, description="Builds Silex, a GUI for viewing Silo files")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("mpi", default=True, description="Compile with MPI Compatibility")
    variant("hdf5", default=True, description="Support HDF5 for database I/O")
    variant("hzip", default=True, description="Enable hzip support")
    variant("fpzip", default=True, description="Enable fpzip support")

    depends_on("perl", type="build")
    depends_on("m4", type="build", when="+shared")
    depends_on("autoconf", type="build", when="+shared")
    depends_on("autoconf-archive", type="build", when="+shared")
    depends_on("automake", type="build", when="+shared")
    depends_on("libtool", type="build", when="+shared")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5@1.8:1.10", when="@:4.10+hdf5")
    depends_on("hdf5@1.12:", when="@4.11:+hdf5")
    depends_on("qt+gui~framework@4.8:4.9", when="+silex")
    depends_on("libx11", when="+silex")
    # Xmu dependency is required on Ubuntu 18-20
    depends_on("libxmu", when="+silex")
    depends_on("readline")
    depends_on("zlib-api")

    patch("remove-mpiposix.patch", when="@4.8:4.10.2")

    # hdf5 1.10 added an additional field to the H5FD_class_t struct
    patch("H5FD_class_t-terminate.patch", when="@:4.10.2-bsd")

    # H5EPR_SEMI_COLON.patch was fixed in current dev
    patch("H5EPR_SEMI_COLON.patch", when="@:4.11-bsd")

    # Fix missing F77 init, fixed in 4.9
    patch("48-configure-f77.patch", when="@:4.8")

    # The previously used AX_CHECK_COMPILER_FLAGS macro was dropped from
    # autoconf-archive in 2011
    patch("configure-AX_CHECK_COMPILE_FLAG.patch", when="@:4.11-bsd")

    # API changes in hdf5-1.13 cause breakage
    # See https://github.com/LLNL/Silo/pull/260
    patch("hdf5-113.patch", when="@4.11:4.11-bsd +hdf5 ^hdf5@1.13:")
    conflicts("^hdf5@1.13:", when="@:4.10.2-bsd")

    # hzip and fpzip are not available in the BSD releases
    conflicts("+hzip", when="@4.10.2-bsd,4.11-bsd")
    conflicts("+fpzip", when="@4.10.2-bsd,4.11-bsd")

    # zfp include missing
    patch("zfp_error.patch", when="@4.11:4.11-bsd +hdf5")

    # use /usr/bin/env perl for portability
    patch("mkinc-usr-bin-env-perl.patch", when="@:4.11-bsd")

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "ldflags":
            if "+hdf5" in spec:
                if spec["hdf5"].satisfies("~shared"):
                    flags.append("-ldl")

        if "+pic" in spec:
            if name == "cflags":
                flags.append(self.compiler.cc_pic_flag)
            elif name == "cxxflags":
                flags.append(self.compiler.cxx_pic_flag)
            elif name == "fcflags":
                flags.append(self.compiler.fc_pic_flag)
        if name == "cflags" or name == "cxxflags":
            if spec.satisfies("%oneapi"):
                flags.append("-Wno-error=int")
                flags.append("-Wno-error=int-conversion")
            if "+hdf5" in spec:
                # @:4.10 can use up to the 1.10 API
                if "@:4.10" in spec:
                    if "@1.10:" in spec["hdf5"]:
                        flags.append("-DH5_USE_110_API")
                    elif "@1.8:" in spec["hdf5"]:
                        # Just in case anytone is trying to force the 1.6 api for
                        # some reason
                        flags.append("-DH5_USE_18_API")
                else:
                    # @4.11: can use newer HDF5 APIs, so this ensures silo is
                    # presented with an HDF5 API consistent with the HDF5 version.
                    # Use the latest even-numbered API version, i.e. v1.13.1 uses
                    # API v1.12
                    maj_ver = int(spec["hdf5"].version[0])
                    min_ver = int(spec["hdf5"].version[1])
                    min_apiver = int(min_ver / 2) * 2
                    flags.append("-DH5_USE_{0}{1}_API".format(maj_ver, min_apiver))

            if spec.compiler.name in ["clang", "apple-clang"]:
                flags.append("-Wno-implicit-function-declaration")
        return (flags, None, None)

    @when("%clang@9:")
    def patch(self):
        self.clang_9_patch()

    @when("%apple-clang@11.0.3:")
    def patch(self):
        self.clang_9_patch()

    def clang_9_patch(self):
        # Clang 9 and later include macro definitions in <math.h> that conflict
        # with typedefs DOMAIN and RANGE used in Silo plugins.
        # It looks like the upstream fpzip repo has been fixed, but that change
        # hasn't yet made it into silo.
        # https://github.com/LLNL/fpzip/blob/master/src/pcmap.h

        if str(self.spec.version).endswith("-bsd"):
            # The files below don't exist in the BSD licenced version
            return

        def repl(match):
            # Change macro-like uppercase to title-case.
            return match.group(1).title()

        files_to_filter = [
            "src/fpzip/codec.h",
            "src/fpzip/pcdecoder.inl",
            "src/fpzip/pcencoder.inl",
            "src/fpzip/pcmap.h",
            "src/fpzip/pcmap.inl",
            "src/fpzip/read.cpp",
            "src/fpzip/write.cpp",
            "src/hzip/hzmap.h",
            "src/hzip/hzresidual.h",
        ]

        filter_file(r"\b(DOMAIN|RANGE|UNION)\b", repl, *files_to_filter)

    @property
    def force_autoreconf(self):
        # Update autoconf's tests whether libtool supports shared libraries.
        # (Otherwise, shared libraries are always disabled on Darwin.)
        if self.spec.satisfies("@4.11-bsd") or self.spec.satisfies("@4.10.2-bsd"):
            return False
        else:
            return self.spec.satisfies("+shared")

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-install-lite-headers"]

        config_args.extend(self.enable_or_disable("pythonmodule", variant="python"))
        config_args.extend(self.enable_or_disable("fortran"))
        config_args.extend(self.enable_or_disable("silex"))
        config_args.extend(self.enable_or_disable("shared"))
        config_args.extend(self.enable_or_disable("hzip"))
        config_args.extend(self.enable_or_disable("fpzip"))

        # Do not specify the prefix of zlib if it is in a system directory
        # (see https://github.com/spack/spack/pull/21900).
        zlib_prefix = self.spec["zlib-api"].prefix
        if is_system_path(zlib_prefix):
            config_args.append("--with-zlib=yes")
        else:
            config_args.append("--with-zlib=%s,%s" % (zlib_prefix.include, zlib_prefix.lib))

        if "+hdf5" in spec:
            config_args.append(
                "--with-hdf5=%s,%s" % (spec["hdf5"].prefix.include, spec["hdf5"].prefix.lib)
            )

        if "+silex" in spec:
            x = spec["libx11"]
            config_args.extend(
                [
                    "--with-Qt-dir=" + spec["qt"].prefix,
                    "--with-Qt-lib=QtGui -lQtCore",
                    "--x-includes=" + x.prefix.include,
                    "--x-libraries=" + x.prefix.lib,
                ]
            )

        if "+mpi" in spec:
            config_args.append("CC=%s" % spec["mpi"].mpicc)
            config_args.append("CXX=%s" % spec["mpi"].mpicxx)
            config_args.append("FC=%s" % spec["mpi"].mpifc)

        return config_args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libsilo*", root=self.prefix, shared=shared, recursive=True)
