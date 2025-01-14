# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xalt(AutotoolsPackage):
    """XALT 2 is a tool to allow a site to track user executables and library usage on a cluster.
    When installed it can tell a site what are the top executables by Node-Hours or by the number
    of users or the number of times it is run. XALT 2 also tracks library usage as well. XALT 2 can
    also track package use by R, MATLAB or Python. It tracks both MPI and non-MPI programs."""

    homepage = "https://xalt.readthedocs.io/en/latest/"
    git = "https://github.com/xalt/xalt.git"

    version("2.10.45", tag="xalt-2.10.45")

    depends_on("py-mysqlclient", when="+MySQL")

    # Multiple values variants
    variant(
        "config",
        default="Config/rtm_config.py",
        description="A python file defining the accept, ignore, hostname pattern lists",
    )
    variant(
        "etcDir",
        default=".",
        description="Directory where xalt_db.conf and reverseMapD can be found",
    )
    variant(
        "mode",
        default="700",
        values=("755", "750", "700"),
        description="Override executable install mode (755 or 750 or 700)",
    )
    variant(
        "primeNumber",
        default="997",
        description="The prime number of directories when using XALT_FILE_PREFIX",
    )
    variant(
        "syshostConfig",
        default="mapping:mapping.example.json",
        description="How to determine syshost",
    )
    variant(
        "tmpdir", default="/dev/shm", description="The tmp directory to use with package records"
    )
    variant(
        "trackGPU",
        default="no",
        values=("yes", "no", "dcgm", "nvml"),
        description="Track GPU executables",
    )
    variant(
        "transmission",
        default="file",
        values=("file", "syslog", "file_separate_dirs", "curl"),
        description="Transmission style",
    )
    variant(
        "xaltFilePrefix", default="$HOME", description="Prefix where the json files are written"
    )

    # Boolean variants
    variant("32bit", default=True, description="Allow for 32 bits executables")
    variant(
        "cmdlineRecord", default=True, description="Record the program's execution command line"
    )
    variant("computeSHA1", default=False, description="Compute SHA1 sums on libraries")
    variant("functionTracking", default=True, description="Track functions from modules")
    variant(
        "hostnameParser",
        default=False,
        description="Replace built-in lex based hostname parser c_file:file.c or library:file_64.a or library:file_64.a:file_32.a",
    )
    variant("MySQL", default=True, description="Require the mysqlclient/MySQL-python module")
    variant("preloadOnly", default=True, description="Only use XALT in preload only mode")
    variant(
        "signalHandler",
        default=False,
        description="Have XALT capture executions that fail with a signal",
    )
    variant("siteControlledPrefix", default=False, description="A site controlled prefix")
    variant("supportCURL", default=True, description="Support CURL transmission style")
    variant(
        "staticLibs", default=False, description="Link with static libraries (currently only dcgm)"
    )
    variant("trackMPI", default=True, description="Track MPI executables")
    variant("trackScalarPrgms", default=True, description="Track non-mpi executables")

    def configure_args(self):
        args = []

        args.append("--exec-prefix={0}".format(self.prefix))

        for multi_variant in (
            "config",
            "etcDir",
            "mode",
            "primeNumber",
            "syshostConfig",
            "tmpdir",
            "trackGPU",
            "transmission",
            "xaltFilePrefix",
        ):
            args.append(
                "--with-" + multi_variant + "={0}".format(self.spec.variants[multi_variant].value)
            )

        for boolean_variant in (
            "32bit",
            "cmdlineRecord",
            "computeSHA1",
            "functionTracking",
            "hostnameParser",
            "MySQL",
            "preloadOnly",
            "signalHandler",
            "siteControlledPrefix",
            "supportCURL",
            "staticLibs",
            "trackMPI",
            "trackScalarPrgms",
        ):
            args += self.with_or_without(boolean_variant)

        return args
