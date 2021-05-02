# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
from spack.architecture import OperatingSystem


class LinuxDistro(OperatingSystem):
    """ This class will represent the autodetected operating system
        for a Linux System. Since there are many different flavors of
        Linux, this class will attempt to encompass them all through
        autodetection using the python module platform and the method
        platform.dist()
    """

    def __init__(self):
        try:
            # This will throw an error if imported on a non-Linux platform.
            from external.distro import linux_distribution
            distname, version, _ = linux_distribution(
                full_distribution_name=False)
            distname, version = str(distname), str(version)
        except ImportError:
            distname, version = 'unknown', ''

        # Grabs major version from tuple on redhat; on other platforms
        # grab the first legal identifier in the version field.  On
        # debian you get things like 'wheezy/sid'; sid means unstable.
        # We just record 'wheezy' and don't get quite so detailed.
        version = re.split(r'[^\w-]', version)

        if 'ubuntu' in distname:
            version = '.'.join(version[0:2])
        # openSUSE Tumbleweed is a rolling release which can change
        # more than once in a week, so set version to tumbleweed
        elif 'opensuse-tumbleweed' in distname:
            distname = 'opensuse'
            version = 'tumbleweed'
        else:
            version = version[0]

        super(LinuxDistro, self).__init__(distname, version)
