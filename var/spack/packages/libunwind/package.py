##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os.path

class Libunwind(Package):
    """A portable and efficient C programming interface (API) to determine
       the call-chain of a program."""
    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"

    version('1.1', 'fb4ea2f6fbbe45bf032cd36e586883ce')

    def detect_elf(self):
        """
            Determine whether the current system supports ELF,
            i.e. whether the file "elf.h" can be included
        """
        with working_dir('check-for-elf', create=True):
            with open('elf.c', 'w') as f:
                f.write("#include <elf.h>\n")
            with open('Makefile', 'w') as f:
                f.write("elf.o: elf.c; cc -c elf.c\n")
            try:
                make()
            except:
                pass
            return os.path.exists('elf.o')

    def install(self, spec, prefix):
        if not self.detect_elf():
            # libunwind requires an ELF system
            mkdirp(prefix.lib)
            return

        configure("--prefix=" + prefix)
        make()
        make("install")
