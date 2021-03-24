# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class Irep(MakefilePackage):
    """IREP is a tool that enables mixed-language simulation codes to use a
    common, Lua-based format for their input decks. Essentially, the input
    format is a set of tables -- Lua's one (and only?) data structure."""

    homepage = "https://irep.readthedocs.io/"
    url      = "ssh://git@github.com:LLNL/irep.git"

    version('master', '5e0c98cd230eaf5bf918dbec3645ac5786aa6c457b573e1091f83d06dc2e1b08')

    depends_on('lua-luajit', type=('link', 'run'))
    depends_on('lua', type=('link', 'run'))

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
