# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hadoop(Package):
    """The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models.
    """

    homepage = "https://hadoop.apache.org/"
    url = "https://archive.apache.org/dist/hadoop/common/hadoop-3.3.2/hadoop-3.3.2.tar.gz"
    list_url = "https://archive.apache.org/dist/hadoop/common"
    list_depth = 1

    license("Apache-2.0", checked_by="wdconinc")

    version("3.4.0", sha256="e311a78480414030f9ec63549a5d685e69e26f207103d9abf21a48b9dd03c86c")
    version("3.3.6", sha256="f5195059c0d4102adaa7fff17f7b2a85df906bcb6e19948716319f9978641a04")
    version("3.3.5", sha256="446e05ca92fa23a60617a8b17946dede47281af1504041617cb7d5f62e74252a")
    version("3.3.4", sha256="6a483d1a0b123490ebd8df3f71b64eb39f333f78b95f090aeb58e433cbc2416d")
    version("3.3.3", sha256="fa71c61bbaa427129aef09fec028b34dd542c65ad90fdccec5e7ef93d83b8764")
    version("3.3.2", sha256="b341587495b12eec0b244b517f21df88eb46ef634dc7dc3e5969455b80ce2ce5")
    version("3.3.0", sha256="ea1a0f0afcdfb9b6b9d261cdce5a99023d7e8f72d26409e87f69bda65c663688")
    version("3.2.2", sha256="97e73b46c3972cd3c40c2295bd9488843c24e8503c36e7c57f6e6ecc4e12b8c3")
    version("3.2.1", sha256="f66a3a4115b8f16c1077d1a198a06854dbef0e4233291712ed08d0a10629ed37")
    version("3.1.3", sha256="1e8b7ca4e3911f8ec999595f71921390e9ad7a27255fbd36af1f3a1628b67e2b")
    version("2.10.1", sha256="273d5fa1d479d0bb96759b16cf4cbd6ba3e7f863a0778cbae55ab83417e961f0")
    version("2.10.0", sha256="131750c258368be4baff5d4a83b4de2cd119bda3774ed26d1d233b6fdf33f07f")
    version("2.9.2", sha256="3d2023c46b1156c1b102461ad08cbc17c8cc53004eae95dab40a1f659839f28a")
    version("2.8.5", sha256="f9c726df693ce2daa4107886f603270d66e7257f77a92c9886502d6cd4a884a4")
    version("2.7.7", sha256="d129d08a2c9dafec32855a376cbd2ab90c6a42790898cabbac6be4d29f9c2026")
    version("2.7.5", sha256="0bfc4d9b04be919be2fdf36f67fa3b4526cdbd406c512a7a1f5f1b715661f831")

    depends_on("java", type="run")

    def install(self, spec, prefix):
        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir("bin")
        install_dir("etc")
        install_dir("include")
        install_dir("lib")
        install_dir("libexec")
        install_dir("sbin")
        install_dir("share")
