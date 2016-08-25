##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Qthreads(Package):
    """The qthreads API is designed to make using large numbers of
       threads convenient and easy, and to allow portable access to
       threading constructs used in massively parallel shared memory
       environments. The API maps well to both MTA-style threading and
       PIM-style threading, and we provide an implementation of this
       interface in both a standard SMP context as well as the SST
       context. The qthreads API provides access to full/empty-bit
       (FEB) semantics, where every word of memory can be marked
       either full or empty, and a thread can wait for any word to
       attain either state."""
    homepage = "http://www.cs.sandia.gov/qthreads/"

    # Google Code has stopped serving tarballs
    # We assume the tarballs will soon be available on Github instead
    # url = "https://qthreads.googlecode.com/files/qthread-1.10.tar.bz2"
    # version('1.10', '5af8c8bbe88c2a6d45361643780d1671')

    # Temporarily install from a git branch
    url = "https://github.com/Qthreads/qthreads"
    version("1.10",
            git="https://github.com/Qthreads/qthreads",
            branch="release-1.10")

    # patch("ldflags.patch")
    patch("restrict.patch")
    patch("trap.patch")

    depends_on("autoconf", type="build")
    depends_on("hwloc")

    def install(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()
        configure("--prefix=%s" % prefix,
                  "--enable-guard-pages",
                  "--with-topology=hwloc",
                  "--with-hwloc=%s" % spec["hwloc"].prefix)
        make()
        make("install")
