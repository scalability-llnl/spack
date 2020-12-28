# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path

import spack.build_environment
import spack.fetch_strategy
import spack.package_base
from spack.reporter import Reporter

__all__ = ['JUnit']


class JUnit(Reporter):
    """Generate reports of spec installations for JUnit."""

    def __init__(self, args):
        Reporter.__init__(self, args)
        self.template_file = os.path.join('reports', 'junit.xml')

    def build_report(self, filename, report_data):
        # Write the report
        with open(filename, 'w') as f:
            env = spack.tengine.make_environment()
            t = env.get_template(self.template_file)
            f.write(t.render(report_data))

    def test_report(self, filename, report_data):
        self.build_report(filename, report_data)
