# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHtmlTagset(PerlPackage):
    """Data tables useful in parsing HTML"""

    homepage = "https://metacpan.org/pod/HTML::Tagset"
    url = "http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/HTML-Tagset-3.20.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.24", sha256="eb89e145a608ed1f8f141a57472ee5f69e67592a432dcd2e8b1dbb445f2b230b")
    version("3.20", sha256="adb17dac9e36cd011f5243881c9739417fd102fce760f8de4e9be4c7131108e2")
