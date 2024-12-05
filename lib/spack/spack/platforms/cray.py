# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path


def slingshot_network():
    return os.path.exists("/opt/cray/pe") and (
        os.path.exists("/lib64/libcxi.so") or os.path.exists("/usr/lib64/libcxi.so")
    )
