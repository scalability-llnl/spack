##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class PerlUriEscape(PerlPackage):
    """This module provides functions to percent-encode and percent-decode URI
    strings as defined by RFC 3986. Percent-encoding URI's is informally called
    "URI escaping". This is the terminology used by this module, which predates
    the formalization of the terms by the RFC by several years."""

    homepage = "https://metacpan.org/pod/URI::Escape"
    url      = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-1.71.tar.gz"

    version('1.71', '247c3da29a794f72730e01aa5a715daf')

    depends_on('perl-extutils-makemaker', type='build')
