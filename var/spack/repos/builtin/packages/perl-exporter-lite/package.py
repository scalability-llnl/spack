# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExporterLite(PerlPackage):
    """Exporter::Lite is an alternative to Exporter, intended to provide a
    lightweight subset of the most commonly-used functionality. It supports
    import(), @EXPORT and @EXPORT_OK and not a whole lot else."""

    homepage = "https://metacpan.org/pod/Exporter::Lite"
    url = "https://cpan.metacpan.org/authors/id/N/NE/NEILB/Exporter-Lite-0.08.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.09", sha256="79d8b14fd5013922c63e850f15bf51059f2502404535eb6690ef23612c2a198d")
    version("0.08", sha256="c05b3909af4cb86f36495e94a599d23ebab42be7a18efd0d141fc1586309dac2")
