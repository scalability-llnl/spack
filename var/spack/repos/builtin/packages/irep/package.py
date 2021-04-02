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

    version('master', branch='master')

    depends_on('lua-luajit', type=('link', 'run'))
    depends_on('lua', type=('link', 'run'))

    def cmake_args(self):
        args = []
        args.append('-DIREP_GENERATE={0}'.format(self.prefix.bin.irep-generate))
        args.append('-DIREP_LIBRARIES={0}'.format(self.prefix.lib.libIR.a))
        args.append('-DIREP_INCLUDE_DIR={0}'.format(self.prefix))

        return args

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        mkdirp(prefix.lib)
        install('irep/libIR.a', prefix.lib)
