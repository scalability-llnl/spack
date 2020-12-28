# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lsscsi(AutotoolsPackage):
    """Uses information provided by the sysfs pseudo file system in Linux
    kernel 2.6 series to list SCSI devices or all SCSI hosts. Includes a
    'classic'option to mimic the output of 'cat /proc/scsi/scsi' that has
    been widely used prior to the lk 2.6 series."""

    homepage = "http://sg.danny.cz/scsi/lsscsi.html"
    url      = "http://sg.danny.cz/scsi/lsscsi-0.31.tgz"

    version('0.31',     sha256='12bf1973014803c6fd6d547e7594a4c049f0eef3bf5d22190d4be29d7c09f3ca')
    version('0.30',     sha256='619a2187405f02c5f57682f3478bffc75326803cd08839e39d434250c5518b15')
