# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rename(Package):
    """Perl-powered file rename script with many helpful built-ins."""

    homepage = "http://plasmasturm.org/code/rename"
    url = "https://github.com/ap/rename/archive/v1.600.tar.gz"

    version("1.600", sha256="538fa908c9c2c4e7a08899edb6ddb47f7cbeb9b1a1d04e003d3c19b56fcc7f88")

    depends_on("perl", type=("build", "run"))

    def install(self, spec, prefix):
        Executable("pod2man")("rename", "rename.1")
        bdir = join_path(prefix, "bin")
        mkdirp(bdir)
        install("rename", bdir)
        mdir = join_path(prefix, "share", "man", "man1")
        mkdirp(mdir)
        install("rename.1", mdir)
