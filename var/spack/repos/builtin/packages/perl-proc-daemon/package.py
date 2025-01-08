# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlProcDaemon(PerlPackage):
    """Run Perl program(s) as a daemon process"""

    homepage = "https://metacpan.org/pod/Proc::Daemon"
    url = "https://cpan.metacpan.org/authors/id/A/AK/AKREAL/Proc-Daemon-0.23.tar.gz"

    maintainers("EbiArnie")

    version("0.23", sha256="34c0b85b7948b431cbabc97cee580835e515ccf43badbd8339eb109474089b69")

    depends_on("perl-proc-processtable", type=("build", "link"))
