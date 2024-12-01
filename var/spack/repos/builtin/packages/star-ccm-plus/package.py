# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re

from spack.package import *


class StarCcmPlus(Package):
    """STAR-CCM+ (Computational Continuum Mechanics) CFD solver."""

    homepage = "https://mdx.plm.automation.siemens.com/star-ccm-plus"
    manual_download = True

    def url_for_version(self, version):
        url = "{pwd}/STAR-CCM+{version}_linux-x86_64.tar.gz".format(
            pwd=os.getcwd(), version=version
        )
        return url

    version(
        "17.02.007_01", sha256="79c0859b84f753d9c690aad60b6252677a8625224148fb698aa6a94aa2a09a8c"
    )
    version(
        "16.06.008_01", sha256="64577ec0e9a98d971114e68c4eec05bb746e061dfbf77b8d8919583c796c9e4b"
    )
    version("11.06.010_02", md5="d349c6ac8293d8e6e7a53533d695588f")

    variant("doc", default=False, description="Install the documentation")

    # Licensing
    license_required = True
    license_vars = ["CDLMD_LICENSE_FILE", "LM_LICENSE_FILE"]

    def install(self, spec, prefix):
        # There is a known issue with the LaunchAnywhere application.
        # Specifically, it cannot handle long prompts or prompts
        # containing special characters and backslashes. It results in
        # the following error message:
        #
        # An internal LaunchAnywhere application error has occured and this
        # application cannot proceed. (LAX)
        #
        # Stack Trace:
        #     java.lang.IllegalArgumentException: Malformed \uxxxx encoding.
        #     at java.util.Properties.loadConvert(Unknown Source)
        #     at java.util.Properties.load0(Unknown Source)
        #     at java.util.Properties.load(Unknown Source)
        #     at com.zerog.common.java.util.PropertiesUtil.loadProperties(
        #         Unknown Source)
        #     at com.zerog.lax.LAX.<init>(Unknown Source)
        #     at com.zerog.lax.LAX.main(Unknown Source)
        #
        # https://www.maplesoft.com/support/faqs/detail.aspx?sid=35272
        env["PS1"] = ">"
        env["PROMPT_COMMAND"] = ""

        if "@:12" in spec:
            file_pattern = "*.bin"
        else:
            file_pattern = "*.sh"

        installer = Executable(join_path(self.stage.source_path, glob.glob(file_pattern)[0]))

        installer(
            "-i",
            "silent",
            "-DINSTALLDIR={0}".format(prefix),
            "-DINSTALLFLEX=false",
            "-DADDSYSTEMPATH=false",
            "-DCOMPUTE_NODE=false",
            "-DNODOC={0}".format("false" if "+docs" in spec else "true"),
        )

    def setup_run_environment(self, env):
        # using Version.up_to strips out the 0 padding
        version = re.sub("_.*$", "", format(self.spec.version))
        env.prepend_path(
            "PATH", join_path(self.prefix, version, "STAR-View+{0}".format(version), "bin")
        )
        env.prepend_path(
            "PATH", join_path(self.prefix, version, "STAR-CCM+{0}".format(version), "star", "bin")
        )
