# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LinuxPam(AutotoolsPackage):
    """Linux PAM (Pluggable Authentication Modules for Linux) project."""

    homepage = "http://www.linux-pam.org/"
    url      = "https://github.com/linux-pam/linux-pam/releases/download/v1.3.1/Linux-PAM-1.3.1.tar.xz"

    version('1.3.1', sha256='eff47a4ecd833fbf18de9686632a70ee8d0794b79aecb217ebd0ce11db4cd0db')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    def configure_args(self):
        config_args = [
            '--includedir=' + self.prefix.include.security
        ]
        return config_args
