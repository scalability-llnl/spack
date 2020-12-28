# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class StarCcmPlus(Package):
    """STAR-CCM+ (Computational Continuum Mechanics) CFD solver."""

    homepage = "http://mdx.plm.automation.siemens.com/star-ccm-plus"
    url      = "file://{0}/STAR-CCM+11.06.010_02_linux-x86_64.tar.gz".format(os.getcwd())
    manual_download = True

    version('11.06.010_02', 'd349c6ac8293d8e6e7a53533d695588f')

    variant('doc', default=False, description='Install the documentation')

    # Licensing
    license_required = True
    license_vars = ['CDLMD_LICENSE_FILE', 'LM_LICENSE_FILE']

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
        env['PS1'] = '>'
        env['PROMPT_COMMAND'] = ''

        installer = Executable(glob.glob('*.bin')[0])

        installer(
            '-i', 'silent',
            '-DINSTALLDIR={0}'.format(prefix),
            '-DINSTALLFLEX=false',
            '-DADDSYSTEMPATH=false',
            '-DNODOC={0}'.format('false' if '+docs' in spec else 'true')
        )
