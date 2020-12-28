# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

import spack.package_base
from spack.package import *


class FindExternals1(AutotoolsPackage):
    executables = ['find-externals1-exe']

    url = "http://www.example.com/find-externals-1.0.tar.gz"

    version('1.0', 'hash-1.0')

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        exe_to_path = dict(
            (os.path.basename(p), p) for p in exes_in_prefix
        )
        if 'find-externals1-exe' not in exe_to_path:
            return None

        exe = spack.util.executable.Executable(
            exe_to_path['find-externals1-exe'])
        output = exe('--version', output=str)
        if output:
            match = re.search(r'find-externals1.*version\s+(\S+)', output)
            if match:
                version_str = match.group(1)
                return Spec.from_detection(
                    'find-externals1@{0}'.format(version_str)
                )
