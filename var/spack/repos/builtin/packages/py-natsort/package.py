# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNatsort(PythonPackage):
    """Simple yet flexible natural sorting in Python."""

    homepage = "https://pypi.org/project/natsort/"
    url = "https://github.com/SethMMorton/natsort/archive/5.2.0.zip"

    version('5.2.0', sha256='0ae15082842e8a3598750b4bbaa4f7c138caf004e59c7040429d56bf9e9631bd')
    version('5.1.1', sha256='6467eeca268d9accb2e3149acace49649f865b0051a672006a64b20597f04561')
    version('5.1.0', sha256='79279792cc97a0005b2075ed2bc9b8a3e25e5edffe43ee2fb26b116283f5dab4')
    version('5.0.3', sha256='408f6fa87f6bbe3e09b255286d4db7b678bf22d6a5cd1651d05bfc1f99792a2e')
    version('5.0.2', sha256='6315d94b6651edd9bf1e29cfd513a0349ec46a38ed38d33121a11d5162dbe556')
    version('5.0.1', sha256='fe915cd4ddc90182947758b77873dda42935d5493819df8439f2daef01ffaacb')
    version('5.0.0', sha256='b46b3569ac69e8f4a88f1a479d108872857538c7564226c32df1fd75e809c240')
    version('4.0.4', sha256='14e5ddaf689de2f5ac33aa7963554fa2944b019f526ece1036d74fe60528531b')
    version('4.0.3', sha256='8824792d7ebc37a57010e1ba301244653f8655ea20ddab6b0d546cf1d9ffedda')
    version('4.0.1', sha256='1c1d29150938ca71f0943363a06765dbb2cea01f9c4d760ba880cc65f39baba0')

    depends_on('py-setuptools', type=('build'))
