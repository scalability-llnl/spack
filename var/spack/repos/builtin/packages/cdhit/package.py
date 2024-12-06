# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob

from spack.package import *


class Cdhit(MakefilePackage):
    """CD-HIT is a very widely used program for clustering and comparing
    protein or nucleotide sequences."""

    homepage = "http://cd-hit.org/"
    url = "https://github.com/weizhongli/cdhit/archive/V4.6.8.tar.gz"

    license("GPL-2.0-only")

    version("4.8.1", sha256="f8bc3cdd7aebb432fcd35eed0093e7a6413f1e36bbd2a837ebc06e57cdb20b70")
    version("4.6.8", sha256="37d685e4aa849314401805fe4d4db707e1d06070368475e313d6f3cb8fb65949")

    depends_on("cxx", type="build")  # generated

    maintainers("snehring")

    variant("openmp", default=True, description="Compile with multi-threading support")
    variant("zlib", default=True, description="Compile with zlib")

    depends_on("perl", type=("build", "run"))
    depends_on("perl-text-nsp", type="run")
    depends_on("zlib-api", when="+zlib", type="link")

    def patch(self):
        for f in glob("*.pl"):
            filter_file("^#!/usr/bin/perl.*$", "#!/usr/bin/env perl", f)

    def build(self, spec, prefix):
        mkdirp(prefix.bin)
        make_args = []
        if spec.satisfies("~openmp"):
            make_args.append("openmp=no")
        if spec.satisfies("~zlib"):
            make_args.append("zlib=no")
        make(*make_args)

    def setup_build_environment(self, env):
        env.set("PREFIX", self.prefix.bin)
