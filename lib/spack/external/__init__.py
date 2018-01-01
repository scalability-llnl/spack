##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
"""This module contains the following external, potentially separately
licensed, packages that are included in Spack:

argparse
--------

* Homepage: https://pypi.python.org/pypi/argparse
* Usage: We include our own version to be Python 2.6 compatible.
* Version: 1.4.0
* Note: This package has been slightly modified to improve
  error message formatting. See the following commit if the
  vendored copy ever needs to be updated again:
  https://github.com/spack/spack/pull/6786/commits/dfcef577b77249106ea4e4c69a6cd9e64fa6c418

ctest_log_parser
----------------

* Homepage: ???
* Usage: Functions to parse build logs and extract error messages.
* Version: ???

distro
------

* Homepage: https://pypi.python.org/pypi/distro
* Usage: Provides a more stable linux distribution detection.
* Version: 1.0.4 (last version supporting Python 2.6)

functools
---------

* Homepage: ???
* Usage: Used for implementation of total_ordering.
* Version: ???

jinja2
------

* Homepage: https://pypi.python.org/pypi/Jinja2
* Usage: A modern and designer-friendly templating language for Python.
* Version: 2.10

jsonschema
----------

* Homepage: https://pypi.python.org/pypi/jsonschema
* Usage: An implementation of JSON Schema for Python.
* Version: 2.5.1 (last version supporting Python 2.6)

markupsafe
----------

* Homepage: https://pypi.python.org/pypi/MarkupSafe
* Usage: Implements a XML/HTML/XHTML Markup safe string for Python.
* Version: 1.0

orderddict
----------

* Homepage: ???
* Usage: We include our own version to be Python 2.6 compatible.
* Version: ???

py
--

* Homepage: https://pypi.python.org/pypi/py
* Usage: Needed by pytest. Library with cross-python path,
  ini-parsing, io, code, and log facilities.
* Version: 1.4.34 (last version supporting Python 2.6)

pyqver2
-------

* Homepage: https://github.com/ghewgill/pyqver
* Usage: External script to query required python version of
  python source code. Used for ensuring 2.6 compatibility.
* Version: unversioned

pytest
------

* Homepage: https://pypi.python.org/pypi/pytest
* Usage: Testing framework used by Spack.
* Version: 3.2.5 (last version supporting Python 2.6)

pyyaml
------

* Homepage: https://pypi.python.org/pypi/PyYAML
* Usage: Used for config files.
* Version: 3.12

six
---

* Homepage: https://pypi.python.org/pypi/six
* Usage: Python 2 and 3 compatibility utilities.
* Version: 1.11.0
"""
