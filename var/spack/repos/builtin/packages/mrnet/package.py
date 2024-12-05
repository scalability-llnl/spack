# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Mrnet(AutotoolsPackage):
    """The MRNet Multi-Cast Reduction Network."""

    homepage = "https://paradyn.org/mrnet"
    url = "https://ftp.cs.wisc.edu/pub/paradyn/mrnet/mrnet_5.0.1.tar.gz"
    git = "https://github.com/dyninst/mrnet.git"
    list_url = "http://ftp.cs.wisc.edu/paradyn/mrnet"

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("5.0.1-4", commit="2c5632aa27188de6866abc49bf1de70fb6b27af9")
    version("5.0.1-3", commit="7375ba5bb0df87c68e58ad15e9e5e351ae020c08")
    version("5.0.1-2", commit="20b1eacfc6d680d9f6472146d2dfaa0f900cc2e9")
    version("5.0.1", sha256="df0bab4c4c462d0c32df4fd97bf2546f32439f31ca96b54ebbbadd33dd6bc107")
    version("4.1.0", sha256="94758191ac46a9dbfea931a8e61167fe7e8a5f880caa418305c44f1d12af5e45")
    version("4.0.0", sha256="7207c6d493b3f17c386667cfefa81364c96b9c8b831c67442d218d77813c5d38")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("lwthreads", default=False, description="Also build the MRNet LW threadsafe libraries")
    parallel = False

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-shared"]

        # Build the MRNet LW thread safe libraries when the
        # lwthreads variant is present
        if "+lwthreads" in spec:
            config_args.append("--enable-ltwt-threadsafe")

        return config_args
