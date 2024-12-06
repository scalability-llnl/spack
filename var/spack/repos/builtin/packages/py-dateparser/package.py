# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDateparser(PythonPackage):
    """dateparser -- python parser for human readable dates"""

    homepage = "https://github.com/scrapinghub/dateparser"
    pypi = "dateparser/dateparser-0.7.2.tar.gz"

    license("BSD-3-Clause")

    version("0.7.2", sha256="e1eac8ef28de69a554d5fcdb60b172d526d61924b1a40afbbb08df459a36006b")

    variant("calendars", default=True, description="Add calendar libraries")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil@2.7.5:", type=("build", "run"))
    depends_on("py-pytz", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-tzlocal", type=("build", "run"))
    depends_on("py-umalqurra", type=("build", "run"), when="+calendars")
    depends_on("py-ruamel-yaml", type=("build", "run"), when="+calendars")
    depends_on("py-convertdate", type=("build", "run"), when="+calendars")
    depends_on("py-jdatetime", type=("build", "run"), when="+calendars")
