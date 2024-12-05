# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class H2database(MavenPackage):
    """H2 is an embeddable RDBMS written in Java."""

    homepage = "https://h2database.com"
    url = "https://github.com/h2database/h2database/archive/version-1.4.200.tar.gz"

    version("1.4.200", sha256="59df19cc708442ae54a9639fc1c8c98ec6a55f66c154b39807032ba04fbe9c92")
    version("1.4.199", sha256="0f59d6e4ca71dda44a252897ca717a873abc1db800011fa068a7a57f921193ce")
    version("1.4.198", sha256="abba231e41ca31a9cc6571987ad97fe2c43232dc6d0e01c69ffbfcf3ea838967")
    version("1.4.197", sha256="46d883a491f56270bbd681afc8237a5d69787c1838561e8680afbac693c26344")
    version("1.4.196", sha256="9b0c7edac6ab7faad25743702aff1af63329fca37f6f5677908ae31ab968b219")
    version("1.4.195", sha256="ad7fe6cd2c2ef08eb026279468e4d2b37c979c053fd7a523982d843a03a8c560")
    version("1.4.194", sha256="0941a0d704be6e381644a39fa6003c0b0203905285a8330c905b950dfa2bbe31")
    version("1.4.193", sha256="7da24c48c2f06b59e21955f7dd8c919836f600ccf98b41531c24ec09c622149c")
    version("1.4.192", sha256="b5f370d7256cf816696a28acd282ed10bf8a05e09b814bf79d4527509846c977")
    version("1.4.191", sha256="9890adc66979647b131242e87ad1498b906c0dcc041d25fcb24ff304b86b4f98")

    build_directory = "h2"
