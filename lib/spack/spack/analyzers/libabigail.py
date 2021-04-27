# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack
import spack.error
import spack.bootstrap
import spack.hooks
import spack.monitor
import spack.binary_distribution
import spack.package
import spack.repo

import llnl.util.tty as tty

from .analyzer_base import AnalyzerBase

import os


class Libabigail(AnalyzerBase):

    name = "libabigail"
    outfile = "spack-analyzer-libabigail.json"
    description = "Application Binary Interface (ABI) features for objects"

    def __init__(self, spec, dirname=None):
        """
        init for an analyzer ensures we have all needed dependencies.

        For the libabigail analyzer, this means Libabigail.
        Since the output for libabigail is one file per object, we communicate
        with the monitor multiple times.
        """
        super(Libabigail, self).__init__(spec, dirname)

        # This doesn't seem to work to import on the module level
        tty.debug("Preparing to use Libabigail, will install if missing.")

        with spack.bootstrap.ensure_bootstrap_configuration():

            # libabigail won't install lib/bin/share without docs
            spec = spack.spec.Spec("libabigail+docs")
            spec.concretize()

            self.abidw = spack.bootstrap.get_executable(
                "abidw", spec=spec, install=True)

    def run(self):
        """
        Run libabigail, and save results to filename.

        This run function differs in that we write as we generate and then
        return a dict with the analyzer name as the key, and the value of a
        dict of results, where the key is the object name, and the value is
        the output file written to.
        """
        manifest = spack.binary_distribution.get_buildfile_manifest(self.spec)

        # This result will store a path to each file
        result = {}

        # Generate an output file for each binary or object
        for obj in manifest.get("binary_to_relocate_fullpath", []):

            # We want to preserve the path in the install directory in case
            # a library has an equivalenly named lib or executable, for example
            outdir = os.path.dirname(obj.replace(self.spec.package.prefix,
                                     '').strip(os.path.sep))
            outfile = "spack-analyzer-libabigail-%s.xml" % os.path.basename(obj)
            outfile = os.path.join(self.output_dir, outdir, outfile)
            outdir = os.path.dirname(outfile)

            # Create the output directory
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            # Sometimes libabigail segfaults and dumps
            try:
                self.abidw(obj, "--out-file", outfile)
                result[obj] = outfile
                tty.info("Writing result to %s" % outfile)
            except spack.error.SpackError:
                tty.warn("Issue running abidw for %s" % obj)

        return {self.name: result}

    def save_result(self, result, overwrite=False):
        """
        Read saved ABI results and upload to monitor server.

        ABI results are saved to individual files, so each one needs to be
        read and uploaded. Result here should be the lookup generated in run(),
        the key is the analyzer name, and each value is the result file.
        We currently upload the entire xml as text because libabigail can't
        easily read gzipped xml, but this will be updated when it can.
        """
        if not spack.monitor.cli:
            return

        name = self.spec.package.name

        for obj, filename in result.get(self.name, {}).items():

            # Don't include the prefix
            rel_path = obj.replace(self.spec.prefix + os.path.sep, "")

            # We've already saved the results to file during run
            content = spack.monitor.read_file(filename)

            # A result needs an analyzer, value or binary_value, and name
            data = {"value": content, "install_file": rel_path, "name": "abidw-xml"}
            tty.info("Sending result for %s %s to monitor." % (name, rel_path))
            spack.hooks.on_analyzer_save(self.spec.package, {"libabigail": [data]})
