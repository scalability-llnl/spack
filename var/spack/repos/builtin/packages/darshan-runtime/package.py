# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class DarshanRuntime(AutotoolsPackage):
    """Darshan (runtime) is a scalable HPC I/O characterization tool
    designed to capture an accurate picture of application I/O behavior,
    including properties such as patterns of access within files, with
    minimum overhead. DarshanRuntime package should be installed on
    systems where you intend to instrument MPI applications."""

    homepage = "https://www.mcs.anl.gov/research/projects/darshan/"
    url = "https://web.cels.anl.gov/projects/darshan/releases/darshan-3.4.0.tar.gz"
    git = "https://github.com/darshan-hpc/darshan.git"

    maintainers("shanedsnyder", "carns")

    tags = ["e4s"]
    test_requires_compiler = True

    version("main", branch="main", submodules=True)
    version("3.4.5", sha256="1c017ac635fab5ee0e87a6b52c5c7273962813569495cb1dd3b7cfa6e19f6ed0")
    version("3.4.4", sha256="d9c9df5aca94dc5ca3d56fd763bec2f74771d35126d61cb897373d2166ccd867")
    version("3.4.3", sha256="dca5f9f9b0ead55a8724b218071ecbb5c4f2ef6027eaade3a6477256930ccc2c")
    version("3.4.2", sha256="b095c3b7c059a8eba4beb03ec092b60708780a3cae3fc830424f6f9ada811c6b")
    version("3.4.1", sha256="77c0a4675d94a0f9df5710e5b8658cc9ef0f0981a6dafb114d0389b1af64774c")
    version("3.4.0", sha256="7cc88b7c130ec3b574f6b73c63c3c05deec67b1350245de6d39ca91d4cff0842")
    version(
        "3.4.0-pre1", sha256="57d0fd40329b9f8a51bdc9d7635b646692b341d80339115ab203357321706c09"
    )
    version("3.3.1", sha256="281d871335977d0592a49d053df93d68ce1840f6fdec27fea7a59586a84395f7")
    version("3.3.0", sha256="2e8bccf28acfa9f9394f2084ec18122c66e45d966087fa2e533928e824fcb57a")
    version(
        "3.3.0-pre2", sha256="0fc09f86f935132b7b05df981b05cdb3796a1ea02c7acd1905323691df65e761"
    )
    version(
        "3.3.0-pre1", sha256="1c655359455b5122921091bab9961491be58a5f0158f073d09fe8cc772bd0812"
    )
    version("3.2.1", sha256="d63048b7a3d1c4de939875943e3e7a2468a9034fcb68585edbc87f57f622e7f7")
    version("3.2.0", sha256="4035435bdc0fa2a678247fbf8d5a31dfeb3a133baf06577786b1fe8d00a31b7e")
    version("3.1.8", sha256="3ed51c8d5d93b4a8cbb7d53d13052140a9dffe0bc1a3e1ebfc44a36a184b5c82")
    version("3.1.7", sha256="9ba535df292727ac1e8025bdf2dc42942715205cad8319d925723fd88709e8d6")
    version("3.1.6", sha256="21cb24e2a971c45e04476e00441b7fbea63d2afa727a5cf8b7a4a9d9004dd856")
    version("3.1.0", sha256="b847047c76759054577823fbe21075cfabb478cdafad341d480274fb1cef861c")
    version("3.0.0", sha256="95232710f5631bbf665964c0650df729c48104494e887442596128d189da43e0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi", when="+mpi")
    depends_on("zlib-api")
    depends_on("hdf5", when="+hdf5")
    depends_on("parallel-netcdf", when="+parallel-netcdf")
    depends_on("lustre", when="+lustre")
    depends_on("papi", when="+apxc")
    depends_on("autoconf", type="build", when="@main")
    depends_on("automake", type="build", when="@main")
    depends_on("libtool", type="build", when="@main")
    depends_on("m4", type="build", when="@main")
    depends_on("autoconf", type="build", when="@3.4.0:")
    depends_on("automake", type="build", when="@3.4.0:")
    depends_on("libtool", type="build", when="@3.4.0:")
    depends_on("m4", type="build", when="@3.4.0:")

    variant("mpi", default=True, description="Compile with MPI support")
    variant("hdf5", default=False, description="Compile with HDF5 module", when="@3.2:")
    variant(
        "parallel-netcdf",
        default=False,
        description="Compile with Parallel NetCDF module",
        when="@3.4.1:",
    )
    variant("lustre", default=False, description="Compile with Lustre module", when="@3.1:")
    variant("apmpi", default=False, description="Compile with AutoPerf MPI module", when="@3.3:")
    variant(
        "apmpi_sync",
        default=False,
        description="Compile with AutoPerf MPI module (with collective synchronization timing)",
        when="@3.3:",
    )
    variant("apxc", default=False, description="Compile with AutoPerf XC module", when="@3.3:")
    variant(
        "scheduler",
        default="NONE",
        description="Queue system scheduler JOB ID",
        values=("NONE", "cobalt", "pbs", "sge", "slurm"),
        multi=False,
    )
    variant(
        "log_path",
        values=str,
        default="none",
        description="Path to centralized, formatted Darshan log directory",
    )
    variant("mmap_logs", default=False, description="Use mmap to store Darshan log data")
    variant("group_readable_logs", default=False, description="Write group-readable logs")

    @property
    def configure_directory(self):
        return "darshan-runtime"

    def configure_args(self):
        spec = self.spec
        extra_args = []

        job_id = "NONE"
        if spec.satisfies("scheduler=slurm"):
            job_id = "SLURM_JOBID"
        elif spec.satisfies("scheduler=cobalt"):
            job_id = "COBALT_JOBID"
        elif spec.satisfies("scheduler=pbs"):
            job_id = "PBS_JOBID"
        elif spec.satisfies("scheduler=sge"):
            job_id = "JOB_ID"

        if spec.satisfies("+hdf5"):
            if self.version < Version("3.3.2"):
                extra_args.append("--enable-hdf5-mod=%s" % spec["hdf5"].prefix)
            else:
                extra_args.append("--enable-hdf5-mod")
        if spec.satisfies("+parallel-netcdf"):
            extra_args.append("--enable-pnetcdf-mod")
        if spec.satisfies("+lustre"):
            extra_args.append("--enable-lustre-mod")
        else:
            extra_args.append("--disable-lustre-mod")
        if spec.satisfies("+apmpi"):
            extra_args.append("--enable-apmpi-mod")
        if spec.satisfies("+apmpi_sync"):
            extra_args.extend(["--enable-apmpi-mod", "--enable-apmpi-coll-sync"])
        if spec.satisfies("+apxc"):
            extra_args.append("--enable-apxc-mod")
        if spec.satisfies("+group_readable_logs"):
            extra_args.append("--enable-group-readable-logs")
        if spec.satisfies("+mmap_logs"):
            extra_args.append("--enable-mmap-logs")
        log_path = self.spec.variants["log_path"].value
        if log_path != "none":
            extra_args.append("--with-log-path=" + log_path)
        else:
            extra_args.append("--with-log-path-by-env=DARSHAN_LOG_DIR_PATH")

        extra_args.append("--with-mem-align=8")
        extra_args.append("--with-jobid-env=%s" % job_id)
        extra_args.append("--with-zlib=%s" % spec["zlib-api"].prefix)

        if "+mpi" not in spec:
            extra_args.append("--without-mpi")

        return extra_args

    def setup_run_environment(self, env):
        if self.spec.variants["log_path"].value == "none":
            # set a default path for log file that can be overrode by user
            darshan_log_dir = os.environ["HOME"]
            env.set("DARSHAN_LOG_DIR_PATH", darshan_log_dir)

    @property
    def basepath(self):
        return join_path("darshan-test", join_path("regression", join_path("test-cases", "src")))

    @run_after("install")
    def _copy_test_inputs(self):
        test_inputs = [join_path(self.basepath, "mpi-io-test.c")]
        cache_extra_test_sources(self, test_inputs)

    def test_mpi_io_test(self):
        """build, run, and check outputs"""
        if "+mpi" not in self.spec:
            raise SkipTest("Test requires +mpi build")

        testdir = "intercept-test"
        logname = join_path(os.getcwd(), testdir, "test.darshan")
        testexe = "mpi-io-test"

        with working_dir(testdir, create=True):
            env["LD_PRELOAD"] = join_path(self.prefix.lib, "libdarshan.so")
            env["DARSHAN_LOGFILE"] = logname

            # compile the program
            fname = join_path(
                self.test_suite.current_test_cache_dir, self.basepath, f"{testexe}.c"
            )
            cc = Executable(self.spec["mpi"].mpicc)
            compile_opt = ["-c", fname]
            link_opt = ["-o", "mpi-io-test", "mpi-io-test.o"]
            cc(*(compile_opt))
            cc(*(link_opt))

            # run test program and intercept
            mpi_io_test = which(join_path(".", testexe))
            out = mpi_io_test("-f", "tmp.dat", output=str.split, error=str.split)
            env.pop("LD_PRELOAD")

            expected_output = [
                r"Write bandwidth = \d+.\d+ Mbytes/sec",
                r"Read bandwidth = \d+.\d+ Mbytes/sec",
            ]
            check_outputs(expected_output, out)

            assert os.path.exists(logname), f"Expected {logname} to exist"
            assert (os.stat(logname)).st_size > 0, f"Expected non-empty {logname}"
