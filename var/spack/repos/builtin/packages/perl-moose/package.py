# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoose(PerlPackage):
    """A postmodern object system for Perl 5"""

    homepage = "https://metacpan.org/pod/Moose"
    url = "https://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Moose-2.2006.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.2207", sha256="7c2daddc49754ded93f65b8ce9e3ac9b6d11ab27d111ec77f95a8528cf4ac409")
    version("2.2203", sha256="fa7814acf4073fa434c148d403cbbf8a7b62f73ad396fa8869f3036d6e3241a7")
    version("2.2010", sha256="af0905b69f18c27de1177c9bc7778ee495d4ec91be1f223e8ca8333af4de08c5")
    version("2.2009", sha256="63ba8a5e27dbcbdbac2cd8f4162fff50a31e9829d8955a196a5898240c02d194")
    version("2.2007", sha256="bc75a320b55ba26ac9e60e11a77b3471066cb615bf7097537ed22e20df88afe8")
    version("2.2006", sha256="a4e00ab25cc41bebc5e7a11d71375fb5e64b56d5f91159afee225d698e06392b")

    depends_on("c", type="build")  # generated

    depends_on("perl-cpan-meta-check", type=("build", "run"))
    depends_on("perl-test-cleannamespaces", type=("build", "run"))
    depends_on("perl-devel-overloadinfo", type=("build", "run"))
    depends_on("perl-class-load-xs", type=("build", "run"))
    depends_on("perl-devel-stacktrace", type=("build", "run"))
    depends_on("perl-eval-closure", type=("build", "run"))
    depends_on("perl-sub-name", type=("build", "run"))
    depends_on("perl-module-runtime-conflicts", type=("build", "run"))
    depends_on("perl-devel-globaldestruction", type=("build", "run"))
    depends_on("perl-package-deprecationmanager", type=("build", "run"))
    depends_on("perl-package-stash-xs", type=("build", "run"))
