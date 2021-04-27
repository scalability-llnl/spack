# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""An analyzer base provides basic functions to run the analysis, save results,
and (optionally) interact with a Spack Monitor
"""

import spack.monitor
import spack.hooks
import llnl.util.tty as tty
import spack.util.path
import spack.config

import os


def get_analyzer_dir(spec, analyzer_dir=None):
    """
    Given a spec, return the directory to save analyzer results.

    We create the directory if it does not exist. We also check that the
    spec has an associated package. An analyzer cannot be run if the spec isn't
    associated with a package. If the user provides a custom analyzer_dir,
    we use it over checking the config and the default at ~/.spack/analyzers
    """
    # An analyzer cannot be run if the spec isn't associated with a package
    if not hasattr(spec, "package") or not spec.package:
        tty.die("A spec can only be analyzed with an associated package.")

    # The top level directory is in the user home, or a custom location
    if not analyzer_dir:
        analyzer_dir = spack.util.path.canonicalize_path(
            spack.config.get('config:analyzers_dir', '~/.spack/analyzers'))

    # We follow the same convention as the spec install (this could be better)
    package_prefix = os.sep.join(spec.package.prefix.split('/')[-3:])
    meta_dir = os.path.join(analyzer_dir, package_prefix)
    return meta_dir


class AnalyzerBase(object):

    def __init__(self, spec, dirname=None):
        """
        Verify that the analyzer has correct metadata.

        An Analyzer is intended to run on one spec install, so the spec
        with its associated package is required on init. The child analyzer
        class should define an init function that super's the init here, and
        also check that the analyzer has all dependencies that it
        needs. If an analyzer subclass does not have dependencies, it does not
        need to define an init. An Analyzer should not be allowed to proceed
        if one or more dependencies are missing. The dirname, if defined,
        is an optional directory name to save to (instead of the default meta
        spack directory).
        """
        self.spec = spec
        self.dirname = dirname
        self.meta_dir = os.path.dirname(spec.package.install_log_path)

        for required in ["name", "outfile", "description"]:
            if not hasattr(self, required):
                tty.die("Please add a %s attribute on the analyzer." % required)

    def run(self):
        """
        Given a spec with an installed package, run the analyzer on it.
        """
        raise NotImplementedError

    @property
    def output_dir(self):
        """
        The full path to the output directory.

        This includes the nested analyzer directory structure. This function
        does not create anything.
        """
        if not hasattr(self, "_output_dir"):
            output_dir = get_analyzer_dir(self.spec, self.dirname)
            self._output_dir = os.path.join(output_dir, self.name)

        return self._output_dir

    def save_result(self, result, overwrite=False):
        """
        Save a result to the associated spack monitor, if defined.

        This function is on the level of the analyzer because it might be
        the case that the result is large (appropriate for a single request)
        or that the data is organized differently (e.g., more than one
        request per result). If an analyzer subclass needs to over-write
        this function with a custom save, that is appropriate to do (see abi).
        """
        # We maintain the structure in json with the analyzer as key so
        # that in the future, we could upload to a monitor server
        if result[self.name]:

            outfile = os.path.join(self.output_dir, self.outfile)

            # Only try to create the results directory if we have a result
            if not os.path.exists(self._output_dir):
                os.makedirs(self._output_dir)

            # Don't overwrite an existing result if overwrite is False
            if os.path.exists(outfile) and not overwrite:
                tty.info("%s exists and overwrite is False, skipping." % outfile)
            else:
                tty.info("Writing result to %s" % outfile)
                spack.monitor.write_json(result[self.name], outfile)

        # This hook runs after a save result
        spack.hooks.on_analyzer_save(self.spec.package, result)
