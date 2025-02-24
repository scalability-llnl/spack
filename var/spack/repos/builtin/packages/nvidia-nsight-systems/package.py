# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
import shutil
from glob import glob

from spack.package import *

# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()
_versions = {
    "2024.6.1": {
        "Linux-aarch64": (
            "24700c28dfda9f95d4e93de218b86ab1ba0ee8b74cb61c3c581767296159c75c",
            "https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2024_6/nsight-systems-2024.6.1-2024.6.1.90_3490548-0.aarch64.rpm",
        ),
        "Linux-x86_64": (
            "dd4359a47ff3857395c55a0da483b64f5c0c3a1a2e57dd543a512dc3d2cd2674",
            "https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2024_6/nsight-systems-2024.6.1-2024.6.1.90_3490548-0.x86_64.rpm",
        ),
    },
    "2024.1.1": {
        "Linux-aarch64": (
            "41dc15ae128ef1de8e582b66bb465ac6bd67b9d20ef77fc70528b735d80fb3ec",
            "https://developer.download.nvidia.com/devtools/repos/rhel8/arm64/nsight-systems-2024.1.1-2024.1.1.59_3380207-0.aarch64.rpm",
        ),
        "Linux-ppc64le": (
            "8c98b511df1747c4c782430504ae6fa4b3fce6fa72623083a828fc0a1e11f1b8",
            "https://developer.download.nvidia.com/devtools/repos/rhel8/ppc64le/nsight-systems-cli-2024.1.1-2024.1.1.59_3380207-0.ppc64le.rpm",
        ),
        "Linux-x86_64": (
            "96f57548e0bd69cb02cd1fe8c70ed4a650636ecb3a5ea5ec490c8049adc2beb5",
            "https://developer.download.nvidia.com/devtools/repos/rhel8/x86_64/nsight-systems-2024.1.1-2024.1.1.59_3380207-0.x86_64.rpm",
        ),
    },
}


class NvidiaNsightSystems(Package):
    """NVIDIA Nsight™ Systems is a system-wide performance analysis tool designed
    to visualize an application’s algorithms, identify the largest opportunities
    to optimize, and tune to scale efficiently across any quantity or size of CPUs
    and GPUs, from large servers to the smallest system on a chip"""

    homepage = "https://developer.nvidia.com/nsight-systems"
    url = "https://developer.download.nvidia.com/devtools/repos/"
    maintainers("scothalverson")
    license("NVIDIA Software License Agreement")

    executables = ["^nsys$"]

    # Used to unpack the source RPM archives.
    depends_on("libarchive programs='bsdtar'", type="build")

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # Example output:
        #     NVIDIA Nsight Systems version 2024.1.1.59-241133802077v0
        # but we only want to match 2024.1.1
        match = re.search(r"NVIDIA Nsight Systems version ((?:[0-9]+.){2}[0-9])", output)
        return match.group(1) if match else None

    def install(self, spec, prefix):
        bsdtar = which("bsdtar")
        rpm_file = glob(join_path(self.stage.source_path, "nsight-systems*.rpm"))[0]
        params = ["-x", "-f", rpm_file]
        ver = prefix.split("/")[-1].split("-")[-2]
        bsdtar(*params)

        arch = self.spec.target.family
        if arch == "aarch64":
            folders = ["documentation", "host-linux-armv8", "target-linux-sbsa-armv8"]
        elif arch == "ppc64le":
            folders = ["documentation", "host-linux-ppc64le", "target-linux-ppc64le"]
        elif arch == "x86_64":
            folders = ["documentation", "host-linux-x64", "target-linux-x64"]
        if os.path.exists(join_path("opt", "nvidia", "nsight-systems-cli")):
            base_path = join_path("opt", "nvidia", "nsight-systems-cli")
        elif os.path.exists(join_path("opt", "nvidia", "nsight-systems")):
            base_path = join_path("opt", "nvidia", "nsight-systems")
        else:
            raise InstallError("Couldn't determine subdirectories to install.")

        for sd in folders:
            shutil.copytree(join_path(base_path, ver, sd), join_path(prefix, sd))
        os.mkdir(join_path(prefix, "bin"))
        if arch == "aarch64":
            os.symlink(
                join_path(prefix, "host-linux-armv8", "nsys-ui"),
                join_path(prefix, "bin", "nsys-ui"),
            )
            os.symlink(
                join_path(prefix, "target-linux-sbsa-armv8", "nsys"),
                join_path(prefix, "bin", "nsys"),
            )
        elif arch == "ppc64le":
            # `nsys-ui` is missing in the PowerPC version of the package.
            os.symlink(
                join_path(prefix, "target-linux-ppc64le", "nsys"), join_path(prefix, "bin", "nsys")
            )
        elif arch == "x86_64":
            os.symlink(
                join_path(prefix, "host-linux-x64", "nsys-ui"), join_path(prefix, "bin", "nsys-ui")
            )
            os.symlink(
                join_path(prefix, "target-linux-x64", "nsys"), join_path(prefix, "bin", "nsys")
            )
