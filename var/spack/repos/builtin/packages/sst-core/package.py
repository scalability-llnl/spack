# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstCore(AutotoolsPackage):
    """The Structural Simulation Toolkit (SST) core
    provides a parallel discrete event simulation (PDES)
    framework for performing architecture simulations
    of existing and proposed HPC systems"""

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/sstsimulator/sst-core.git"
    url = "https://github.com/sstsimulator/sst-core/releases/download/v14.1.0_Final/sstcore-14.1.0.tar.gz"

    maintainers("berquist", "naromero77")

    license("BSD-3-Clause")

    version("14.1.0", sha256="9d17c37d1ebdff8d8eb10ab0084eb901c78a7c5a76db15189e3d7fc318fd6f9d")
    version("14.0.0", sha256="fadc7ee99472ff3ac5d4b3f3e507123e32bd9fb89c4c6b48fbd2dca8aeb8b8d6")
    version("13.1.0", sha256="0a44c62ee0b18a20a3cb089f4e0d43e293dc5adc6c3fa7639d40986cf5b9854c")
    version("13.0.0", sha256="c9d868dcdd75d59bef7c73146709a3b2a52a78f0df5ec2c3dc9f21434c51d935")
    version("12.1.0", sha256="f7530226643439678e2f4183ec4dbadf7750411bdaa44d9443887f81feb97574")
    version("12.0.1", sha256="8662a778354e587e55b909725943dd5bb01d55121b1abc1a384a4eea161e9f5a")
    version("12.0.0", sha256="fae3e092e508ab297ec60941a71f772f3b9247581ef407284700868158443066")
    version("11.1.0", sha256="b3967944a5dc329f0ae32e7e3355bd991346632d8d30290d2a11e6731ce73736")
    version("11.0.0", sha256="25d17c35d1121330ad74375b6d27fe5c5592d1add3edf0bbb356aa3b5f59f401")
    version("10.1.0", sha256="e464213a81c7b3ccec994fdba2b56992b52fb9a6db089ef7c3445b54306d4b87")
    version("10.0.0", sha256="64cf93a46dfab011fba49244bf0e0efe25ef928c6fbde1d49003220d0eb7735a")
    version("9.1.0", sha256="cfeda39bb2ce9f32032480427517df62e852c0b3713797255e3b838075f3614d")
    version("9.0.0", sha256="1a5763c51429ae941fb59e6f0b76b7754477cc302ef7a1958afd2b74186b2a11")
    version("8.0.0", sha256="34a62425c3209cf80b6bca99cb0dcc328b67fb84ed92d5e6d6c975ad9319ba8a")
    version("7.2.0", sha256="3015579bbbc7a9de0eb984cea248acc02303d779b8ed5eee640c4a5532a2cfdb")
    version("7.1.0", sha256="06accc9b203311a752b86e775c379f3bb56e4b95eda658769f7d92a11765aa06")
    version("7.0.0", sha256="818c5923688b5c8b98669ebd49c5b2493e9414c61be57eec1e9944d191b4a309")
    version("6.1.0", sha256="3b2840efe90fc312818e680a49fa01c7eb25a337d8a8d0d9374bd31887330a0c")
    version("6.0.0", sha256="ecfde0409e7345d88950f9d2dc531709878a19469d8ade71517337eec525e379")

    version("develop", branch="devel")
    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    variant(
        "pdes_mpi",
        default=True,
        description="Build support for parallel discrete event simulation",
    )
    variant(
        "zoltan",
        default=False,
        when="@:12.0",
        description="Use Zoltan for partitioning parallel runs",
    )
    variant("hdf5", default=False, description="Build support for HDF5 statistic output")
    variant("zlib", default=False, description="Build support for ZLIB compression")
    # Starting with 0bc4832f3f87aa78d1efd3e15743eb059dc03250 and then 14.0.0.
    variant(
        "curses",
        default=True,
        when="@develop,master",
        description="Build support for interactive sst-info",
    )

    variant("trackevents", default=False, description="Enable event and activity tracking")
    variant(
        "trackperf",
        default=False,
        description="Enable tracking of simulator performance and component runtime",
    )
    variant("preview", default=False, description="Preview build with deprecated features removed")
    variant("profile", default=False, description="Enable performance profiling of core features")

    depends_on("python@:3.11", type=("build", "run", "link"))
    depends_on("mpi", when="+pdes_mpi")
    depends_on("zoltan", when="+zoltan")
    depends_on("hdf5", when="+hdf5")
    depends_on("zlib-api", when="+zlib")
    depends_on("gettext")
    depends_on("ncurses", when="+curses")

    for version_name in ("master", "develop"):
        depends_on("autoconf@1.68:", type="build", when="@{}".format(version_name))
        depends_on("automake@1.11.1:", type="build", when="@{}".format(version_name))
        depends_on("libtool@1.2.4:", type="build", when="@{}".format(version_name))
        depends_on("m4", type="build", when="@{}".format(version_name))

    # force out-of-source builds
    build_directory = "spack-build"

    @when("@develop,master")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("autogen.sh")

    def configure_args(self):
        args = []
        if "+zoltan" in self.spec:
            args.append("--with-zoltan=%s" % self.spec["zoltan"].prefix)
        if "+hdf5" in self.spec:
            args.append("--with-hdf5=%s" % self.spec["hdf5"].prefix)
        if "+zlib" in self.spec:
            args.append("--with-zlib=%s" % self.spec["zlib-api"].prefix)
        if "+curses" in self.spec:
            args.append("--with-curses={}".format(self.spec["ncurses"].prefix))

        if "+pdes_mpi" in self.spec:
            args.append("--enable-mpi")
            env["CC"] = self.spec["mpi"].mpicc
            env["CXX"] = self.spec["mpi"].mpicxx
            env["F77"] = self.spec["mpi"].mpif77
            env["FC"] = self.spec["mpi"].mpifc
        else:
            args.append("--disable-mpi")

        if "+trackevents" in self.spec:
            args.append("--enable-event-tracking")
        if "+trackperf" in self.spec:
            args.append("--enable-perf-tracking")
        if "+preview" in self.spec:
            args.append("--enable-preview-build")
        if "+profile" in self.spec:
            args.append("--enable-profile")

        args.append("--with-python=%s" % self.spec["python"].prefix)
        return args

    def patch(self):
        """The Autotools-based setup does not add Python to the RPATH or RUNPATH."""
        self.rpath.append(self.spec["python"].prefix.lib)
