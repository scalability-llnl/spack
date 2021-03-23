# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Ngspice(AutotoolsPackage):
    """ngspice is the open source spice simulator for electric and
    electronic circuits."""

    homepage = "http://ngspice.sourceforge.net/"
    url      = "https://sourceforge.net/projects/ngspice/files/ngspice-33.tar.gz"

    version('34', sha256='2263fffc6694754972af7072ef01cfe62ac790800dad651bc290bfcae79bd7b5')
    version('33', sha256='b99db66cc1c57c44e9af1ef6ccb1dcbc8ae1df3e35acf570af578f606f8541f1')

    depends_on('fftw')

    def configure_args(self):
        args = []
        args.append('--without-x')
        args.append('--with-ngshared')
        return args
