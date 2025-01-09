# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import textwrap
from typing import Optional

import llnl.util.tty as tty
from llnl.util.tty.color import colorize

import spack.environment as ev
import spack.repo
import spack.store
from spack.util.environment import EnvironmentModifications


def activate_header(env, shell, prompt=None, view: Optional[str] = None):
    # Construct the commands to run
    cmds = ""
    if shell == "csh":
        # TODO: figure out how to make color work for csh
        cmds += "setenv SPACK_ENV %s;\n" % env.path
        if view:
            cmds += "setenv SPACK_ENV_VIEW %s;\n" % view
        cmds += 'alias despacktivate "spack env deactivate";\n'
        if prompt:
            cmds += "if (! $?SPACK_OLD_PROMPT ) "
            cmds += 'setenv SPACK_OLD_PROMPT "${prompt}";\n'
            cmds += 'set prompt="%s ${prompt}";\n' % prompt
    elif shell == "fish":
        if "color" in os.getenv("TERM", "") and prompt:
            prompt = colorize("@G{%s} " % prompt, color=True)

        cmds += "set -gx SPACK_ENV %s;\n" % env.path
        if view:
            cmds += "set -gx SPACK_ENV_VIEW %s;\n" % view
        cmds += "function despacktivate;\n"
        cmds += "   spack env deactivate;\n"
        cmds += "end;\n"
        #
        # NOTE: We're not changing the fish_prompt function (which is fish's
        # solution to the PS1 variable) here. This is a bit fiddly, and easy to
        # screw up => spend time reasearching a solution. Feedback welcome.
        #
    elif shell == "bat":
        # TODO: Color
        cmds += 'set "SPACK_ENV=%s"\n' % env.path
        if view:
            cmds += 'set "SPACK_ENV_VIEW=%s"\n' % view
    elif shell == "pwsh":
        cmds += "$Env:SPACK_ENV='%s'\n" % env.path
        if view:
            cmds += "$Env:SPACK_ENV_VIEW='%s'\n" % view
    else:
        bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
        zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)

        cmds += "export SPACK_ENV=%s;\n" % env.path
        if view:
            cmds += "export SPACK_ENV_VIEW=%s;\n" % view
        cmds += "alias despacktivate='spack env deactivate';\n"
        if prompt:
            cmds += textwrap.dedent(
                rf"""
                if [ -z ${{SPACK_OLD_PS1+x}} ]; then
                    if [ -z ${{PS1+x}} ]; then
                        PS1='$$$$';
                    fi;
                    export SPACK_OLD_PS1="${{PS1}}";
                fi;
                if [ -n "${{TERM:-}}" ] && [ "${{TERM#*color}}" != "${{TERM}}" ] && \
                   [ -n "${{BASH:-}}" ];
                then
                    export PS1="{bash_color_prompt} ${{PS1}}";
                elif [ -n "${{TERM:-}}" ] && [ "${{TERM#*color}}" != "${{TERM}}" ] && \
                     [ -n "${{ZSH_NAME:-}}" ];
                then
                    export PS1="{zsh_color_prompt} ${{PS1}}";
                else
                    export PS1="{prompt} ${{PS1}}";
                fi
                """
            ).lstrip("\n")
    return cmds


def deactivate_header(shell):
    cmds = ""
    if shell == "csh":
        cmds += "unsetenv SPACK_ENV;\n"
        cmds += "unsetenv SPACK_ENV_VIEW;\n"
        cmds += "if ( $?SPACK_OLD_PROMPT ) "
        cmds += '    eval \'set prompt="$SPACK_OLD_PROMPT" &&'
        cmds += "          unsetenv SPACK_OLD_PROMPT';\n"
        cmds += "unalias despacktivate;\n"
    elif shell == "fish":
        cmds += "set -e SPACK_ENV;\n"
        cmds += "set -e SPACK_ENV_VIEW;\n"
        cmds += "functions -e despacktivate;\n"
        #
        # NOTE: Not changing fish_prompt (above) => no need to restore it here.
        #
    elif shell == "bat":
        # TODO: Color
        cmds += 'set "SPACK_ENV="\n'
        cmds += 'set "SPACK_ENV_VIEW="\n'
        # TODO: despacktivate
        # TODO: prompt
    elif shell == "pwsh":
        cmds += "Set-Item -Path Env:SPACK_ENV\n"
        cmds += "Set-Item -Path Env:SPACK_ENV_VIEW\n"
    else:
        cmds += "if [ ! -z ${SPACK_ENV+x} ]; then\n"
        cmds += "unset SPACK_ENV; export SPACK_ENV;\n"
        cmds += "fi;\n"
        cmds += "if [ ! -z ${SPACK_ENV_VIEW+x} ]; then\n"
        cmds += "unset SPACK_ENV_VIEW; export SPACK_ENV_VIEW;\n"
        cmds += "fi;\n"
        cmds += "alias despacktivate > /dev/null 2>&1 && unalias despacktivate;\n"
        cmds += "if [ ! -z ${SPACK_OLD_PS1+x} ]; then\n"
        cmds += "    if [ \"$SPACK_OLD_PS1\" = '$$$$' ]; then\n"
        cmds += "        unset PS1; export PS1;\n"
        cmds += "    else\n"
        cmds += '        export PS1="$SPACK_OLD_PS1";\n'
        cmds += "    fi;\n"
        cmds += "    unset SPACK_OLD_PS1; export SPACK_OLD_PS1;\n"
        cmds += "fi;\n"

    return cmds


def activate(
    env: ev.Environment, use_env_repo=False, view: Optional[str] = "default"
) -> EnvironmentModifications:
    """Activate an environment and append environment modifications

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        env: the environment to activate
        use_env_repo: use the packages exactly as they appear in the environment's repository
        view: generate commands to add runtime environment variables for named view

    Returns:
        spack.util.environment.EnvironmentModifications: Environment variables
        modifications to activate environment."""
    ev.activate(env, use_env_repo=use_env_repo)

    env_mods = EnvironmentModifications()

    #
    # NOTE in the fish-shell: Path variables are a special kind of variable
    # used to support colon-delimited path lists including PATH, CDPATH,
    # MANPATH, PYTHONPATH, etc. All variables that end in PATH (case-sensitive)
    # become PATH variables.
    #
    try:
        if view and env.has_view(view):
            with spack.store.STORE.db.read_transaction():
                env.add_view_to_env(env_mods, view)
    except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
        tty.error(e)
        tty.die(
            "Environment view is broken due to a missing package or repo.\n",
            "  To activate without views enabled, activate with:\n",
            "    spack env activate -V {0}\n".format(env.name),
            "  To remove it and resolve the issue, " "force concretize with the command:\n",
            "    spack -e {0} concretize --force".format(env.name),
        )

    return env_mods


def deactivate() -> EnvironmentModifications:
    """Deactivate an environment and collect corresponding environment modifications.

    Note: unloads the environment in its current state, not in the state it was
        loaded in, meaning that specs that were removed from the spack environment
        after activation are not unloaded.

    Returns:
        Environment variables modifications to activate environment.
    """
    env_mods = EnvironmentModifications()
    active = ev.active_environment()

    if active is None:
        return env_mods

    active_view = os.getenv(ev.spack_env_view_var)

    if active_view and active.has_view(active_view):
        try:
            with spack.store.STORE.db.read_transaction():
                active.rm_view_from_env(env_mods, active_view)
        except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn(
                "Could not fully deactivate view due to missing package "
                "or repo, shell environment may be corrupt."
            )

    ev.deactivate()

    return env_mods
