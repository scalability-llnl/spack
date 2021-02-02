# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty
import spack.config


def die_if_deployment(command):
    """Die if Spack is in deployment mode."""
    mode = spack.config.restricted_config.get('config:mode', 'standard')
    if isinstance(mode, dict) and 'deployment' in mode:
        msg = "For security reasons, Spack cannot run the `%s`" % command
        msg += " command in deployment mode."
        tty.die(msg)


def setup_deployment_args(command, args, required):
    """
    Setup required arguments in deployment mode

    Arguments:
        command (str): command name
        args (Namespace): Argparse arguments
        required (dict): Arguments to override and new values
    Returns:
        None

    This method modifies the object passed as args.
    """
    mode = spack.config.restricted_config.get('config:mode', 'standard')
    if isinstance(mode, dict) and 'deployment' in mode:
        msg = "Spack is in deployment mode. Setting the following values"
        msg += " for the `%s` command:\n" % command
        for arg_name, new_value in required.items():
            msg += "        %s = %s\n" % (arg_name, new_value)
            setattr(args, arg_name, new_value)
        tty.warn(msg)


def confirm_command_if_deployment(command):
    """
    Warn the user and prompt for confirmation

    Commands that modify the environment (but not configuration) are allowed
    in deployment mode but require confirmation.
    """
    mode = spack.config.restricted_config.get('config:mode', 'standard')
    if isinstance(mode, dict) and 'deployment' in mode:
        env_name = mode['deployment']['env']
        msg = 'Attempting to run command `%s` in environment' % command
        msg += ' %s while in deployment mode.' % env_name
        tty.mgs(msg)
        answer = tty.get_yes_or_no('do you want to proceed?', default=False)
        if not answer:
            tty.die('Aborting `%s` command' % command)
