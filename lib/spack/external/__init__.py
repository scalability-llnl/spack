##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
"""
This module contains external, potentially separately licensed,
packages that are included in spack.

So far:
    argparse:    We include our own version to be Python 2.6 compatible.

    distro:      Provides a more stable linux distribution detection.

    functools:   Used for implementation of total_ordering.

    graphterm:   Used for interactive ASCII node-link diagrams.

    jsonschema:  An implementation of JSON Schema for Python.

    ordereddict: We include our own version to be Python 2.6 compatible.

    py:          Needed by pytest.  Library with cross-python path,
                 ini-parsing, io, code, and log facilities.

    pyqver2:     External script to query required python version of
                 python source code. Used for ensuring 2.6 compatibility.

    pytest:      Testing framework used by Spack.

    yaml:        Used for config files.
"""
