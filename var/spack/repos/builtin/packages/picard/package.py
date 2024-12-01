# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os.path
import re

from spack.package import *


class Picard(Package):
    """Picard is a set of command line tools for manipulating high-throughput
    sequencing (HTS) data and formats such as SAM/BAM/CRAM and VCF.
    """

    homepage = "https://broadinstitute.github.io/picard/"
    url = "https://github.com/broadinstitute/picard/releases/download/2.26.2/picard.jar"
    _urlfmt = "https://github.com/broadinstitute/picard/releases/download/{0}/picard.jar"
    _oldurlfmt = (
        "https://github.com/broadinstitute/picard/releases/download/{0}/picard-tools-{0}.zip"
    )

    license("GPL-2.0-or-later")

    # They started distributing a single jar file at v2.6.0, prior to
    # that it was a .zip file with multiple .jar and .so files
    version(
        "3.1.1",
        sha256="15c79f51fd0ac001049f9dd7b9bac1dbdf759dcb0230a89c7f6d1f246e8bbab4",
        expand=False,
    )
    version(
        "3.0.0",
        sha256="0d5e28ab301fad3b02030d01923888129ba82c5f722ac5ccb2d418ab76ac5499",
        expand=False,
    )
    version(
        "2.26.2",
        sha256="99fab1699a735fd048a05975a243774f1cc99e87a9b28311d4aa872d06390474",
        expand=False,
    )
    version(
        "2.25.7",
        sha256="dc0e830d3e838dee2b4f4aa1c9631fb3a4c3ec982de8dfe5145fc748104c7146",
        expand=False,
    )
    version(
        "2.25.6",
        sha256="768709826514625381e6fa3920945360167f4e830bf72f79eb070da059676f02",
        expand=False,
    )
    version(
        "2.25.5",
        sha256="f7fa9784b84d384abfcbd77076f5ceab7b2797dc863ac35fd41470daa3efe3a5",
        expand=False,
    )
    version(
        "2.25.4",
        sha256="c3ac14471e48e28e24201ae5515f828ffa45db7ac3e37173251a672845b4a9b3",
        expand=False,
    )
    version(
        "2.25.3",
        sha256="1d4dbfcb36d23fde11f173ab0de8a99835e04161efb04f246bbcbfc0bee3b493",
        expand=False,
    )
    version(
        "2.25.2",
        sha256="aead4baf12028a5d2b9ef70e00c93e4bba8f6bece0b9a7104b89b842a8e0326f",
        expand=False,
    )
    version(
        "2.25.1",
        sha256="6d6e622d6b465f9fc704c37bcba55b0dac5ad14d07088bbdbdfade5cd027ee1c",
        expand=False,
    )
    version(
        "2.25.0",
        sha256="faf2434da84fe21b516d57817767920fdedfc19ebdc01d9cae8d6d3314f7e897",
        expand=False,
    )
    version(
        "2.24.0",
        sha256="70e91039bccc6f6db60f18c41713218a8cdf45f591f02c1012c062152b27cd7b",
        expand=False,
    )
    version(
        "2.20.8",
        sha256="aff92d618ee9e6bafc1ab4fbfa89fc557a0dbe596ae4b92fe3bf93ebf95c7105",
        expand=False,
    )
    version(
        "2.19.0",
        sha256="f97fc3f7a73b55cceea8b6a6488efcf1b2fbf8cad61d88645704ddd45a8c5950",
        expand=False,
    )
    version(
        "2.18.3",
        sha256="0e0fc45d9a822ee9fa562b3bb8f1525a439e4cd541429a1a4ca4646f37189b70",
        expand=False,
    )
    version(
        "2.18.0",
        sha256="c4c64b39ab47968e4afcaf1a30223445ee5082eab31a03eee240e54c2e9e1dce",
        expand=False,
    )
    version(
        "2.17.0",
        sha256="ffea8bf90e850919c0833e9dcc16847d40090a1ef733c583a710a3282b925998",
        expand=False,
    )
    version(
        "2.16.0",
        sha256="01cf3c930d2b4841960497491512d327bf669c1ed2e753152e1e651a27288c2d",
        expand=False,
    )
    version(
        "2.15.0",
        sha256="dc3ff74c704954a10796b390738078617bb0b0fef15731e9d268ed3b26c6a285",
        expand=False,
    )
    version(
        "2.13.2",
        sha256="db7749f649e8423053fb971e6af5fb8a9a1a797cb1f20fef1100edf9f82f6f94",
        expand=False,
    )
    version(
        "2.10.0",
        sha256="e256d5e43656b7d8be454201a7056dce543fe9cbeb30329a0d8c22d28e655775",
        expand=False,
    )
    version(
        "2.9.4",
        sha256="0ecee9272bd289d902cc18053010f0364d1696e7518ac92419a99b2f0a1cf689",
        expand=False,
    )
    version(
        "2.9.3",
        sha256="6cca26ce5094b25a82e1a8d646920d584c6db5f009476196dc285be6522e00ce",
        expand=False,
    )
    version(
        "2.9.2",
        sha256="05714b9743a7685a43c94a93f5d03aa4070d3ab6e20151801301916d3e546eb7",
        expand=False,
    )
    version(
        "2.9.0",
        sha256="9a57f6bd9086ea0f5f1a6d9d819459854cb883bb8093795c916538ed9dd5de64",
        expand=False,
    )
    version(
        "2.8.3",
        sha256="97a4b6c8927c8cb5f3450630c9b39bf210ced8c271f198119118ce1c24b8b0f6",
        expand=False,
    )
    version(
        "2.6.0",
        sha256="671d9e86e6bf0c28ee007aea55d07e2456ae3a57016491b50aab0fd2fd0e493b",
        expand=False,
    )
    version("1.140", sha256="0d27287217413db6b846284c617d502eaa578662dcb054a7017083eab9c54438")

    variant("parameters", default=False, description="get java parameters in the adapter script")

    depends_on("java@17:", type="run", when="@3.0.0:")
    depends_on("java@8:", type="run", when="@:2.27.5")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        # The list of files to install varies with release...
        # ... but skip the spack-build-{env}out.txt files.
        files = [x for x in glob.glob("*") if not re.match("^spack-", x)]
        for f in files:
            install(f, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.

        script_sh = join_path(
            os.path.dirname(__file__),
            "picard_with_parameters.sh" if "+parameters" in spec else "picard.sh",
        )

        script = prefix.bin.picard
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("picard.jar", join_path(prefix.bin, "picard.jar"), script, **kwargs)

    def setup_run_environment(self, env):
        """The Picard docs suggest setting this as a convenience."""
        env.prepend_path("PICARD", join_path(self.prefix.bin, "picard.jar"))

    def url_for_version(self, version):
        if version < Version("2.6.0"):
            return self._oldurlfmt.format(version)
        else:
            return self._urlfmt.format(version)
