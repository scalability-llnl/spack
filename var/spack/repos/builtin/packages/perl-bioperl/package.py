# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBioperl(PerlPackage):
    """BioPerl is the product of a community effort to produce Perl code which
    is useful in biology. Examples include Sequence objects, Alignment objects
    and database searching objects. These objects not only do what they are
    advertised to do in the documentation, but they also interact - Alignment
    objects are made from the Sequence objects, Sequence objects have access to
    Annotation and SeqFeature objects and databases, Blast objects can be
    converted to Alignment objects, and so on. This means that the objects
    provide a coordinated and extensible framework to do computational biology.

    BioPerl development focuses on Perl classes, or code that is used to create
    objects representing biological entities. There are scripts provided in the
    scripts/ and examples/ directories but scripts are not the main focus of
    the BioPerl developers. Of course, as the objects do most of the hard work
    for you, all you have to do is combine a number of objects together
    sensibly to make useful scripts.

    The intent of the BioPerl development effort is to make reusable tools that
    aid people in creating their own sites or job-specific applications.

    The BioPerl website at https://bioperl.org/ also attempts to maintain links
    and archives of standalone bio-related Perl tools that are not affiliated
    or related to the core BioPerl effort. Check the site for useful code ideas
    and contribute your own if possible."""

    homepage = "https://metacpan.org/pod/BioPerl"
    url = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/BioPerl-1.7.8.tar.gz"

    license("Artistic-1.0")

    version("1.7.8", sha256="c490a3be7715ea6e4305efd9710e5edab82dabc55fd786b6505b550a30d71738")
    version(
        "1.7.6",
        sha256="df2a3efc991b9b5d7cc9d038a1452c6dac910c9ad2a0e47e408dd692c111688d",
        url="https://cpan.metacpan.org/authors/id/C/CD/CDRAUG/BioPerl-1.7.6.tar.gz",
    )
    version("1.6.924", sha256="616a7546bb3c58504de27304a0f6cb904e18b6bbcdb6a4ec8454f2bd37bb76d0")

    # This is technically the same as 1.7.2, but with a more conventional version number.
    version(
        "1.007002",
        sha256="17aa3aaab2f381bbcaffdc370002eaf28f2c341b538068d6586b2276a76464a1",
        url="https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/BioPerl-1.007002.tar.gz",
        deprecated=True,
    )

    with default_args(type=("build", "run")):
        depends_on("perl-data-stag")
        depends_on("perl-error")
        depends_on("perl-graph")
        depends_on("perl-http-message")
        depends_on("perl-io-string")
        depends_on("perl-io-stringy")
        depends_on("perl-ipc-run")
        depends_on("perl-libwww-perl")
        depends_on("perl-libxml-perl")
        depends_on("perl-list-moreutils")
        depends_on("perl-module-build")
        depends_on("perl-set-scalar")
        depends_on("perl-test-most")
        depends_on("perl-test-requiresinternet")
        depends_on("perl-uri")
        depends_on("perl-xml-dom")
        depends_on("perl-xml-dom-xpath")
        depends_on("perl-xml-libxml")
        depends_on("perl-xml-parser")
        depends_on("perl-xml-sax")
        depends_on("perl-xml-sax-base")
        depends_on("perl-xml-sax-writer")
        depends_on("perl-xml-simple")
        depends_on("perl-xml-twig")
        depends_on("perl-yaml")

        with when("@:1.7.0"):
            depends_on("perl-clone")
            depends_on("perl-db-file")
            depends_on("perl-dbd-mysql")
            depends_on("perl-dbd-pg")
            depends_on("perl-dbd-sqlite")
            depends_on("perl-dbi")
            depends_on("perl-gd")
            depends_on("perl-graphviz")
            depends_on("perl-scalar-list-utils")
            depends_on("perl-set-scalar")
            depends_on("perl-svg")

        # TODO:
        #     variant("optionaldeps", default=False, description="Add optional dependencies")
        #        with when("@:1.7.0+optionaldeps"):
        #            depends_on("perl-sort-naturally")
        #            depends_on("perl-test-harness")
        #            depends_on("perl-text-parsewords")
        #            depends_on("perl-algorithm-munkres")
        #            depends_on("perl-array-compare")
        #            depends_on("perl-bio-phylo")
        #            depends_on("perl-convert-binary-c")
        #            depends_on("perl-html-entities")
        #            depends_on("perl-html-headparser")
        #            depends_on("perl-html-tableextract")
        #            depends_on("perl-svg-graph")

        def configure_args(self):
            args = ["--accept=1"]
            return args
