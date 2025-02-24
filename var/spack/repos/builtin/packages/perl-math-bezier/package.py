# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathBezier(PerlPackage):
    """Math::Bezier - solution of Bezier Curves"""

    homepage = "https://metacpan.org/pod/Math::Bezier"
    url = "https://cpan.metacpan.org/authors/id/A/AB/ABW/Math-Bezier-0.01.tar.gz"

    version("0.01", sha256="11a815fc45fdf0efabb1822ab77faad8b9eea162572c5f0940c8ed7d56e6b8b8")
