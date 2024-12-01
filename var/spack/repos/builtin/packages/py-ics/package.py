# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIcs(PythonPackage):
    """Ics.py : iCalendar for Humans

    Ics.py is a pythonic and easy iCalendar library. Its goals are to
    read and write ics data in a developer friendly way.

    iCalendar is a widely-used and useful format but not user friendly.
    Ics.py is there to give you the ability of creating and reading
    this format without any knowledge of it.

    It should be able to parse every calendar that respects the
    rfc5545 and maybe some more. It also outputs rfc compliant
    calendars.

    iCalendar (file extension .ics) is used by Google Calendar, Apple
    Calendar, Android and many more.

    Ics.py is available for Python>=3.6 and is Apache2 Licensed.
    """

    homepage = "https://github.com/C4ptainCrunch/ics.py"
    url = "https://github.com/C4ptainCrunch/ics.py/archive/v0.6.tar.gz"

    version("0.7", sha256="48c637e5eb8dfc817b1f3f6b3f662ba19cfcc25f8f71eb42f5d07e6f2c573994")
    version("0.6", sha256="4947263136202d0489d4f5e5c7175dfd2db5d3508b8b003ddeaef96347f68830")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-arrow@0.11:0.14", type=("build", "run"))
    depends_on("py-six@1.5:", type=("build", "run"))
    depends_on("py-tatsu@4.2:", type=("build", "run"), when="@0.6:")
