# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XmlrpcC(AutotoolsPackage):
    """Programming library for writing an XML-RPC server or client in
    C or C++."""

    homepage = "https://sourceforge.net/projects/xmlrpc-c/"
    url      = "https://sourceforge.net/projects/xmlrpc-c/files/Xmlrpc-c%20Super%20Stable/1.51.06/xmlrpc-c-1.51.06.tgz"

    version('1.51.06', sha256='06dcd87d9c88374559369ffbe83b3139cf41418c1a2d03f20e08808085f89fd0')

    @when('target=aarch64:')
    def configure_args(self):
        args = ['--build=arm-linux']
        return args
