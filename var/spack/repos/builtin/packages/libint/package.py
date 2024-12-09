# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.boost import Boost

TUNE_VARIANTS = (
    "none",
    "cp2k-lmax-4",
    "cp2k-lmax-5",
    "cp2k-lmax-6",
    "cp2k-lmax-7",
    "molgw-lmax-4",
    "molgw-lmax-5",
    "molgw-lmax-6",
    "molgw-lmax-7",
)


class Libint(AutotoolsPackage):
    """Libint is a high-performance library for computing
    Gaussian integrals in quantum mechanics.
    """

    homepage = "https://github.com/evaleev/libint"
    url = "https://github.com/evaleev/libint/archive/v2.1.0.tar.gz"

    maintainers("dev-zero")

    license("LGPL-3.0-only")

    version("2.9.0", sha256="4929b2f2d3e53479270be052e366e8c70fa154a7f309e5c2c23b7d394159687d")
    version("2.6.0", sha256="4ae47e8f0b5632c3d2a956469a7920896708e9f0e396ec10071b8181e4c8d9fa")
    version("2.4.2", sha256="86dff38065e69a3a51d15cfdc638f766044cb87e5c6682d960c14f9847e2eac3")
    version("2.4.1", sha256="0513be124563fdbbc7cd3c7043e221df1bda236a037027ba9343429a27db8ce4")
    version("2.4.0", sha256="52eb16f065406099dcfaceb12f9a7f7e329c9cfcf6ed9bfacb0cff7431dd6019")
    version("2.2.0", sha256="f737d485f33ac819d7f28c6ce303b1f3a2296bfd2c14f7c1323f8c5d370bb0e3")
    version("2.1.0", sha256="43c453a1663aa1c55294df89ff9ece3aefc8d1bbba5ea31dbfe71b2d812e24c8")
    version("1.1.6", sha256="f201b0c621df678cfe8bdf3990796b8976ff194aba357ae398f2f29b0e2985a6")
    version("1.1.5", sha256="ec8cd4a4ba1e1a98230165210c293632372f0e573acd878ed62e5ec6f8b6174b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("debug", default=False, description="Enable building with debug symbols")
    variant("fortran", default=False, description="Build & install Fortran bindings")
    variant(
        "tune",
        default="none",
        multi=False,
        values=TUNE_VARIANTS,
        description="Tune libint for use with the given package",
    )
    variant(
        "fma",
        default=False,
        description=(
            "Generate code utilizing FMA" " (requires capable CPU and recent enough compiler)"
        ),
    )

    # Build dependencies
    depends_on("autoconf@2.52:", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("python", type="build")
    depends_on("cmake@3.19:", when="@2.6.0:", type="build")

    # Libint 2 dependencies
    # Fixme: Can maintainers please confirm that this is a required dependency
    depends_on(Boost.with_default_variants, when="@2:")
    depends_on("gmp+cxx", when="@2:")
    depends_on("eigen", when="@2.7.0:")
    # unicode variable names in @2.9.0:
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67224
    conflicts("%gcc@:9", when="@2.9.0:", msg="libint@2.9.0: requires at least gcc 10")

    for tvariant in TUNE_VARIANTS[1:]:
        conflicts(
            "tune={0}".format(tvariant),
            when="@:2.5",
            msg=(
                "for versions prior to 2.6, tuning for specific"
                "codes/configurations is not supported"
            ),
        )

    def url_for_version(self, version):
        base_url = "https://github.com/evaleev/libint/archive"
        if version == Version("1.0.0"):
            return "{0}/LIBINT_1_00.tar.gz".format(base_url)
        elif version < Version("2.1.0"):
            return "{0}/release-{1}.tar.gz".format(base_url, version.dashed)
        else:
            return "{0}/v{1}.tar.gz".format(base_url, version)

    def autoreconf(self, spec, prefix):
        if self.spec.satisfies("@2:"):
            which("bash")("autogen.sh")
        else:
            # Fall back since autogen is not available
            libtoolize()
            aclocal("-I", "lib/autoconf")
            autoconf()

    @property
    def optflags(self):
        flags = "-O2"

        # microarchitecture-specific optimization flags should be controlled
        # by Spack, otherwise we may end up with contradictory or invalid flags
        # see https://github.com/spack/spack/issues/17794

        return flags

    def setup_build_environment(self, env):
        # Set optimization flags
        env.set("CFLAGS", self.optflags)
        env.set("CXXFLAGS", self.optflags)

        if self.spec.satisfies("%fj"):
            env.set("LDFLAGS", "--linkfortran")

        # Change AR to xiar if we compile with Intel and we
        # find the executable
        if self.spec.satisfies("%intel") and which("xiar"):
            env.set("AR", "xiar")

    def configure_args(self):
        config_args = ["--enable-shared"]

        if self.spec.satisfies("@2:"):
            # --with-boost option available only from version 2 and above
            config_args.extend(["--with-boost={0}".format(self.spec["boost"].prefix)])

        # Optimization flag names have changed in libint 2
        if self.version < Version("2.0.0"):
            config_args.extend(
                [
                    "--with-cc-optflags={0}".format(self.optflags),
                    "--with-cxx-optflags={0}".format(self.optflags),
                ]
            )
        else:
            config_args.extend(
                [
                    "--with-cxx-optflags={0}".format(self.optflags),
                    "--with-cxxgen-optflags={0}".format(self.optflags),
                ]
            )

        # Options required by CP2K, removed in libint 2
        if self.version < Version("2.0.0"):
            config_args.extend(["--with-libint-max-am=5", "--with-libderiv-max-am1=4"])

        if self.spec.satisfies("@2.6.0:"):
            config_args += ["--with-libint-exportdir=generated"]
            config_args += self.enable_or_disable("debug", activation_value=lambda x: "opt")
            config_args += self.enable_or_disable("fma")

            tune_value = self.spec.variants["tune"].value
            if tune_value.startswith("cp2k"):
                lmax = int(tune_value.split("-lmax-")[1])
                config_args += [
                    "--enable-eri=1",
                    "--enable-eri2=1",
                    "--enable-eri3=1",
                    "--with-max-am={0}".format(lmax),
                    "--with-eri-max-am={0},{1}".format(lmax, lmax - 1),
                    "--with-eri2-max-am={0},{1}".format(lmax + 2, lmax + 1),
                    "--with-eri3-max-am={0},{1}".format(lmax + 2, lmax + 1),
                    "--with-opt-am=3",
                    # keep code-size at an acceptable limit,
                    # cf. https://github.com/evaleev/libint/wiki#program-specific-notes:
                    "--enable-generic-code",
                    "--disable-unrolling",
                ]
            if tune_value.startswith("molgw"):
                lmax = int(tune_value.split("-lmax-")[1])
                config_args += [
                    "--enable-1body=1",
                    "--enable-eri=0",
                    "--enable-eri2=0",
                    "--enable-eri3=0",
                    "--with-multipole-max-order=0",
                    "--with-max-am={0}".format(lmax),
                    "--with-eri-max-am={0}".format(lmax),
                    "--with-eri2-max-am={0}".format(lmax),
                    "--with-eri3-max-am={0}".format(lmax),
                    "--with-opt-am=2",
                    "--enable-contracted-ints",
                    # keep code-size at an acceptable limit,
                    # cf. https://github.com/evaleev/libint/wiki#program-specific-notes:
                    "--enable-generic-code",
                    "--disable-unrolling",
                ]

        return config_args

    @property
    def build_targets(self):
        if self.spec.satisfies("@2.6.0:"):
            return ["export"]

        return []

    @when("@2.6.0:")
    def build(self, spec, prefix):
        """
        Starting from libint 2.6.0 we're using the 2-stage build
        to get support for the Fortran bindings, required by some
        packages (CP2K notably).
        """

        # upstream says that using configure/make for the generated code
        # is deprecated and one should use CMake

        # skip tarball creation and removal of dir with generated code
        filter_file("&& rm -rf $(EXPORTDIR)", "", "export/Makefile", string=True)

        make("export")
        # now build the library
        with working_dir(os.path.join(self.build_directory, "generated")):
            if spec.satisfies("@2.6.0"):
                config_args = [
                    f"--prefix={prefix}",
                    "--enable-shared",
                    f"--with-boost={spec['boost'].prefix}",
                    f"--with-cxx-optflags={self.optflags}",
                ]
                config_args += self.enable_or_disable("debug", activation_value=lambda x: "opt")
                config_args += self.enable_or_disable("fortran")
                configure = Executable("./configure")
                configure(*config_args)
                make()
            else:
                cmake_args = [
                    "..",
                    f"-DCMAKE_INSTALL_PREFIX={prefix}",
                    "-DLIBINT2_BUILD_SHARED_AND_STATIC_LIBS=ON",
                ]
                if spec.satisfies("+fortran"):
                    cmake_args.append("-DENABLE_FORTRAN=ON")
                if spec.satisfies("+debug"):
                    cmake_args.append("CMAKE_BUILD_TYPE=Debug")
                cmake = Executable("cmake")
                mkdirp("build")
                with working_dir("build"):
                    cmake(*cmake_args)
                    make()

    @when("@2.6.0:")
    def check(self):
        path = join_path(self.build_directory, "generated")
        if self.spec.satisfies("@2.9.0:"):
            path = join_path(path, "build")
        with working_dir(path):
            make("check")

    @when("@2.6.0:")
    def install(self, spec, prefix):
        path = join_path(self.build_directory, "generated")
        if self.spec.satisfies("@2.9.0:"):
            path = join_path(path, "build")
        with working_dir(path):
            make("install")

    @when("@:2.6.0")
    def patch(self):
        # Use Fortran compiler to link the Fortran example, not the C++
        # compiler
        if self.spec.satisfies("+fortran"):
            if not self.spec.satisfies("%fj"):
                filter_file(
                    "$(CXX) $(CXXFLAGS)",
                    "$(FC) $(FCFLAGS)",
                    "export/fortran/Makefile",
                    string=True,
                )

    @property
    def libs(self):
        return find_libraries("libint2", self.spec.prefix, shared=True, recursive=True)
