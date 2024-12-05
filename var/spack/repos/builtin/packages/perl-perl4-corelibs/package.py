# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerl4Corelibs(PerlPackage):
    """Perl4::CoreLibs - libraries historically supplied with Perl 4"""

    # doesn't look like a homepage but it is
    homepage = "https://metacpan.org/pod/release/ZEFRAM/Perl4-CoreLibs-0.003/lib/Perl4/CoreLibs.pm"
    url = "https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/Perl4-CoreLibs-0.003.tar.gz"

    version("0.005", sha256="0250aafd307e5d25670946a662bdd0a2a8cc6ed9d949a848753f0b26910923a8")
    version("0.004", sha256="78887e3365f8935ab00d528832e9b7a426fb684ffc5c03c20e67a217ca4ac64a")
    version("0.003", sha256="55c9b2b032944406dbaa2fd97aa3692a1ebce558effc457b4e800dabfaad9ade")
    version("0.002", sha256="c68272e8b0e37268d9fbb93f5ef5708e12e0a13bbb5a6123af3f493ea8852521")
    version("0.001", sha256="f7479f63e8b0cc344752a59f66fd084a14ee87bcc2a1f67c1a413afab8d0ad37")
    version("0.000", sha256="d8f2310ad0b0f48c8fc258a75042ebeedf47bcefb231be427761dba77e734875")

    depends_on("perl-module-build", type="build")
