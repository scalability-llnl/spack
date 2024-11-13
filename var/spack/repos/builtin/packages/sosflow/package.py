# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sosflow(CMakePackage):
    """SOSflow provides a flexible, scalable, and programmable framework for
    observation, introspection, feedback, and control of HPC applications."""

    homepage = "https://github.com/cdwdirect/sos_flow/wiki"
    git = "https://github.com/cdwdirect/sos_flow.git"

    version("spack", tag="spack-build-v0.9901", commit="57c77f18af88b01615d5900124f9cfd1770c8241")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libevpath")
    depends_on("sqlite@3:")
    depends_on("pkgconfig")
    depends_on("mpi")

    def setup_build_environment(self, env):
        env.set("SOS_HOST_KNOWN_AS", "SPACK-SOS-BUILD")
        env.set("SOS_HOST_NODE_NAME", "SPACK-SOS-NODE")
        env.set("SOS_HOST_DETAILED", "SPACK-SOS-DETAILED")

    def setup_run_environment(self, env):
        env.set("SOS_ROOT", self.spec.prefix)
        env.set("SOS_BUILD_DIR", self.spec.prefix)
        env.set("SOS_CMD_PORT", "22500")
        env.set("SOS_WORK", env["HOME"])
        env.set("SOS_EVPATH_MEETUP", env["HOME"])
        env.set("SOS_ENV_SET", "true")
