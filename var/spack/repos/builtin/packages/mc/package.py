# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mc(AutotoolsPackage):
    """The GNU Midnight Commander is a visual file manager."""

    homepage = "https://midnight-commander.org"
    url      = "http://ftp.midnight-commander.org/mc-4.8.20.tar.bz2"

    version('4.8.20', 'dcfc7aa613c62291a0f71f6b698d8267')

    depends_on('ncurses')
    depends_on('pkgconfig', type='build')
    depends_on('glib@2.14:')
    depends_on('libssh2@1.2.5:')

    def setup_environment(self, spack_env, run_env):
        # Fix compilation bug on macOS by pretending we don't have utimensat()
        # https://github.com/MidnightCommander/mc/pull/130
        if 'darwin' in self.spec.architecture:
            env['ac_cv_func_utimensat'] = 'no'

    def configure_args(self):
        args = [
            '--disable-debug',
            '--disable-dependency-tracking',
            '--disable-silent-rules',
            '--without-x',
            '--with-screen=ncurses',
            '--enable-vfs-sftp'
        ]
        return args
