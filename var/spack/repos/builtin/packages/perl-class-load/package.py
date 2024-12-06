# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassLoad(PerlPackage):
    """A working (require "Class::Name") and more"""

    homepage = "https://metacpan.org/pod/Class::Load"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-0.24.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.25", sha256="2a48fa779b5297e56156380e8b32637c6c58decb4f4a7f3c7350523e11275f8f")
    version("0.24", sha256="0bb983da46c146534fc77a556d6e40d925142f2eb43103534025ee545265ca36")
