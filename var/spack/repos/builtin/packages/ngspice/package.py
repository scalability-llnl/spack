# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ngspice(AutotoolsPackage):
    """ngspice is the open source spice simulator for electric and
    electronic circuits."""

    homepage = "https://ngspice.sourceforge.net/"
    url = "https://sourceforge.net/projects/ngspice/files/ngspice-33.tar.gz"
    list_url = "https://sourceforge.net/projects/ngspice/files/ng-spice-rework"
    list_depth = 1
    git = "git://git.code.sf.net/p/ngspice/ngspice"

    maintainers("aweits", "cessenat")

    license("BSD-3-Clause")

    # Master version by default adds the experimental adms feature
    version("master", branch="master")
    version("43", sha256="14dd6a6f08531f2051c13ae63790a45708bd43f3e77886a6a84898c297b13699")
    version("42", sha256="737fe3846ab2333a250dfadf1ed6ebe1860af1d8a5ff5e7803c772cc4256e50a")
    version("41", sha256="1ce219395d2f50c33eb223a1403f8318b168f1e6d1015a7db9dbf439408de8c4")
    version("40", sha256="e303ca7bc0f594e2d6aa84f68785423e6bf0c8dad009bb20be4d5742588e890d")
    version("39", sha256="bf94e811eaad8aaf05821d036a9eb5f8a65d21d30e1cab12701885e09618d771")
    version("38", sha256="2c3e22f6c47b165db241cf355371a0a7558540ab2af3f8b5eedeeb289a317c56")
    version("37", sha256="9beea6741a36a36a70f3152a36c82b728ee124c59a495312796376b30c8becbe")
    version("34", sha256="2263fffc6694754972af7072ef01cfe62ac790800dad651bc290bfcae79bd7b5")
    version("33", sha256="b99db66cc1c57c44e9af1ef6ccb1dcbc8ae1df3e35acf570af578f606f8541f1")
    version("32", sha256="3cd90c4e94516d87c5b4d02a3a6405b1136b25d05c871d4fee1fd7c4c0d03ef2")
    version("31", sha256="845f3b0c962e47ded051dfbc134c3c1e4ac925c9f0ce1cb3df64eb9b9da5c282")
    version("30", sha256="08fe0e2f3768059411328a33e736df441d7e6e7304f8dad0ed5f28e15d936097")
    version("29", sha256="8d6d0ffbc15f248eb6ec3bde3b9d1397fbc95cb677e1c6a14ff46065c7f95c4a")
    version("27", sha256="0c08c7d57a2e21cf164496f3237f66f139e0c78e38345fbe295217afaf150695")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # kicad needs build=lib, i.e. --with--ngshared
    variant(
        "build",
        default="lib",
        description="Build type: lib=ngshared, bin otherwise",
        values=("lib", "bin"),
        multi=False,
    )

    variant("X", default=False, description="Use the X Window System")
    variant(
        "debug",
        default="auto",
        description="Enable debugging features: " "auto is yes for build=lib, no for build=bin",
        values=("auto", "yes", "no"),
        multi=False,
    )
    variant("xspice", default=False, description="Enable XSPICE enhancements")
    variant("cider", default=False, description="Enable CIDER enhancements")
    variant("openmp", default=False, description="Compile with multi-threading support")
    variant("readline", default=True, description="Build readline support (for bin)")
    variant("fft", default=True, description="Use external fftw lib")
    variant("osdi", default=False, description="Use osdi/OpenVAF")

    depends_on("fftw-api@3", when="+fft")
    with when("+fft+openmp"):
        depends_on("acfl threads=openmp", when="^[virtuals=fftw-api] acfl")
        depends_on("amdfftw+openmp", when="^[virtuals=fftw-api] amdfftw")
        depends_on("armpl-gcc threads=openmp", when="^[virtuals=fftw-api] armpl-gcc")
        depends_on("cray-fftw+openmp", when="^[virtuals=fftw-api] cray-fftw")
        depends_on("fftw+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("fujitsu-fftw+openmp", when="^[virtuals=fftw-api] fujitsu-fftw")
        depends_on("intel-mkl threads=openmp", when="^[virtuals=fftw-api] intel-mkl")
        depends_on("intel-oneapi-mkl threads=openmp", when="^[virtuals=fftw-api] intel-oneapi-mkl")
        depends_on(
            "intel-parallel-studio threads=openmp",
            when="^[virtuals=fftw-api] intel-parallel-studio",
        )

    with when("+fft~openmp"):
        depends_on("acfl threads=none", when="^[virtuals=fftw-api] acfl")
        depends_on("amdfftw~openmp", when="^[virtuals=fftw-api] amdfftw")
        depends_on("armpl-gcc threads=none", when="^[virtuals=fftw-api] armpl-gcc")
        depends_on("cray-fftw~openmp", when="^[virtuals=fftw-api] cray-fftw")
        depends_on("fftw~openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("fujitsu-fftw~openmp", when="^[virtuals=fftw-api] fujitsu-fftw")
        depends_on("intel-mkl threads=none", when="^[virtuals=fftw-api] intel-mkl")
        depends_on("intel-oneapi-mkl threads=none", when="^[virtuals=fftw-api] intel-oneapi-mkl")
        depends_on(
            "intel-parallel-studio threads=none", when="^[virtuals=fftw-api] intel-parallel-studio"
        )

    depends_on("readline", when="+readline build=bin")

    # Needed for autoreconf:
    depends_on("bison", type="build", when="@master")
    depends_on("flex", type="build", when="@master")

    # INSTALL indicates dependency on these :
    depends_on("freetype", when="+X build=bin")
    depends_on("libxrender", when="+X build=bin")
    depends_on("fontconfig", when="+X build=bin")
    depends_on("libxft", when="+X build=bin")
    depends_on("libxext", when="+X build=bin")
    depends_on("libxmu", when="+X build=bin")
    depends_on("libxaw", when="+X build=bin")
    depends_on("libx11", when="+X build=bin")

    # Need autotools when building on master:
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    depends_on("adms", when="@master")

    conflicts(
        "%gcc@:4.9.9",
        when="@32:",
        msg="Failure to compile recent release with old gcc due to hicum2",
    )
    conflicts("@28", msg="This release does not compile")

    @when("@master")
    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")("--adms")

    def configure_args(self):
        spec = self.spec
        args = []
        if "build=lib" in spec:
            args.append("--with-ngshared")
            # Legacy debug is activated in auto debug mode with build=lib
            if "debug=no" in spec:
                args.append("--disable-debug")
            args.append("--without-x")
        else:
            if "debug=auto" in spec or "debug=no" in spec:
                args.append("--disable-debug")
            if "+readline" in spec:
                args.append("--with-readline=yes")
            if "+X" in spec:
                args.append("--with-x")
                x = spec["libx11"]
                args.extend(
                    ["--x-includes=%s" % x.prefix.include, "--x-libraries=%s" % x.prefix.lib]
                )
            else:
                args.append("--without-x")
        if "+xspice" in spec:
            args.append("--enable-xspice")
        if "+cider" in spec:
            args.append("--enable-cider")

        if "+openmp" in spec:
            args.append("--enable-openmp")
        if "~fft" in spec:
            args.append("--with-fftw3=no")
        if "+osdi" in spec:
            args.append("--enable-osdi")
        if "darwin" in spec.architecture:
            args.append("--enable-pss")
        if "@master" in spec:
            args.append("--enable-adms")

        # Do not hide compilation line (easier to debug compilation)
        args.append("--disable-silent-rules")

        return args

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%nvhpc") and name == "cflags":
            flags.append("-Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes")
            flags.append("-Wnested-externs -Wredundant-decls")
            if "debug=yes" in self.spec:
                flags.append("-g")
        return (None, None, flags)

    def setup_run_environment(self, env):
        if "build=lib" in self.spec:
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
