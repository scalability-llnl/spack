# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiomart(RPackage):
    """Interface to BioMart databases (i.e. Ensembl).

    In recent years a wealth of biological data has become available in
    public data repositories. Easy access to these valuable data resources
    and firm integration with data analysis is needed for comprehensive
    bioinformatics data analysis. biomaRt provides an interface to a growing
    collection of databases implementing the BioMart software suite
    (<http://www.biomart.org>). The package enables retrieval of large
    amounts of data in a uniform way without the need to know the underlying
    database schemas or write complex SQL queries. The most prominent
    examples of BioMart databases are maintain by Ensembl, which provides
    biomaRt users direct access to a diverse set of data and enables a wide
    range of powerful online queries from gene annotation to database
    mining."""

    bioc = "biomaRt"

    version("2.56.0", commit="91ca89eff52e63c225f7e4eb24b765d08faf3ed9")
    version("2.54.0", commit="4fb88fb56c684d5678f8288ba05db193e4881758")
    version("2.52.0", commit="cf4932ac02686da45ea36ff5137fa63cead8860b")
    version("2.50.3", commit="83a519ac13d73dc545cb6aafde5f4b5001e9e08f")
    version("2.46.2", commit="90d6abfdfa04259006f7b47efb10271ada76aec1")
    version("2.40.5", commit="ed9ddafb0d620168ea8e3ab4884f3457b8525c68")
    version("2.38.0", commit="16b997aba19a90a1c5fa64c442b1e7fcff99a658")
    version("2.36.1", commit="5634e57e20199f9dc1f8b927eb3893143fc02f4f")
    version("2.34.2", commit="a7030915fbc6120cc6812aefdedba423a207459b")
    version("2.32.1", commit="f84d74424fa599f6d08f8db4612ca09914a9087f")

    depends_on("r-xml", type=("build", "run"))
    depends_on("r-xml@3.99-0.7:", type=("build", "run"), when="@2.52.0:")
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-progress", type=("build", "run"), when="@2.34.2:")
    depends_on("r-stringr", type=("build", "run"), when="@2.34.2:")
    depends_on("r-httr", type=("build", "run"), when="@2.34.2:")
    depends_on("r-digest", type=("build", "run"), when="@2.50.3:")
    depends_on("r-biocfilecache", type=("build", "run"), when="@2.46.2:")
    depends_on("r-rappdirs", type=("build", "run"), when="@2.46.2:")
    depends_on("r-xml2", type=("build", "run"), when="@2.46.2:")

    depends_on("r-rcurl", type=("build", "run"), when="@:2.40.5")
    depends_on("r-openssl", type=("build", "run"), when="@2.46.2")
