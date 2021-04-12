# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class Irep(MakefilePackage):
    """IREP is a tool that enables mixed-language simulation codes to use a
    common, Lua-based format for their input decks. Essentially, the input
    format is a set of tables -- Lua's one (and only?) data structure."""

    homepage = "https://irep.readthedocs.io/"
    git      = "ssh://git@github.com:LLNL/irep.git"

    maintainers = ['tomstitt', 'kennyweiss']

    version('master', branch='master')

    depends_on('lua-luajit', type=('link', 'run'))
    depends_on('lua', type=('link', 'run'))

    def cmake_args(self):
        args = []
        args.append('-DCMAKE_PREFIX_PATH={0}'.format(self.prefix)) # Is there supposed to be more here?

        return args

    def install(self, spec, prefix):
        # Library
        mkdirp(prefix.lib)
        install('irep/libIR.a', prefix.lib)

        # Header
        mkdirp(prefix.include)
        install('irep/wkt_app.h', prefix.include)

        #mkdirp(prefix.share)
        #install('cmake/irep-config.cmake', prefix.share)
        #install('irep/wkt.mk', prefix.share)

        # irep-config.cmake
        super(self, irep).install(spec, prefix)
        install('CMAKE_PREFIX_PATH', self.prefix.share)

        # irep-generate
        mkdirp(prefix.bin)
        install('bim/irep-generate', prefix.bin)
