# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMozillaCa(PerlPackage):
    """Mozilla's CA cert bundle in PEM format"""

    homepage = "https://metacpan.org/pod/Mozilla::CA"
    url = "http://search.cpan.org/CPAN/authors/id/A/AB/ABH/Mozilla-CA-20160104.tar.gz"

    license("MPL-2.0")

    version("20160104", sha256="27a7069a243162b65ada4194ff9d21b6ebc304af723eb5d3972fb74c11b03f2a")
