# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path


def slingshot_network():
    return os.path.exists("/opt/cray/pe") and (
        os.path.exists("/lib64/libcxi.so") or os.path.exists("/usr/lib64/libcxi.so")
    )
