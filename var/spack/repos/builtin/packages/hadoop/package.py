# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hadoop(Package):
    """The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models.
    """

    homepage = "http://hadoop.apache.org/"
    url      = "https://www.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz"

    version('3.2.1',  sha256='f66a3a4115b8f16c1077d1a198a06854dbef0e4233291712ed08d0a10629ed37')
    version('3.1.3',  sha256='1e8b7ca4e3911f8ec999595f71921390e9ad7a27255fbd36af1f3a1628b67e2b')
    version('2.10.0', sha256='131750c258368be4baff5d4a83b4de2cd119bda3774ed26d1d233b6fdf33f07f')
    version('2.9.2',  sha256='3d2023c46b1156c1b102461ad08cbc17c8cc53004eae95dab40a1f659839f28a')
    version('2.8.5',  sha256='f9c726df693ce2daa4107886f603270d66e7257f77a92c9886502d6cd4a884a4')
    version('2.7.7',  sha256='d129d08a2c9dafec32855a376cbd2ab90c6a42790898cabbac6be4d29f9c2026')

    depends_on('java', type='run')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('etc')
        install_dir('include')
        install_dir('lib')
        install_dir('libexec')
        install_dir('sbin')
        install_dir('share')
