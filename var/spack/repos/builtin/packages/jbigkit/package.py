# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jbigkit(MakefilePackage):
    """JBIG-Kit is a software implementation of
    the JBIG1 data compression standard."""

    homepage = "https://www.cl.cam.ac.uk/~mgk25/jbigkit/"
    url = "https://www.cl.cam.ac.uk/~mgk25/jbigkit/download/jbigkit-2.1.tar.gz"

    version("2.1", sha256="de7106b6bfaf495d6865c7dd7ac6ca1381bd12e0d81405ea81e7f2167263d932")
    version("1.6", sha256="d841b6d0723c1082450967f3ea500be01810a34ec4a97ad10985ae7071a6150b")

    depends_on("c", type="build")  # generated

    build_directory = "libjbig"

    def edit(self, spec, prefix):
        makefile = FileFilter("libjbig/Makefile")
        makefile.filter("CC = .*", "CC = cc")

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.include)
            for f in ["jbig85.h", "jbig_ar.h", "jbig.h"]:
                install(f, prefix.include)
            mkdir(prefix.lib)
            for f in ["libjbig85.a", "libjbig.a"]:
                install(f, prefix.lib)
            mkdir(prefix.bin)
            for f in ["tstcodec", "tstcodec85"]:
                install(f, prefix.bin)

    @property
    def libs(self):
        return find_libraries("libjbig*", root=self.prefix, shared=False, recursive=True)
