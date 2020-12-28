# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spiral(CMakePackage):
    """SPIRAL is a program generation system for linear transforms and other
    mathematical functions that produces very high performance code for a wide
    spectrum of hardware platforms."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/spiral-software/archive/8.1.2.tar.gz"

    maintainers = ['spiralgen']

    version('8.2.0', sha256='983f38d270ae2cb753c88cbce3f412e307c773807ad381acedeb9275afc0be32')
    version('8.1.2', sha256='506f1dbf923aa1c9f19f05444fa947085715eef37c9d2494d133fcaaa1dd50bc')

    extendable = True

    # No dependencies.

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make('all')
            make('install/local')

        # For some reason the make install/local doesn't seem to install
        # the gap exe...though it does work if run manually
        gapfil = join_path(self.build_directory, 'gap/src/gap')
        dest = join_path(self.stage.source_path, 'gap/bin')
        install(gapfil, dest)

    def install(self, spec, prefix):
        mkdirp(prefix.gap.bin)
        gapfil = join_path(self.build_directory, 'gap/src/gap')
        install(gapfil, prefix.gap.bin)
        with working_dir(join_path(self.build_directory, 'gap')):
            files = ('spiral', 'spirald', '_spiral.g')
            for fil in files:
                install(fil, prefix)
                set_executable(join_path(prefix, fil))

        with working_dir(self.stage.source_path):
            files = ('LICENSE', 'README.md', 'ReleaseNotes.md')
            for fil in files:
                install(fil, prefix)

        mkdirp(prefix.gap.lib)
        mkdirp(prefix.gap.grp)
        mkdirp(prefix.namespaces)
        mkdirp(prefix.profiler)
        mkdirp(prefix.tests)

        print("self.stage.source_path = " + self.stage.source_path)
        with working_dir(self.stage.source_path):
            install_tree('namespaces', prefix.namespaces)
            install_tree('profiler', prefix.profiler)
            install_tree('tests', prefix.tests)

        with working_dir(join_path(self.stage.source_path, 'gap')):
            install_tree('lib', prefix.gap.lib)
            install_tree('grp', prefix.gap.grp)
