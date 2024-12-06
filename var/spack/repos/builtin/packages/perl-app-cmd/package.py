# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAppCmd(PerlPackage):
    """Write command line apps with less suffering"""

    homepage = "https://metacpan.org/pod/App::Cmd"
    url = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/App-Cmd-0.331.tar.gz"

    license("Artistic-1.0")

    version("0.335", sha256="f95517fc4df348d9e7ea01467aabd9725f0715662ee483b54b81d3f0b38c9874")
    version("0.331", sha256="4a5d3df0006bd278880d01f4957aaa652a8f91fe8f66e93adf70fba0c3ecb680")
