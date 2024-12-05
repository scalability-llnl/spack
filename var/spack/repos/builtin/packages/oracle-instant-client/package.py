# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


def oracleclient_releases():
    releases = [
        {
            "version": "21.1.0.0.0",
            "components": {
                "basic": [
                    "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basic-linux.x64-21.1.0.0.0.zip",
                    "9b63e264c01ac54a0f0e61bd638576aed6f04a36b305bcd17847755e7b9855ce",
                ],
                "sqlplus": [
                    "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sqlplus-linux.x64-21.1.0.0.0.zip",
                    "3220f486940e82f1a7825e8f0875729d63abd57cc708f1908e2d5f2163b93937",
                ],
                "tools": [
                    "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-tools-linux.x64-21.1.0.0.0.zip",
                    "ff652d5bbfeaaa2403cbc13c5667f52e1d648aa2a5c59a50f4c9f84e6d2bba74",
                ],
                "sdk": [
                    "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sdk-linux.x64-21.1.0.0.0.zip",
                    "80a465530a565ed327ab9ae0d9fc067ed42338536c7e8721cf2c26e474f4f75f",
                ],
                "jdbc": [
                    "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-jdbc-linux.x64-21.1.0.0.0.zip",
                    "76c866272712f2b432cc4be675605b22deca02f7a88a292b5ed8d29212d79dc7",
                ],
                "odbc": [
                    "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-odbc-linux.x64-21.1.0.0.0.zip",
                    "ec7722b522684f0a3f63481573d0eb3537764224eabed6223f33699dd940bf20",
                ],
            },
        },
        {
            "version": "19.10.0.0.0",
            "components": {
                "basic": [
                    "https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basic-linux.x64-19.10.0.0.0dbru.zip",
                    "c2eeea093d70f5416f8a8560f9fa5b57707a76ac9775906dbc4aaa778fdee84f",
                ],
                "sqlplus": [
                    "https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-sqlplus-linux.x64-19.10.0.0.0dbru.zip",
                    "eee44825f348966796166beb8c0d8cc8f61929bae05229b65b34794e0f05659a",
                ],
                "tools": [
                    "https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-tools-linux.x64-19.10.0.0.0dbru.zip",
                    "93bf58d2e15bb3ca98f8e5f579a93760571a37e0d9312187f6a5f228d492c863",
                ],
                "sdk": [
                    "https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-sdk-linux.x64-19.10.0.0.0dbru.zip",
                    "2c4ae1b77fe32f3d3bf86a4ef560dc3a5dcbf5d11d742b4afeca414e5388ff2f",
                ],
                "jdbc": [
                    "https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-jdbc-linux.x64-19.10.0.0.0dbru.zip",
                    "3fabbc4a86b8c5b4b29c4d76524c7d7e5bfab33cdbfa73f1199fc5582ed25df6",
                ],
                "odbc": [
                    "https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-odbc-linux.x64-19.10.0.0.0dbru.zip",
                    "1c7ae3ea5913af9647ae68e2053cdaf9154ef6c9aa07e8b7d91e1ead9d5e675a",
                ],
            },
        },
    ]

    return releases


class OracleInstantClient(Package):
    """Oracle instant client"""

    homepage = "https://www.oracle.com/database/technologies/instant-client.html"
    url = "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basic-linux.x64-21.1.0.0.0.zip"

    releases = oracleclient_releases()
    for release in releases:
        oracle_version = release["version"]
        main_pkg = release["components"]["basic"]
        url, sha256 = main_pkg
        version(oracle_version, sha256=sha256, url=url)
        for rname, atts in release["components"].items():
            if rname == "basic":
                continue
            url, sha256 = atts
            condition = "@{0}".format(oracle_version)
            resource(name=rname, url=url, sha256=sha256, when=condition, placement=rname)

    depends_on("libaio", type="link")

    # TODO: add URLs for macOS. Unfortunately still no native M1 support.
    # https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html
    conflicts("platform=darwin")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        mkdirp(prefix.doc)

        for dirn, fns in {
            ".": ("adrci", "genezi", "uidrvci"),
            "sqlplus": ("glogin.sql", "sqlplus"),
            "odbc": ("odbc_update_ini.sh",),
            "tools": ("exp", "expdp", "imp", "impdp", "sqlldr", "wrc"),
        }.items():
            for fn in fns:
                install(join_path(dirn, fn), prefix.bin)

        for fn in glob.glob(join_path(self.stage.source_path, "*.so*")):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, "*.jar")):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, "sqlplus", "*.so*")):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, "jdbc", "*.so*")):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, "odbc", "*.so*")):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, "tools", "*.so*")):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, "jdbc", "*.jar")):
            install(fn, prefix.lib)

        install_tree("network", prefix.lib)

        for dirn, fns in {
            ".": ("BASIC_LICENSE", "BASIC_README"),
            "sqlplus": ("SQLPLUS_LICENSE", "SQLPLUS_README"),
            "jdbc": ("JDBC_LICENSE", "JDBC_README"),
            "odbc": ("ODBC_LICENSE", "ODBC_README"),
            "sdk": ("SDK_LICENSE", "SDK_README"),
            "tools": ("TOOLS_LICENSE", "TOOLS_README"),
        }.items():
            for fn in fns:
                install(join_path(dirn, fn), prefix.doc)

        install_tree(join_path("odbc", "help"), prefix.doc)
        install_tree(join_path("sdk", "sdk", "include"), prefix.include)
