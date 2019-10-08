# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SublimeText(Package):
    """Sublime Text is a sophisticated text editor for code, markup and
    prose."""

    homepage = "http://www.sublimetext.com/"
    url      = "https://download.sublimetext.com/sublime_text_3_build_3211_x64.tar.bz2"

    version('3.2.2.3211', sha256='0b3c8ca5e6df376c3c24a4b9ac2e3b391333f73b229bc6e87d0b4a5f636d74ee')
    version('3.2.1.3207', sha256='acb64f1de024a0f004888096afa101051e48d96c7a3e7fe96e11312d524938c4')
    version('3.1.1.3176', '7d4c8c5167224888d901e8cbafb6ec7f')
    version('3.0.3126',   'acc34252b0ea7dff1f581c5db1564dcb')
    version('2.0.2',      '699cd26d7fe0bada29eb1b2cd7b50e4b')

    # Sublime text comes as a pre-compiled binary.
    # Since we can't link to Spack packages, we'll just have to
    # add them as runtime dependencies.

    # depends_on('libgobject', type='run')
    depends_on('gtkplus@:2', type='run', when='@:3.1')
    depends_on('gtkplus@3:', type='run', when='@3.2:')
    depends_on('glib', type='run')
    depends_on('libx11', type='run')
    depends_on('pcre', type='run')
    depends_on('libffi', type='run')
    depends_on('libxcb', type='run')
    depends_on('libxau', type='run')

    def url_for_version(self, version):
        if version[0] == 2:
            return "https://download.sublimetext.com/Sublime%20Text%20{0}%20x64.tar.bz2".format(version)
        else:
            return "https://download.sublimetext.com/sublime_text_{0}_build_{1}_x64.tar.bz2".format(version[0], version[-1])

    def install(self, spec, prefix):
        install_tree('.', prefix)
        src = join_path(prefix, 'sublime_text')
        dst = join_path(prefix, 'bin')
        mkdirp(dst)
        force_symlink(src, join_path(dst, 'sublime_text'))
        force_symlink(src, join_path(dst, 'subl'))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', join_path(self.prefix, "bin"))
