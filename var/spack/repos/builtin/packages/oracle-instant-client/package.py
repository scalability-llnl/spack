# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

def oracleclient_releases():
    releases = [
    {
        'version': '21.1.0.0.0',
        'components': {
           'basic': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basic-linux.x64-21.1.0.0.0.zip', '9b63e264c01ac54a0f0e61bd638576aed6f04a36b305bcd17847755e7b9855ce'],
           'sqlplus': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sqlplus-linux.x64-21.1.0.0.0.zip', '3220f486940e82f1a7825e8f0875729d63abd57cc708f1908e2d5f2163b93937'],
           'tools': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-tools-linux.x64-21.1.0.0.0.zip', 'ff652d5bbfeaaa2403cbc13c5667f52e1d648aa2a5c59a50f4c9f84e6d2bba74'],
           'sdk': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sdk-linux.x64-21.1.0.0.0.zip', '80a465530a565ed327ab9ae0d9fc067ed42338536c7e8721cf2c26e474f4f75f'],
           'jdbc': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-jdbc-linux.x64-21.1.0.0.0.zip', '76c866272712f2b432cc4be675605b22deca02f7a88a292b5ed8d29212d79dc7'],
           'odbc': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-odbc-linux.x64-21.1.0.0.0.zip', 'ec7722b522684f0a3f63481573d0eb3537764224eabed6223f33699dd940bf20']
        }
    }]
    
    return releases


class OracleInstantClient(Package):
    """Oracle instant client"""

    homepage = "https://www.oracle.com/database/technologies/instant-client.html"
    url      = "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basic-linux.x64-21.1.0.0.0.zip"
    
    releases = oracleclient_releases()
    for release in releases:
        # define the version using the mscore tarball
        oracle_version = release['version']
        main_pkg = release['components']['basic']
        url, sha256 = main_pkg
        version(oracle_version, sha256=sha256, url=url)
        # define resources for the other tarballs
        for name, atts in release['components'].items():
            # skip the tarball used for the version(...) call
            if name == 'basic':
                continue
            url, sha256 = atts
            condition = "@{0}".format(oracle_version)
            resource(name=name, url=url, sha256=sha256, when=condition, placement=name)

    def patch(self):
        pass
    
    def install(self, spec, prefix):
        pass
