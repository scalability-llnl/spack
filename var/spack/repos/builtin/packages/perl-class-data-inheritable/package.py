# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassDataInheritable(PerlPackage):
    """For creating accessor/mutators to class data."""

    homepage = "http://search.cpan.org/~tmtm/Class-Data-Inheritable-0.08/lib/Class/Data/Inheritable.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz"

    version('0.08', sha256='9967feceea15227e442ec818723163eb6d73b8947e31f16ab806f6e2391af14a')
