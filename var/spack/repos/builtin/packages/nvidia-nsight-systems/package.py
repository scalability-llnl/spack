# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (https://docs.nvidia.com/nsight-systems/CopyrightAndLicenses/index.html)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nvidia-nsight-systems
#
# You can edit this file again by typing:
#
#     spack edit nvidia-nsight-systems
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
from glob import glob
import shutil
import os


class NvidiaNsightSystems(Package):
    """NVIDIA Nsight™ Systems is a system-wide performance analysis tool designed to visualize an application’s algorithms, identify the largest opportunities to optimize, and tune to scale efficiently across any quantity or size of CPUs and GPUs, from large servers to our smallest system on a chip (SoC)"""

    homepage = "https://developer.nvidia.com/nsight-systems"
    url = "https://developer.download.nvidia.com/devtools/repos/"
    maintainers("scothalverson")
    license("NVIDIA Software License Agreement")

    depends_on("libarchive programs='bsdtar'")
    version('2024.1.1', sha256='b67168897c30b8f7a2c5c2ff1b2bc2bf1a544d4a220bf6eb0db6af9835aefe07', url='https://developer.download.nvidia.com/devtools/repos/rhel8/arm64/nsight-systems-cli-2024.1.1-2024.1.1.59_3380207-0.aarch64.rpm', expand=False)

    def install(self, spec, prefix):
        bsdtar = which("bsdtar")
        rpm_file = glob(join_path(self.stage.source_path, "nsight-systems*.rpm"))[0]
        params = ['-x', '-f', rpm_file]
        ver = prefix.split("/")[-1].split("-")[-2]
        bsdtar(*params)
        params = ['-x', '-f', 'data.tar.gz']
        bsdtar(*params)
        for sd in ["/documentation", "/host-linux-armv8", "/target-linux-sbsa-armv8"]:
            shutil.copytree("opt/nvidia/nsight-systems/"+ver + sd, prefix + sd)
        os.mkdir(prefix + "/bin")
        os.symlink(prefix + "/host-linux-armv8/nsys-ui", prefix + "/bin/nsys-ui")
        os.symlink(prefix + "/target-linux-sbsa-armv8/nsys", prefix + "/bin/nsys")

        
