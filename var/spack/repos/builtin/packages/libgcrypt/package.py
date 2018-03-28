##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Libgcrypt(AutotoolsPackage):
    """Libgcrypt is a general purpose cryptographic library based on
       the code from GnuPG. It provides functions for all cryptographic
       building blocks: symmetric ciphers, hash algorithms, MACs, public
       key algorithms, large integer functions, random numbers and a lot
       of supporting functions. """
    homepage = "http://www.gnu.org/software/libgcrypt/"
    url = "https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-1.8.1.tar.bz2"

    version('1.8.1', 'b21817f9d850064d2177285f1073ec55')
    version('1.7.6', '54e180679a7ae4d090f8689ca32b654c')
    version('1.6.2', 'b54395a93cb1e57619943c082da09d5f')

    variant("shared", default=True, description="Enable shared libs")

    depends_on("libgpg-error")

    def configure_args(self):
        if "+shared" in self.spec:
            return ["--enable-shared"]
        return ["--disable-shared"]
