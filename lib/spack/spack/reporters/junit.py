# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

import spack.tengine

from .base import Reporter


class JUnit(Reporter):
    """Generate reports of spec installations for JUnit."""

    _jinja_template = "reports/junit.xml"

    def concretization_report(self, filename, msg):
        pass

    def build_report(self, filename, specs):
        if not (os.path.splitext(filename))[1]:
            # Ensure the report name will end with the proper extension;
            # otherwise, it currently defaults to the "directory" name.
            filename = filename + ".xml"

        report_data = {"specs": specs}
        with open(filename, "w") as f:
            env = spack.tengine.make_environment()
            t = env.get_template(self._jinja_template)
            f.write(t.render(report_data))

    def test_report(self, filename, specs):
        self.build_report(filename, specs)
