# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iproute2(AutotoolsPackage):
    """This is a set of utilities for Linux networking."""

    homepage = "https://github.com/shemminger/iproute2"
    url      = "https://github.com/shemminger/iproute2/archive/v5.9.0.tar.gz"

    version('5.9.0', sha256='1afde56d416f136b1236ac2f8276e4edbe114ca3c2ab12f11af11b84cf0992e4')
    version('5.8.0', sha256='78c73ed49c35fae59ab4e9d88220dcc70da924de3838e13a3cdc7c09496e5a45')
    version('5.7.0', sha256='12a3861f463c6bbd1bb3b213ac734f75c89172b74104140dd0bbfcb1e13ee798')
    version('5.6.0', sha256='be41c35eddb02e736a2040b66ccfacee41fe7ee454580588f8959568d8a3c5b3')
    version('5.5.0', sha256='5bc88876a3140f640e3318453382be5be4c673ccc17a518c05a5ce2ef9aa9a7f')

    def install(self, spec, prefix):
        make('install', 'DESTDIR={0}'.format(prefix), 'PREFIX=')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
