# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bedops(MakefilePackage):
    """BEDOPS is an open-source command-line toolkit that performs highly
    efficient and scalable Boolean and other set operations, statistical
    calculations, archiving, conversion and other management of genomic data of
    arbitrary scale."""

    homepage = "https://bedops.readthedocs.io"
    url = "https://github.com/bedops/bedops/archive/v2.4.39.tar.gz"

    maintainers("jacorvar")

    license("bzip2-1.0.6")

    version("2.4.41", sha256="3b868c820d59dd38372417efc31e9be3fbdca8cf0a6b39f13fb2b822607d6194")
    version("2.4.40", sha256="8c01db76669dc58c595e2e1b9bdb6d462f3363fc569b15c460a63a63b8b6bf30")
    version("2.4.39", sha256="f8bae10c6e1ccfb873be13446c67fc3a54658515fb5071663883f788fc0e4912")
    version("2.4.35", sha256="da0265cf55ef5094834318f1ea4763d7a3ce52a6900e74f532dd7d3088c191fa")
    version("2.4.34", sha256="533a62a403130c048d3378e6a975b73ea88d156d4869556a6b6f58d90c52ed95")
    version("2.4.30", sha256="218e0e367aa79747b2f90341d640776eea17befc0fdc35b0cec3c6184098d462")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    @property
    def build_targets(self):
        # avoid static linking with glibc for all invocations
        return ["SFLAGS="]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("install", "BINDIR=%s" % prefix.bin)
