# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MongoCxxDriver(CMakePackage):
    """C++ Driver for MongoDB"""

    homepage = "http://www.mongocxx.org"
    url = "https://github.com/mongodb/mongo-cxx-driver/releases/download/r3.7.0/mongo-cxx-driver-r3.7.0.tar.gz"
    git = "https://github.com/mongodb/mongo-cxx-driver"

    license("Apache-2.0")

    version("3.10.1", sha256="0297d9d1a513f09438cc05254b14baa49edd1fa64a6ce5d7a80a1eb7677cf2be")
    version("3.7.0", sha256="fb2da11178db728f63147fe4b0c7509eb49b1b02c5cb55f9bee5f927e451a0c7")
    version("3.6.7", sha256="2c58005d4fe46f1973352fba821f7bb37e818cefc922377ce979a9fd1bff38ac")
    version("3.6.6", sha256="d5906b9e308a8a353a2ef92b699c9b27ae28ec6b34fdda94e15d2981b27e64ca")
    version("3.6.5", sha256="83ded94c28ef26151371eeea2204e5923565c9305bfc12812a26af98e91cf8ea")
    version("3.6.4", sha256="4be223bb221c86fb07b41f92c19eebde2983f2e5ebcab90574b1a2075d0bf43a")
    version("3.6.3", sha256="8a3624f91fe85328864a09508d7678aa8c9bc0504bd236aaea6c250ff230c6a3")
    version("3.6.2", sha256="24325dce74723f7632da76d0eeb5f5020828498cc5bc1a624c6d7117efb2b7cf")
    version("3.6.1", sha256="83523e897ef18f7ce05d85d1632dd4ba486c264a1b89c09020163ab29e11eab7")
    version("3.6.0", sha256="3bb3177e204e0d9596a103519251793e64144b2bb2e4156baf1fa3683c9814bf")
    version("3.5.1", sha256="47690f601a09a92e7f4f7b77ebf452176efece67d78f84fc5b7c52d8d0eff97e")
    version("3.5.0", sha256="2a61369e616c4c08310586c339a27bddee0482305e1dcc83ce08e3529cfa5b7a")
    version("3.4.2", sha256="6dc6d4ca151e3fd0e99e466b6de26078eb97cbec321f2913ba49f321de2afab3")
    version("3.4.1", sha256="3849908af8b722e23750f2f45b4ceb8ca22961440d57b706fb381cd567752141")
    version("3.4.0", sha256="e9772ac5cf1c996c2f77fd78e25aaf74a2abf5f3864cb31b18d64955fd41c14d")
    version("3.3.2", sha256="0de36003d5270997c6283478a928b4e25c7e6c10c181cf1a9cd210be5e9c65a7")
    version("3.3.1", sha256="ce25962b0674d35fe67605bb28c6c9138e7799d503da1919779405ee7564c569")
    version("3.3.0", sha256="22857d0985039ca1bf77b7c709d4306a4d0728e1f839eccdb439415f1b26e199")
    version("3.2.1", sha256="d5e62797cbc48c6e5e18bc0a66c14556e78871d05db4bccc295074af51b8421e")
    version("3.2.0", sha256="e26edd44cf20bd6be91907403b6d63a065ce95df4c61565770147a46716aad8c")

    depends_on("cxx", type="build")  # generated

    depends_on("mongo-c-driver@1.9.2:")

    def url_for_version(self, version):
        git_archive = self.git + "/archive/refs/tags/r{version}.tar.gz"
        release_url = self.git + "/releases/download/r{version}/mongo-cxx-driver-r{version}.tar.gz"
        template_url = release_url if self.spec.satisfies("@3.6.0:") else git_archive
        return template_url.format(version=version)
