# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParallelly(RPackage):
    """Enhancing the 'parallel' Package.

    Utility functions that enhance the 'parallel' package and support the
    built-in parallel backends of the 'future' package. For example,
    availableCores() gives the number of CPU cores available to your R process
    as given by the operating system, 'cgroups' and Linux containers, R
    options, and environment variables, including those set by job schedulers
    on high-performance compute clusters. If none is set, it will fall back to
    parallel::detectCores(). Another example is makeClusterPSOCK(), which is
    backward compatible with parallel::makePSOCKcluster() while doing a better
    job in setting up remote cluster workers without the need for configuring
    the firewall to do port-forwarding to your local computer."""

    cran = "parallelly"

    license("LGPL-2.1-or-later")

    version("1.38.0", sha256="632c823c64d1bb840b2a5ff2cb2f5ffc743d62d5090a3cde55a2ebdde230d1aa")
    version("1.35.0", sha256="3f5e9b6507196aab052c5e67f8b524b75aa356731c5eaffbadde76c967ad5dcd")
    version("1.32.1", sha256="31c685f59ac7ff702fe2720910780378113adf0df0baf048a62eef94524cca90")
    version("1.31.1", sha256="40c7fc3d842fa928448e574091a521bead2367bf97545c744ca78ea9af3117da")
    version("1.30.0", sha256="aab080cb709bab232b2d808053efb2391eeb30a2de9497cbe474c99df89f9f3b")
    version("1.28.1", sha256="f4ae883b18409adb83c561ed69427e740e1b50bf85ef57f48c3f2edf837cc663")
    version("1.23.0", sha256="376ce2381587380a4da60f9563710d63084a605f93aa364e9349f2523e83bc08")
