# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import textwrap

from llnl.util.tty.color import colorize

from spack.util.environment import EnvironmentModifications


def prompt_modifications(prompt, shell, env=os.environ):
    mods = EnvironmentModifications()

    if shell == "fish" or shell == "pwsh" or shell == "bat":
        # requires a function and can't be set with os.environ
        pass
    elif shell == "csh":
        mods.set("SPACK_OLD_PROMPT", env.get("prompt", None))
        mods.set("prompt", prompt)
    else:
        mods.set("SPACK_OLD_PS1", env.get("PS1", "$$$$"))
        if "TERM" in env and "color" in env["TERM"]:
            if "BASH" in env:
                bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
                mods.set("PS1", f"{bash_color_prompt} {env.get('PS1','$ ')}")
            else:
                zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)
                mods.set("PS1", f"{zsh_color_prompt} {env.get('PS1', '$ ')}")
        else:
            mods.set("PS1", f"{prompt} {env.get('PS1', '$ ')}")

    return mods


def custom_prompt(prompt, shell):
    cmds = ""
    if shell == "csh":
        cmds += "if (! $?SPACK_OLD_PROMPT ) "
        cmds += 'setenv SPACK_OLD_PROMPT "${prompt}";\n'
        cmds += 'set prompt="%s ${prompt}";\n' % prompt
    elif shell == "fish":
        if "color" in os.getenv("TERM", ""):
            prompt = colorize(f"@G{prompt}", color=True)
        cmds += "set -gx SPACK_PROMPT '%s';\n" % prompt
    elif shell == "bat" or shell == "pwsh":
        # TODO
        pass
    else:
        bash_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=True)
        zsh_color_prompt = colorize(f"@G{{{prompt}}}", color=True, enclose=False, zsh=True)
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
