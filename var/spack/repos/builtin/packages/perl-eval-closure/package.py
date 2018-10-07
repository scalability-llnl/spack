# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlEvalClosure(PerlPackage):
    """Safely and cleanly create closures via string eval"""

    homepage = "http://search.cpan.org/~doy/Eval-Closure-0.14/lib/Eval/Closure.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Eval-Closure-0.14.tar.gz"

    version('0.14', 'ceeb1fc579ac9af981fa6b600538c285')
