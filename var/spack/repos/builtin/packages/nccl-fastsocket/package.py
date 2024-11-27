# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class NcclFastsocket(Package):
    """NCCL Fast Socket GCP Net plugin for NCCL"""

    homepage = "https://github.com/google/nccl-fastsocket"
    git = "https://github.com/google/nccl-fastsocket.git"

    version("master", preferred=True)

    depends_on("cxx", type="build")  # generated

    depends_on("bazel", type="build")
    depends_on("nccl", type=["build", "run"])

    maintainers("danielahlin")

    def setup_build_environment(self, env):
        spec = self.spec
        tmp_path = tempfile.mkdtemp(prefix="spack")
        env.set("TEST_TMPDIR", tmp_path)
        env.set("NCCL_INSTALL_PATH", spec["nccl"].prefix)
        env.set("NCCL_HDR_PATH", spec["nccl"].prefix.include)

    def install(self, spec, prefix):
        tmp_path = env["TEST_TMPDIR"]
        # Copied of py-tensorflow
        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + tmp_path,
            "build",
            "libnccl-net.so",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            # Enable verbose output for failures
            "--verbose_failures",
            # Show (formatted) subcommands being executed
            "--subcommands=pretty_print",
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            "--explain=explainlogfile.txt",
            # Increase verbosity of explanation,
            "--verbose_explanations",
        ]
        bazel(*args)
        install_tree("bazel-bin", prefix.lib)

    def setup_run_environment(self, env):
        # The current plugin pickup method of NCCL is to scan for libraries with certain
        # names in the standard library search paths. Consequently, to make nccl-fastsocket
        # discoverable to NCCL it is necessary to add it to the LD_LIBRARY_PATH.
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        # NCCL_NET_PLUGIN can be used to change part of the library-name NCCL is looking
        # for. This is not necessary for this plugin so it is set to the empty string.
        env.set("NCCL_NET_PLUGIN", "")
