# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import gzip
import io
import os
import shutil
import sys

import spack.cmd
import spack.spec
import spack.util.compression as compression
from spack.cmd.common import arguments
from spack.main import SpackCommandError

description = "print out logs for packages"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["spec"])


def _dump_byte_stream_to_stdout(instream: io.BufferedIOBase) -> None:
    # Reopen stdout in binary mode so we don't have to worry about encoding
    outstream = os.fdopen(sys.stdout.fileno(), "wb", closefd=False)
    shutil.copyfileobj(instream, outstream)


def _logs(cmdline_spec: spack.spec.Spec, concrete_spec: spack.spec.Spec):
    if concrete_spec.installed:
        log_path = concrete_spec.package.install_log_path
    elif os.path.exists(concrete_spec.package.stage.path):
        # TODO: `spack logs` can currently not show the logs while a package is being built, as the
        # combined log file is only written after the build is finished.
        log_path = concrete_spec.package.log_path
    else:
        raise SpackCommandError(f"{cmdline_spec} is not installed or staged")

    try:
        stream = open(log_path, "rb")
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise SpackCommandError(f"No logs are available for {cmdline_spec}") from e
        raise SpackCommandError(f"Error reading logs for {cmdline_spec}: {e}") from e

    with stream as f:
        ext = compression.extension_from_magic_numbers_by_stream(f, decompress=False)
        if ext and ext != "gz":
            raise SpackCommandError(f"Unsupported storage format for {log_path}: {ext}")

        # If the log file is gzip compressed, wrap it with a decompressor
        _dump_byte_stream_to_stdout(gzip.GzipFile(fileobj=f) if ext == "gz" else f)


def logs(parser, args):
    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        raise SpackCommandError("You must supply a spec.")

    if len(specs) != 1:
        raise SpackCommandError("Too many specs. Supply only one.")

    concrete_spec = spack.cmd.matching_spec_from_env(specs[0])

    _logs(specs[0], concrete_spec)
