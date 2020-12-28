# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

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

    The BioPerl website at http://bioperl.org also attempts to maintain links
    and archives of standalone bio-related Perl tools that are not affiliated
    or related to the core BioPerl effort. Check the site for useful code ideas
    and contribute your own if possible."""

    homepage = "https://metacpan.org/pod/BioPerl"
    url      = "https://cpan.metacpan.org/authors/id/C/CD/CDRAUG/BioPerl-1.7.6.tar.gz"

    version('1.7.6',
            sha256='df2a3efc991b9b5d7cc9d038a1452c6dac910c9ad2a0e47e408dd692c111688d',
            preferred=True)
    version('1.007002', sha256='17aa3aaab2f381bbcaffdc370002eaf28f2c341b538068d6586b2276a76464a1',
            url='https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/BioPerl-1.007002.tar.gz')

    # According to cpandeps.grinnz.com Module-Build is both a build and run
    # time dependency for BioPerl
    depends_on('perl-module-build', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-io-string', type=('build', 'run'))
    depends_on('perl-data-stag', type=('build', 'run'))
    depends_on('perl-test-most', type=('build', 'run'))
    depends_on('perl-error', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-graph', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-http-message', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-io-stringy', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-ipc-run', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-list-moreutils', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-set-scalar', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-test-requiresinternet', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-dom', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-dom-xpath', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-libxml', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-sax', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-sax-base', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-sax-writer', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-twig', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-xml-writer', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-yaml', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-libwww-perl', when='@1.7.6:', type=('build', 'run'))
    depends_on('perl-libxml-perl', when='@1.7.6:', type=('build', 'run'))

    @when('@1.007002')
    def configure(self, spec, prefix):
        # Overriding default configure method in order to cater to interactive
        # Build.pl
        self.build_method = 'Build.PL'
        self.build_executable = Executable(
            join_path(self.stage.source_path, 'Build'))

        # Config questions consist of:
        #    Do you want to run the Bio::DB::GFF or Bio::DB::SeqFeature::Store
        #        live database tests? y/n [n]
        #
        #    Install [a]ll BioPerl scripts, [n]one, or choose groups
        #        [i]nteractively? [a]
        #
        #    Do you want to run tests that require connection to servers across
        #        the internet (likely to cause some failures)? y/n [n]
        #
        # Eventually, someone can add capability for the other options, but
        # the current answers are the most practical for a spack install.

        config_answers = ['n\n', 'a\n', 'n\n']
        config_answers_filename = 'spack-config.in'

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            inspect.getmodule(self).perl('Build.PL', '--install_base=%s' %
                                         self.prefix, input=f)

    # Need to also override the build and install methods to make sure that the
    # Build script is run through perl and not use the shebang, as it might be
    # too long. This is needed because this does not pick up the
    # `@run_after(configure)` step defined in `PerlPackage`.
    @when('@1.007002')
    def build(self, spec, prefix):
        inspect.getmodule(self).perl('Build')

    @when('@1.007002')
    def install(self, spec, prefix):
        inspect.getmodule(self).perl('Build', 'install')
