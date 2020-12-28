# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E2fsprogs(AutotoolsPackage):
    """It provides the filesystem utilities for use with the ext2 filesystem.
    It also supports the ext3 and ext4 filesystems."""

    homepage = "https://github.com/tytso/e2fsprogs"
    url      = "https://github.com/tytso/e2fsprogs/archive/v1.45.6.tar.gz"

    version('1.45.6', sha256='d785164a2977cd88758cb0cac5c29add3fe491562a60040cfb193abcd0f9609b')
    version('1.45.5', sha256='0fd76e55c1196c1d97a2c01f2e84f463b8e99484541b43ff4197f5a695159fd3')

    depends_on('texinfo', type='build')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
