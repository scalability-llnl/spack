# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SentieonGenomics(Package):
    """Sentieon provides complete solutions for secondary DNA analysis.
    Our software improves upon BWA, GATK, Mutect, and Mutect2 based pipelines.
    The Sentieon tools are deployable on any CPU-based computing system.

    Use of this software is subject to the EULA at:
    https://www.sentieon.com/EULA/eula-aws.html

    Please set the path to the sentieon license server with:

    export SENTIEON_LICENSE=<FQDN>:<PORT>
    """

    homepage = "https://www.sentieon.com/"
    # url is from the permalink documented in dockerfile at
    # https://github.com/Sentieon/sentieon-docker/blob/master/Dockerfile
    # See also: https://github.com/spack/spack/pull/30145/files#r853275635
    url = "https://s3.amazonaws.com/sentieon-release/software/sentieon-genomics-201808.01.tar.gz"
    maintainers("snehring")

    version("202308.02", sha256="a04b98c1b7c4e8916fdc45f15685d5fd83db56386ec2478eb5ea594170405bd5")
    version("202308", sha256="d663067f46e499c23819e344cf548fdc362abbf94d3ef086a2e655c072ebe0d6")
    version("202112.07", sha256="7178769bb5a9619840996356bda4660410fb6f228b2c0b86611bcb1c6bcfc2e1")
    version("202112.06", sha256="18306036f01c3d41dd7ae738b18ae76fd6b666f1172dd4696cd55b4a8465270d")
    version("202112.05", sha256="c97b14b0484a0c0025115ad7b911453af7bdcd09874c26cbc39fd0bc5588a306")
    version("202112.04", sha256="154732dc752476d984908e78b1fc5120d4f23028ee165cc4a451ecc1df0e0246")
    version("202112.02", sha256="033943df7958550fd42b410d34ae91a8956a905fc90ca8baa93d2830f918872c")
    version("201808.07", sha256="fb66b18a7b99e44968eb2c3a6a5b761d6b1e70fba9f7dfc4e5db3a74ab3d3dd9")
    version("201808.01", sha256="6d77bcd5a35539549b28eccae07b19a3b353d027720536e68f46dcf4b980d5f7")

    # Licensing.
    license_require = True
    license_vars = ["SENTIEON_LICENSE"]

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("doc", prefix.doc)
        install_tree("etc", prefix.etc)
        install_tree("lib", prefix.lib)
        install_tree("libexec", prefix.libexec)
        install_tree("share", prefix.share)
