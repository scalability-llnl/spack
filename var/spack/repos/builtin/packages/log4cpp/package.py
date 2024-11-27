# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Log4cpp(AutotoolsPackage):
    """Log4cpp is library of C++ classes for flexible logging to
    files, syslog, IDSA and other destinations. It is modeled after
    the Log4j Java library, staying as close to their API as is
    reasonable."""

    homepage = "https://log4cpp.sourceforge.net/"
    url = "http://sourceforge.net/projects/log4cpp/files/log4cpp-1.1.3.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.1.3", sha256="2cbbea55a5d6895c9f0116a9a9ce3afb86df383cd05c9d6c1a4238e5e5c8f51d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
