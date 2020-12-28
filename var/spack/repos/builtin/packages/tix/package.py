# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tix(AutotoolsPackage):
    """Tix is a powerful high-level widget set that expands the capabilities
       of your Tk/Tcl and Python applications."""

    homepage = "https://sourceforge.net/projects/tix/"
    url      = "https://sourceforge.net/projects/tix/files/tix/8.4.3/Tix8.4.3-src.tar.gz/download"
    version('8.4.3', sha256='562f040ff7657e10b5cffc2c41935f1a53c6402eb3d5f3189113d734fd6c03cb')

    extends('tcl')
    depends_on('tk@:8.5.99')
    depends_on('tcl@:8.5.99')

    def configure_args(self):
        spec = self.spec
        args = [
            '--with-tcl={0}'.format(spec['tcl'].libs.directories[0]),
            '--with-tk={0}'.format(spec['tk'].libs.directories[0]),
            '--exec-prefix={0}'.format(self.prefix),
        ]
        return args

    @property
    def libs(self):
        return find_libraries(['libTix{0}'.format(self.version)],
                              root=self.prefix, recursive=True)
