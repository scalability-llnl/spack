# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyReportlab(PythonPackage):
    """The ReportLab Toolkit. An Open Source Python library for generating
    PDFs and graphics."""

    pypi = "reportlab/reportlab-3.4.0.tar.gz"

    version('3.4.0', sha256='5beaf35e59dfd5ebd814fdefd76908292e818c982bd7332b5d347dfd2f01c343')

    # py-reportlab provides binaries that duplicate those of other packages,
    # thus interfering with activation.
    # - easy_install, provided by py-setuptools
    # - pip, provided by py-pip
    extends('python', ignore=r'bin/.*')
