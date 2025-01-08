# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from ._operating_system import OperatingSystem
from .freebsd import FreeBSDOs
from .linux_distro import LinuxDistro
from .mac_os import MacOs
from .windows_os import WindowsOs

__all__ = ["OperatingSystem", "LinuxDistro", "MacOs", "WindowsOs", "FreeBSDOs"]

#: List of all the Operating Systems known to Spack
operating_systems = [LinuxDistro, MacOs, WindowsOs, FreeBSDOs]
