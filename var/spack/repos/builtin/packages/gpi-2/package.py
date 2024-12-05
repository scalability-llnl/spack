# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import environ

from spack.package import *


class Gpi2(AutotoolsPackage):
    """GPI-2 implements GASPI specification, an API specification for
    asynchronous communication. It provides a flexible, scalable and
    fault tolerant interface for parallel applications.
    """

    homepage = "http://www.gpi-site.com"
    url = "https://github.com/cc-hpc-itwm/GPI-2/archive/refs/tags/v1.5.1.tar.gz"
    git = "https://github.com/cc-hpc-itwm/GPI-2.git"

    maintainers("robert-mijakovic", "acastanedam", "mzeyen1985")

    license("GPL-3.0-only")

    version("develop", branch="next")
    version("master", branch="master")

    version("1.5.1", sha256="4dac7e9152694d2ec4aefd982a52ecc064a8cb8f2c9eab0425428127c3719e2e")
    version("1.5.0", sha256="ee299ac1c08c38c9e7871d4af745f1075570ddbb708bb62d82257244585e5183")
    version("1.4.0", sha256="3b8ffb45346b2fe56aaa7ba15a515e62f9dff45a28e6a014248e20094bbe50a1")
    version("1.3.3", sha256="923a848009e7dcd9d26c317ede68b50289b2a9297eb10a75dcc34a4d49f3cdcc")
    version("1.3.2", sha256="83dbfb2e4bed28ef4e2ae430d30505874b4b50252e2f31dc422b3bc191a87ab0")
    version("1.3.1", sha256="414fa352e7b478442e6f5d0b51ff00deeb4fc705de805676c0e68829f3f30967")
    version("1.3.0", sha256="ffaa5c6abfbf79aec6389ab7caaa2c8a91bce24fd046d9741418ff815cd445d2")
    version("1.2.0", sha256="0a1411276aa0787382573df5e0f60cc38ca8079f2353fb7a7e8dc57050a7d2cb")
    version("1.1.0", sha256="626727565a8b78be0dc8883539b01aaff2bb3bd42395899643bc4d6cc2313773")
    version("1.0.2", sha256="b03b4ac9f0715279b2a5e064fd85047cb640a85c2361d732930307f8bbf2aeb8")
    version("1.0.1", sha256="b1341bb39e7e70334d7acf831fe7f2061376e7516b44d18b31797748c2a169a3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=False, description="Enable Fortran modules")
    variant("mpi", default=False, description="Enable MPI support")
    variant(
        "fabrics",
        values=disjoint_sets(("auto",), ("infiniband",), ("ethernet",)).with_non_feature_values(
            "auto", "none"
        ),
        description="List of fabrics that are enabled; "
        "'none' use GPI-2 default (infiniband), "
        "'infiniband' will use 'rdma-core' from Spack",
    )
    variant(
        "schedulers",
        values=disjoint_sets(
            ("auto",), ("loadleveler",), ("pbs",), ("slurm",)
        ).with_non_feature_values("auto", "none"),
        description="List of lauchers for which support is enabled; "
        "'auto', 'none' or 'pbs' use 'gaspi_run.ssh'",
    )

    depends_on("autoconf", type="build", when="@1.4.0:")  # autogen.sh - autoreconf
    depends_on("automake", type="build", when="@1.4.0:")  # autogen.sh - automake
    depends_on("libtool", type="build", when="@1.4.0:")
    depends_on("m4", type="build", when="@1.4.0:")

    depends_on("sed", type=("build", "run"))
    depends_on("gawk", type=("build", "run"), when="@:1.3.3")
    depends_on("gawk", type=("run"), when="@1.4.0:")
    depends_on("openssh", type="run")

    depends_on("mpi", when="+mpi")
    depends_on("rdma-core", when="fabrics=infiniband")
    depends_on("slurm", when="schedulers=slurm")

    conflicts("%gcc@10:", when="@:1.3.2", msg="gcc>10 is not supported")
    conflicts("schedulers=slurm", when="@:1.3.3", msg="Slurm is not supported")

    def set_specific_cflags(self, spec):
        if spec.satisfies("@1.4.0%gcc@10.1.0:"):
            environ["CFLAGS"] = "-fcommon"

    # GPI-2 without autotools
    @when("@:1.3.3")
    def autoreconf(self, spec, prefix):
        touch = which("touch")
        touch("configure")
        pass

    @when("@:1.3.3")
    def configure(self, spec, prefix):
        pass

    @when("@:1.3.3")
    def build(self, spec, prefix):
        self.old_install(spec, prefix)
        pass

    @when("@:1.3.3")
    def old_install(self, spec, prefix):
        spec = self.spec

        self.set_specific_cflags(spec)

        config_args = ["-p {0}".format(prefix)]
        if spec.satisfies("fabrics=ethernet"):
            config_args += ["--with-ethernet"]
        elif spec.satisfies("fabrics=infiniband"):
            config_args += ["--with-infiniband={0}".format(spec["rdma-core"].prefix)]
        if spec.satisfies("schedulers=loadleveler"):
            config_args += ["--with-ll"]
        if spec.satisfies("+fortran"):
            config_args += ["--with-fortran=true"]
        else:
            config_args += ["--with-fortran=false"]
        if spec.satisfies("+mpi"):
            config_args += ["--with-mpi={0}".format(spec["mpi"].prefix)]

        with working_dir(self.build_directory):
            install = which("./install.sh")
            install(*config_args)

    @when("@:1.3.3")
    def install(self, spec, prefix):
        pass

    # GPI-2 with autotools
    @when("@1.4.0:")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def with_or_without_infiniband(self, activated):
        opt = "infiniband"
        if not activated:
            return "--without-{0}".format(opt)
        return "--with-{0}={1}".format(opt, self.spec["rdma-core"].prefix)

    @when("@1.4.0:")
    def configure_args(self):
        spec = self.spec
        config_args = []

        self.set_specific_cflags(spec)

        config_args.extend(self.with_or_without("fortran"))
        # Mpi
        if spec.satisfies("+mpi"):
            config_args += ["--with-mpi={0}".format(spec["mpi"].prefix)]
        # Fabrics
        if "fabrics=none" not in spec:
            config_args.extend(self.with_or_without("fabrics"))
        # Schedulers
        if "schedulers=none" not in spec:
            config_args.extend(self.with_or_without("schedulers"))

        return config_args

    def set_machines(self):
        with open("{0}/tests/machines".format(self.build_directory), "w") as mfile:
            hostname = environ["HOSTNAME"]
            mfile.write("{0}\n{0}\n".format(hostname))

    # In principle it is possible to run tests for lower versions, but
    # for them NUMA is set by default, thus the number of processes is
    # limited by the number of sockets, i.e., it there is just one,
    # the machine file can not contain more than one host
    @when("@1.4.0:")
    def check(self):
        self.set_machines()
        with working_dir("{0}/tests".format(self.build_directory)):
            bash = which("bash")
            bash("./runtests.sh")
