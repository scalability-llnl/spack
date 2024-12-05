# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import pathlib
import platform
import subprocess

from llnl.util import tty

from spack.error import SpackError
from spack.util import windows_registry as winreg
from spack.version import Version

from ._operating_system import OperatingSystem


def windows_version():
    """Windows version as a Version object"""
    # include the build number as this provides important information
    # for low lever packages and components like the SDK and WDK
    # The build number is the version component that would otherwise
    # be the patch version in sematic versioning, i.e. z of x.y.z
    return Version(platform.version())


class WindowsOs(OperatingSystem):
    """This class represents the Windows operating system.  This will be
    auto detected using the python platform.win32_ver() once we have a
    python setup that runs natively.  The Windows platform will be
    represented using the major version operating system number, e.g.
    10.
    """

    def __init__(self):
        plat_ver = windows_version()
        if plat_ver < Version("10"):
            raise SpackError("Spack is not supported on Windows versions older than 10")
        super().__init__("windows{}".format(plat_ver), plat_ver)

    def __str__(self):
        return self.name

    @property
    def vs_install_paths(self):
        vs_install_paths = []
        root = os.environ.get("ProgramFiles(x86)") or os.environ.get("ProgramFiles")
        if root:
            try:
                extra_args = {"encoding": "mbcs", "errors": "strict"}
                paths = subprocess.check_output(  # type: ignore[call-overload] # novermin
                    [
                        os.path.join(root, "Microsoft Visual Studio", "Installer", "vswhere.exe"),
                        "-prerelease",
                        "-requires",
                        "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                        "-property",
                        "installationPath",
                        "-products",
                        "*",
                    ],
                    **extra_args,
                ).strip()
                vs_install_paths = paths.split("\n")
            except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
                pass
        return vs_install_paths

    @property
    def msvc_paths(self):
        return [os.path.join(path, "VC", "Tools", "MSVC") for path in self.vs_install_paths]

    @property
    def oneapi_root(self):
        root = os.environ.get("ONEAPI_ROOT", "") or os.path.join(
            os.environ.get("ProgramFiles(x86)", ""), "Intel", "oneAPI"
        )
        if os.path.exists(root):
            return root

    @property
    def compiler_search_paths(self):
        # First Strategy: Find MSVC directories using vswhere
        _compiler_search_paths = []
        for p in self.msvc_paths:
            _compiler_search_paths.extend(glob.glob(os.path.join(p, "*", "bin", "Hostx64", "x64")))
        oneapi_root = self.oneapi_root
        if oneapi_root:
            _compiler_search_paths.extend(
                glob.glob(os.path.join(oneapi_root, "compiler", "**", "bin"), recursive=True)
            )

        # Second strategy: Find MSVC via the registry
        def try_query_registry(retry=False):
            winreg_report_error = lambda e: tty.debug(
                'Windows registry query on "SOFTWARE\\WOW6432Node\\Microsoft"'
                f"under HKEY_LOCAL_MACHINE: {str(e)}"
            )
            try:
                # Registry interactions are subject to race conditions, etc and can generally
                # be flakey, do this in a catch block to prevent reg issues from interfering
                # with compiler detection
                msft = winreg.WindowsRegistryView(
                    "SOFTWARE\\WOW6432Node\\Microsoft", winreg.HKEY.HKEY_LOCAL_MACHINE
                )
                return msft.find_subkeys(r"VisualStudio_.*", recursive=False)
            except OSError as e:
                # OSErrors propagated into caller by Spack's registry module are expected
                # and indicate a known issue with the registry query
                # i.e. user does not have permissions or the key/value
                # doesn't exist
                winreg_report_error(e)
                return []
            except winreg.InvalidRegistryOperation as e:
                # Other errors raised by the Spack's reg module indicate
                # an unexpected error type, and are handled specifically
                # as the underlying cause is difficult/impossible to determine
                # without manually exploring the registry
                # These errors can also be spurious (race conditions)
                # and may resolve on re-execution of the query
                # or are permanent (specific types of permission issues)
                # but the registry raises the same exception for all types of
                # atypical errors
                if retry:
                    winreg_report_error(e)
                return []

        vs_entries = try_query_registry()
        if not vs_entries:
            # Occasional spurious race conditions can arise when reading the MS reg
            # typically these race conditions resolve immediately and we can safely
            # retry the reg query without waiting
            # Note: Winreg does not support locking
            vs_entries = try_query_registry(retry=True)

        vs_paths = []

        def clean_vs_path(path):
            path = path.split(",")[0].lstrip("@")
            return str((pathlib.Path(path).parent / "..\\..").resolve())

        for entry in vs_entries:
            try:
                val = entry.get_subkey("Capabilities").get_value("ApplicationDescription").value
                vs_paths.append(clean_vs_path(val))
            except FileNotFoundError as e:
                if hasattr(e, "winerror") and e.winerror == 2:
                    pass
                else:
                    raise

        _compiler_search_paths.extend(vs_paths)
        return _compiler_search_paths
