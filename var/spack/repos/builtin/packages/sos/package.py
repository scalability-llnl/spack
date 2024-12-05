# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sos(AutotoolsPackage):
    """Sandia OpenSHMEM."""

    homepage = "https://github.com/Sandia-OpenSHMEM/SOS"
    url = "https://github.com/Sandia-OpenSHMEM/SOS/archive/refs/tags/v1.5.0.zip"

    # notify when the package is updated.
    maintainers("rscohn2")

    license("BSD-3-Clause")

    version("1.5.2", sha256="c9df8c6ab43890e5d8970467c188ae2fad736845875ca4c370ff047dbb37d017")
    version("1.5.1", sha256="0a6303dcbdd713ef2d83c617c1eb821227603c98cb9816c53585fd993da8a984")
    version("1.5.0", sha256="02679da6085cca2919f900022c46bad48479690586cb4e7f971ec3a735bab4d4")
    version("1.4.5", sha256="42778ba3cedb632ac3fbbf8917f415a804f8ca3b67fb3da6d636e6c50c501906")

    variant("xpmem", default=False, description="Enable xpmem for transport")
    variant("ofi", default=True, description="Enable ofi for transport")
    variant(
        "manual-progress",
        default=False,
        description="Enable intermittent progress calls in transport layer",
    )
    variant(
        "ofi-manual-progress",
        default=False,
        when="+ofi",
        description="Use FI_MANUAL_PROGRESS for data progress control mode",
    )
    variant("shr-atomics", default=False, description="Enable shared memory atomic operations")
    variant(
        "av-map",
        default=False,
        description="Enable av-map instead of av-table in the OFI transport",
    )
    variant(
        "completion-polling",
        default=False,
        description="Enable polling in quiet, fence, and local completion operations",
    )
    variant(
        "thread-completion",
        default=False,
        description="Support SHMEM_THREAD_MULTIPLE in OFI transport using FI_THREAD_COMPLETION",
    )
    variant("error-checking", default=False, description="Enable error checking for SHMEM calls")
    variant(
        "lengthy-tests",
        default=False,
        description="Execute long running tests as part of 'make check'",
    )
    variant("rpath", default=True, description="Use rpath in compiler wrappers ")
    variant("hard-polling", default=False, description="Enable hard polling of wait calls")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("hydra", type=("build", "run"), when="+ofi")

    depends_on("libfabric", type="link", when="+ofi")
    depends_on("xpmem", type="link", when="+xpmem")

    # Enable use of the OSH wrappers outside of Spack by preventing
    # them from using the spack wrappers
    filter_compiler_wrappers("oshcc", "oshc++", "oshcc", "oshfort", relative_root="bin")

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Enable the osh wrappers to use spack wrappers when inside spack
        # with env variables
        env.set("SHMEM_CC", spack_cc)
        env.set("SHMEM_CXX", spack_cxx)
        env.set("SHMEM_FC", spack_fc)

    def autoreconf(self, spec, prefix):
        bash = Executable("bash")
        bash("./autogen.sh")

    def configure_args(self):
        args = []
        args.extend(self.with_or_without("xpmem"))
        args.extend(self.with_or_without("ofi"))
        # This option is not compatiable with remote atomics
        args.extend(self.enable_or_disable("shr-atomics"))
        args.extend(self.enable_or_disable("av-map"))
        args.extend(self.enable_or_disable("completion-polling"))
        args.extend(self.enable_or_disable("thread-completion"))
        args.extend(self.enable_or_disable("error-checking"))
        args.extend(self.enable_or_disable("lengthy-tests"))
        args.extend(self.enable_or_disable("rpath"))
        args.extend(self.enable_or_disable("manual-progress"))
        args.extend(self.enable_or_disable("ofi-manual-progress"))
        args.extend(self.enable_or_disable("hard-polling"))
        args.append("--enable-pmi-simple")
        return args
