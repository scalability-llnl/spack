# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    version("202308.02", sha256="adb553c72d5180f551aea77fb6626dea36f33f1968f3d0ab0bb00dc7af4f5b55")
    version("202308", sha256="13dc8d50577fe4767142c50f1a95772db95cd4b173c2b281cdcdd68a5af47cb0")
    version("202112.07", sha256="ea770483d3e70e9d157fe938096d5ea06e47166d57e0037cf66b6449c7fce2ab")
    version("202112.06", sha256="c6deefda1da814af9fafdeafe5d3b5da3c8698fb9ec17bd03ea32dbabaaca3e5")
    version("202112.05", sha256="77f2b7b727b68cfdb302faa914b202137dea87cff5e30ab121d3e42f55194dda")
    version("202112.04", sha256="36f76ea061bf72c102601717537804101162fa5ebf215061917eeedd128c4d78")
    version("202112.02", sha256="52ea6ab36d9836612eaa9657ddd6297aa43672eb6065534caba21f9a7845b67f")
    version("201808.07", sha256="7c9c12dc52770a0fbdf094ce058f43b601bbbf311c13b5fb56a6088ec1680824")
    version("201808.01", sha256="9f61aa600710d9110463430dcf49cbc03a14dcad5e5bac8717b7e41baaf86fff")

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
