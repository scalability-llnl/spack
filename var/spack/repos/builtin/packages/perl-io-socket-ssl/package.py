# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoSocketSsl(PerlPackage):
    """SSL sockets with IO::Socket interface"""

    homepage = "https://metacpan.org/dist/IO-Socket-SSL/view/lib/IO/Socket/SSL.pod"
    url = "http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-2.052.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.089", sha256="f683112c1642967e9149f51ad553eccd017833b2f22eb23a9055609d2e3a14d1")
    version("2.085", sha256="95b2f7c0628a7e246a159665fbf0620d0d7835e3a940f22d3fdd47c3aa799c2e")
    version("2.052", sha256="e4897a9b17cb18a3c44aa683980d52cef534cdfcb8063d6877c879bfa2f26673")

    depends_on("perl-net-ssleay", type=("build", "run"))

    def configure(self, spec, prefix):
        self.build_method = "Makefile.PL"
        self.build_executable = make
        # Should I do external tests?
        config_answers = ["n\n"]
        config_answers_filename = "spack-config.in"

        with open(config_answers_filename, "w") as f:
            f.writelines(config_answers)

        with open(config_answers_filename, "r") as f:
            perl("Makefile.PL", f"INSTALL_BASE={prefix}", input=f)
