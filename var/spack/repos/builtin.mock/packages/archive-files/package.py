# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ArchiveFiles(AutotoolsPackage):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")

    @property
    def archive_files(self):
        return super().archive_files + ["../../outside.log"]

    def autoreconf(self, spec, prefix):
        pass

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        mkdirp(self.build_directory)
        config_log = join_path(self.build_directory, "config.log")
        touch(config_log)

    def install(self, spec, prefix):
        touch(join_path(prefix, "deleteme"))
