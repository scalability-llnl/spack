# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import multiprocessing
import os


def cpus_available():
    """
    Returns the number of CPUs available for the current process, or the number
    of phyiscal CPUs when that information cannot be retrieved. The number
    of available CPUs might differ from the number of physical CPUs when
    using spack through Slurm or container runtimes.
    """
    try:
        return len(os.sched_getaffinity(0))  # novermin
    except Exception:
        return multiprocessing.cpu_count()
