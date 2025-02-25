# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io

import llnl.util.tty as tty
from llnl.util.filesystem import visit_directory_tree

import spack.config
import spack.error
import spack.verify_libraries


def post_install(spec, explicit):
    """Check whether shared libraries can be resolved in RPATHs."""
    policy = spack.config.get("config:shared_linking:missing_library_policy", "ignore")

    # Currently only supported for ELF files.
    if policy == "ignore" or spec.external or spec.platform not in ("linux", "freebsd"):
        return

    visitor = spack.verify_libraries.ResolveSharedElfLibDepsVisitor(
        [*spack.verify_libraries.ALLOW_UNRESOLVED, *spec.package.unresolved_libraries]
    )
    visit_directory_tree(spec.prefix, visitor)

    if not visitor.problems:
        return

    output = io.StringIO("not all executables and libraries can resolve their dependencies:\n")
    visitor.write(output)
    message = output.getvalue().strip()

    if policy == "error":
        raise CannotLocateSharedLibraries(message)

    tty.warn(message)


class CannotLocateSharedLibraries(spack.error.SpackError):
    pass
