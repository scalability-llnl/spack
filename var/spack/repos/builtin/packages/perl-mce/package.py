# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMce(PerlPackage):
    """MCE - Many-Core Engine for Perl providing parallel processing
    capabilities.

    MCE spawns a pool of workers and therefore does not fork a new process per
    each element of data. Instead, MCE follows a bank queuing model. Imagine
    the line being the data and bank-tellers the parallel workers. MCE enhances
    that model by adding the ability to chunk the next n elements from the
    input stream to the next available worker."""

    homepage = "https://github.com/marioroy/mce-perl"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MARIOROY/MCE-1.874.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.889", sha256="db6153e474d046fc253050bf53c54002d84cd4ca77d21c2b9df56feeb809bbed")
    version("1.884", sha256="c830c0e548094f19c620049e744258be2c121d4a86cf7c94a37599ad016daf33")
    version("1.874", sha256="d809e3018475115ad7eccb8bef49bde3bf3e75abbbcd80564728bbcfab86d3d0")
