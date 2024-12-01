# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlBioEnsemblFuncgen(Package):
    """Ensembl Funcgen Perl API and SQL schema."""

    homepage = "http://ensembl.org/info/docs/api/funcgen/index.html"
    url = "https://github.com/Ensembl/ensembl-funcgen/archive/release/111.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("112", sha256="d7398921779a6865b5e2f0269d51d268f9b8cd96e4ca3577c88e6f34593e683d")
    version("111", sha256="67b1b7d6efde9e8be7b4ef73c54c0b5e7e3eadcd590a94bc980984514ef746d0")
    version("110", sha256="c9e85a423a8c8653741aed799aea9762fa1dfb301f50dc11d291925e81d7aeee")

    extends("perl")

    depends_on("perl-role-tiny", type=("build", "run"))
    depends_on("perl-bio-ensembl")

    variant("sql", default=False, description="Install SQL files")
    variant("scripts", default=False, description="Install scripts")
    variant("templates", default=False, description="Install templates")

    def install(self, spec, prefix):
        install_tree("modules", prefix.lib.perl5)
        mkdirp(prefix.share.ensembl.variation)
        for extra in ["sql", "scripts", "templates"]:
            if spec.satisfies(f"+{extra}"):
                target = join_path(prefix.share.ensembl, extra)
                install_tree(extra, target)
