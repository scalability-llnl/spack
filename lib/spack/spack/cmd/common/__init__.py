# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack.paths


def shell_init_instructions(cmd, equivalent):
    """Print out instructions for users to initialize shell support.

    Arguments:
        cmd (str): the command the user tried to run that requires
            shell support in order to work
        equivalent (str): a command they can run instead, without
            enabling shell support
    """

    shell_specific = "{sh_arg}" in equivalent

    msg = [
        "`%s` requires Spack's shell support." % cmd,
        "",
        "To set up shell support, run the command below for your shell.",
        "",
        color.colorize("@*c{For bash/zsh/sh:}"),
        "  . %s/setup-env.sh" % spack.paths.share_path,
        "",
        color.colorize("@*c{For csh/tcsh:}"),
        "  source %s/setup-env.csh" % spack.paths.share_path,
        "",
        color.colorize("@*c{For fish:}"),
        "  source %s/setup-env.fish" % spack.paths.share_path,
        "",
        color.colorize("@*c{For Windows batch:}"),
        "  %s\\spack_cmd.bat" % spack.paths.bin_path,
        "",
        color.colorize("@*c{For PowerShell:}"),
        "  %s\\setup-env.ps1" % spack.paths.share_path,
        "",
        "Or, if you do not want to use shell support, run "
        + ("one of these" if shell_specific else "this")
        + " instead:",
        "",
    ]

    if shell_specific:
        msg += [
            equivalent.format(sh_arg="--sh  ") + "  # bash/zsh/sh",
            equivalent.format(sh_arg="--csh ") + "  # csh/tcsh",
            equivalent.format(sh_arg="--fish") + "  # fish",
            equivalent.format(sh_arg="--bat ") + "  # batch",
            equivalent.format(sh_arg="--pwsh") + "  # powershell",
        ]
    else:
        msg += ["  " + equivalent]

    msg += [
        "",
        "If you have already set up Spack's shell support but still receive",
        "this message, please make sure to call Spack via the `spack` command",
        "without any path components (such as `bin/spack`).",
    ]

    msg += [""]
    tty.error(*msg)
