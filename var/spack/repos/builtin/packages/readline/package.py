# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Readline(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Readline library provides a set of functions for use by
    applications that allow users to edit command lines as they are typed in.
    Both Emacs and vi editing modes are available. The Readline library
    includes additional functions to maintain a list of previously-entered
    command lines, to recall and perhaps reedit those lines, and perform
    csh-like history expansion on previous commands."""

    homepage = "https://tiswww.case.edu/php/chet/readline/rltop.html"
    # URL must remain http:// so Spack can bootstrap curl
    gnu_mirror_path = "readline/readline-8.0.tar.gz"

    version('8.1', sha256='f8ceb4ee131e3232226a17f51b164afc46cd0b9e6cef344be87c65962cb82b02')
    version('8.0', sha256='e339f51971478d369f8a053a330a190781acb9864cf4c541060f12078948e461')
    version('7.0', sha256='750d437185286f40a369e1e4f4764eda932b9459b5ec9a731628393dd3d32334')
    version('6.3', sha256='56ba6071b9462f980c5a72ab0023893b65ba6debb4eeb475d7a563dc65cafd43')

    depends_on('ncurses')
    # from url=http://www.linuxfromscratch.org/patches/downloads/readline/readline-6.3-upstream_fixes-1.patch
    # this fixes a bug that could lead to seg faults in ipython
    patch('readline-6.3-upstream_fixes-1.patch', when='@6.3')

    def build(self, spec, prefix):
        make('SHLIB_LIBS=' + spec['ncurses'].libs.ld_flags)

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc'):
            filter_file('${GCC+-Wno-parentheses}', '', 'configure',
                        string=True)
            filter_file('${GCC+-Wno-format-security}', '', 'configure',
                        string=True)
