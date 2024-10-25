# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetSsleay(PerlPackage):
    """Perl extension for using OpenSSL"""

    homepage = "https://metacpan.org/pod/Net::SSLeay"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHRISN/Net-SSLeay-1.94.tar.gz"

    license("Artistic-2.0")

    version("1.94", sha256="9d7be8a56d1bedda05c425306cc504ba134307e0c09bda4a788c98744ebcd95d")
    version("1.85", sha256="9d8188b9fb1cae3bd791979c20554925d5e94a138d00414f1a6814549927b0c8")
    version("1.82", sha256="5895c519c9986a5e5af88e3b8884bbdc70e709ee829dc6abb9f53155c347c7e5")

    depends_on("c", type="build")  # generated

    depends_on("openssl")

    def configure(self, spec, prefix):
        self.build_method = "Makefile.PL"
        self.build_executable = make
        # Do you want to run external tests?
        config_answers = ["\n"]
        config_answers_filename = "spack-config.in"

        with open(config_answers_filename, "w") as f:
            f.writelines(config_answers)

        with open(config_answers_filename, "r") as f:
            env["OPENSSL_PREFIX"] = self.spec["openssl"].prefix
            perl("Makefile.PL", "INSTALL_BASE={0}".format(prefix), input=f)

    def url_for_version(self, version):
        if self.spec.satisfies("@1.86:"):
            return f"https://cpan.metacpan.org/authors/id/C/CH/CHRISN/Net-SSLeay-{version}.tar.gz"
        else:
            return f"http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-{version}.tar.gz"
