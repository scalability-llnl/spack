# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Amrfinder(MakefilePackage):
    """NCBI AMRFinderPlus: This software and the accompanying database identify
    acquired antimicrobial resistance genes in bacterial protein and/or
    assembled nucleotide sequences as well as known resistance-associated
    point mutations for several taxa. With AMRFinderPlus we added select
    members of additional classes of genes such as virulence factors,
    biocide, heat, acid, and metal resistance genes."""

    homepage = "https://github.com/ncbi/amr/wiki"
    url = "https://github.com/ncbi/amr/archive/refs/tags/amrfinder_v3.10.30.tar.gz"

    version("3.12.8", sha256="a199bc332877bad9033a7620bc5e8e849db1f19a9ba8b7357ec5451a6a283aa0")
    version("3.11.8", sha256="8aac87595f28d0ba54ed3e97a1c033f9769a9b03e0aba78bc29cf6aff0cf45d1")
    version("3.10.42", sha256="97254f8d6217a4618b7f29c05acbcfe0240ee5e98458f8da7df3840b4be39c1b")
    version("3.10.30", sha256="2f1e30b86935a27cee740bd7229a41fbce278f2f60b33b8e51592bab8bdf23f1")
    version("3.10.24", sha256="fce299c980cda740dcc4f53f9b2dc9061c856213e5bdbc2c339185a5fb7dcf6a")

    depends_on("cxx", type="build")  # generated

    depends_on("blast-plus")
    depends_on("hmmer")
    depends_on("curl")

    def setup_build_environment(self, env):
        env.set("INSTALL_DIR", prefix.bin)
        env.set("DEFAULT_DB_DIR", prefix.share)

    @run_before("build")
    def create_bin_and_share(self):
        mkdirp(self.spec.prefix.bin)
        mkdirp(self.spec.prefix.share)
