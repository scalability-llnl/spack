# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty
import spack.monitor


def on_install_start(spec):
    """On start of an install, we want to ping the server if it exists
    """
    if not spack.monitor.cli:
        return

    tty.debug("Running on_install_start for %s" % spec)
    build_id = spack.monitor.cli.new_build(spec)
    tty.verbose("Build created with id %s" % build_id)


def on_install_success(spec):
    """On the success of an install (after everything is complete)
    """
    if not spack.monitor.cli:
        return

    tty.debug("Running on_install_success for %s" % spec)
    result = spack.monitor.cli.update_build(spec, status="SUCCESS")
    tty.verbose(result.get('message'))


def on_install_failure(spec):
    """Triggered on failure of an install
    """
    if not spack.monitor.cli:
        return

    tty.debug("Running on_install_failure for %s" % spec)
    result = spack.monitor.cli.fail_task(spec)
    tty.verbose(result.get('message'))


def on_phase_success(pkg, phase_name, log_file):
    """Triggered on a phase success
    """
    if not spack.monitor.cli:
        return

    tty.debug("Running on_phase_success %s, phase %s" % (pkg.name, phase_name))
    result = spack.monitor.cli.send_phase(pkg, phase_name, log_file, "SUCCESS")
    tty.verbose(result.get('message'))


def on_phase_error(pkg, phase_name, log_file):
    """Triggered on a phase error
    """
    if not spack.monitor.cli:
        return

    tty.debug("Running on_phase_error %s, phase %s" % (pkg.name, phase_name))
    result = spack.monitor.cli.send_phase(pkg, phase_name, log_file, "ERROR")
    tty.verbose(result.get('message'))


def on_analyzer_save(pkg, result):
    """given a package and a result, if we have a spack monitor, upload
    the result to it.
    """
    if not spack.monitor.cli:
        return

    # This hook runs after a save result
    spack.monitor.cli.send_analyze_metadata(pkg, result)
