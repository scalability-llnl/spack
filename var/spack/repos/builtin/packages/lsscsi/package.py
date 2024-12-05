# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lsscsi(AutotoolsPackage):
    """Uses information provided by the sysfs pseudo file system in Linux
    kernel 2.6 series to list SCSI devices or all SCSI hosts. Includes a
    'classic'option to mimic the output of 'cat /proc/scsi/scsi' that has
    been widely used prior to the lk 2.6 series."""

    homepage = "https://sg.danny.cz/scsi/lsscsi.html"
    url = "https://sg.danny.cz/scsi/lsscsi-0.31.tgz"

    license("GPL-2.0-or-later")

    version("0.32", sha256="0a800e9e94dca2ab702d65d72777ae8cae078e3d74d0bcbed64ba0849e8029a1")
    version("0.31", sha256="12bf1973014803c6fd6d547e7594a4c049f0eef3bf5d22190d4be29d7c09f3ca")
    version("0.30", sha256="619a2187405f02c5f57682f3478bffc75326803cd08839e39d434250c5518b15")

    depends_on("c", type="build")  # generated
