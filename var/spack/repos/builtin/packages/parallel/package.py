# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parallel(AutotoolsPackage, GNUMirrorPackage):
    """GNU parallel is a shell tool for executing jobs in parallel using
    one or more computers. A job can be a single command or a small
    script that has to be run for each of the lines in the input.
    """

    homepage = "http://www.gnu.org/software/parallel/"
    gnu_mirror_path = "parallel/parallel-20170122.tar.bz2"

    version('20200822', sha256='9654226a808392c365b1e7b8dea91bf4870bc4f306228d853eb700679e21be09')
    version('20190222', sha256='86b1badc56ee2de1483107c2adf634604fd72789c91f65e40138d21425906b1c')
    version('20170322', sha256='f8f810040088bf3c52897a2ee0c0c71bd8d097e755312364b946f107ae3553f6')
    version('20170122', sha256='417e83d9de2fe518a976fcff5a96bffe41421c2a57713cd5272cc89d1072aaa6')
    version('20160422', sha256='065a8f471266361218a9eb45c5f8ab995d73b181cc1180600ee08cc768c9ac42')
    version('20160322', sha256='6430f649ec07243645c955e8d6bee6da1df2e699b1e49b185946d1ab38731b08')

    def check(self):
        # The Makefile has a 'test' target, but it does not work
        make('check')

    depends_on('perl', type=('build', 'run'))

    @run_before('install')
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
           can fix up the path to the perl binary.
        """
        perl = self.spec['perl'].command
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

        with working_dir('src'):
            match = '^#!/usr/bin/env perl|^#!/usr/bin/perl.*'
            substitute = "#!{perl}".format(perl=perl)
            files = ['parallel', 'niceload', 'parcat', 'sql', ]
            filter_file(match, substitute, *files, **kwargs)
