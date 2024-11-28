# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystDevel(PerlPackage):
    """Catalyst Development Tools"""

    homepage = "https://metacpan.org/pod/Catalyst::Devel"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Catalyst-Devel-1.42.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.42", sha256="7ec6f0b6cab5b8c097e47769fc73a4d4c015a58c41fdb40fc24df3ee77c48abd")

    depends_on("perl-catalyst-action-renderview@0.10:", type=("build", "run", "test"))
    depends_on("perl-catalyst-plugin-configloader@0.30:", type=("build", "run", "test"))
    depends_on("perl-catalyst-plugin-static-simple@0.28:", type=("build", "run", "test"))
    depends_on("perl-catalyst-runtime", type=("build", "run", "test"))
    depends_on("perl-config-general@2.42:", type=("build", "run", "test"))
    depends_on("perl-file-changenotify@0.07:", type=("build", "run", "test"))
    depends_on("perl-file-copy-recursive", type=("build", "run", "test"))
    depends_on("perl-file-sharedir", type=("build", "run", "test"))
    depends_on("perl-file-sharedir-install", type=("build"))
    depends_on("perl-module-install@1.02:", type=("build", "run", "test"))
    depends_on("perl-moose", type=("build", "run", "test"))
    depends_on("perl-moosex-emulate-class-accessor-fast", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-namespace-clean", type=("build", "run", "test"))
    depends_on("perl-path-class@0.09:", type=("build", "run", "test"))
    depends_on("perl-template-toolkit", type=("build", "run", "test"))
    depends_on("perl-test-fatal@0.003:", type=("build", "test"))
    depends_on("perl-yaml-tiny", type=("build", "test"))
