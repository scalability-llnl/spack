# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCertifi(PythonPackage):
    """Certifi: A carefully curated collection of Root Certificates for validating
    the trustworthiness of SSL certificates while verifying the identity of TLS
    hosts."""

    homepage = "http://certifi.io/"
    url      = "https://pypi.io/packages/source/c/certifi/certifi-2020.6.20.tar.gz"

    version('2020.6.20', sha256='5930595817496dd21bb8dc35dad090f1c2cd0adfaf21204bf6732ca5d8ee34d3')
    version('2019.9.11', sha256='e4f3620cfea4f83eedc95b24abd9cd56f3c4b146dd0177e83a21b4eb49e21e50')
    version('2019.6.16', sha256='945e3ba63a0b9f577b1395204e13c3a231f9bc0223888be653286534e5873695')
    version('2019.3.9',  sha256='b26104d6835d1f5e49452a26eb2ff87fe7090b89dfcaee5ea2212697e1e1d7ae')
    version('2017.4.17', sha256='f7527ebf7461582ce95f7a9e03dd141ce810d40590834f4ec20cddd54234c10a')
    version('2017.1.23', sha256='81877fb7ac126e9215dfb15bfef7115fdc30e798e0013065158eed0707fd99ce')

    depends_on('py-setuptools', type='build')
