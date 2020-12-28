# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libidn2(AutotoolsPackage):
    """Libidn2 is a free software implementation of IDNA2008, Punycode and
    TR46. Its purpose is to encode and decode internationalized domain
    names."""

    homepage = "https://gitlab.com/libidn/libidn2"
    url      = "https://ftp.gnu.org/gnu/libidn/libidn2-2.0.5.tar.gz"

    version('2.3.0',  sha256='e1cb1db3d2e249a6a3eb6f0946777c2e892d5c5dc7bd91c74394fc3a01cab8b5')
    version('2.1.1a', sha256='57666bcf6ecf54230d7bac95c392379561954b57a673903aed4d3336b3048b72')
    version('2.1.1',  sha256='95416080329298a13269e13175041b530cec3d98b54cafae9424b8dfd22078b1')
    version('2.1.0',  sha256='032398dbaa9537af43f51a8d94e967e3718848547b1b2a4eb3138b20cad11d32')
    version('2.0.5',  sha256='53f69170886f1fa6fa5b332439c7a77a7d22626a82ef17e2c1224858bb4ca2b8')

    depends_on('libunistring')

    # in-source build fails
    build_directory = 'spack-build'
