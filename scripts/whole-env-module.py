import argparse
import os
import tempfile

from llnl.util.lang import dedupe

import spack.database as db
import spack.environment as ev
import spack.environment.shell
import spack.paths
import spack.user_environment as uenv
from spack.util.environment import EnvironmentModifications


def main():
    parser = argparse.ArgumentParser(description="Generate sourcing script")
    parser.add_argument("path", type=str, help="Where to generate the file")
    parser.add_argument(
        "--view-input",
        dest="view_input",
        type=str,
        help="If provided, designate a view to create the module for",
    )
    args = parser.parse_args()
    generate_module(args)


def _associate_specs(specs):
    with tempfile.TemporaryDirectory() as temp_dir:
        database = db.Database(temp_dir)
        for spec in specs:
            database.add(spec, directory_layout=None)
        database._read()
        return set(database.query())


def generate_module(args):
    env_mods = EnvironmentModifications()

    if args.view_input:
        if not os.path.isdir(args.view_input):
            raise Exception(
                f"Specified --view-input {args.view_input} does not exist as a directory"
            )

        view_input = os.path.abspath(args.view_input)
        descriptor = ev.environment.ViewDescriptor(base_path=view_input, root=view_input)

        env_mods.extend(uenv.unconditional_environment_modifications(descriptor))
        view = descriptor.view(new=view_input)
        specs_to_consider = list(view.get_all_specs())

        specs_to_consider = _associate_specs(specs_to_consider)

        env_mods.extend(
            uenv.environment_modifications_for_specs(*specs_to_consider, view=view)
        )

        # Note: you cannot encode PruneDuplicatePaths into a direct lmod action
        # so instead, I run dedupe on the environment modifications.
        # This would be incorrect if for example you had an action sequence like
        # [x, undo(x), x]; you could sidestep that particular issue by reversing
        # de-duping, and then re-reversing. Not sure if other effects might be
        # more subtle
        env_mods.env_modifications = list(dedupe(env_mods.env_modifications))
    else:
        active_env = ev.active_environment()
        if not active_env:
            raise Exception("An active env is required unless --view-input is specified")

        view_id = None
        if active_env.has_view(ev.default_view_name):
            view_id = ev.default_view_name
        else:
            raise Exception(f"{active_env.name} does not have a default view")

        env_mods.extend(spack.environment.shell.activate(env=active_env, view=view_id))

    context = {"environment_modifications": [(type(x).__name__, x) for x in env_mods]}

    import jinja2

    template = jinja2.Template(lmod_template())
    text = template.render(context)

    if os.path.exists(args.path):
        raise Exception(f"Already exists {args.path}")
    with open(args.path, "w") as f:
        f.write(text)


def lmod_template():
    return """\
{% block environment %}
{% for command_name, cmd in environment_modifications %}
{% if command_name == 'PrependPath' %}
prepend_path("{{ cmd.name }}", "{{ cmd.value }}", "{{ cmd.separator }}")
{% elif command_name in ('AppendPath', 'AppendFlagsEnv') %}
append_path("{{ cmd.name }}", "{{ cmd.value }}", "{{ cmd.separator }}")
{% elif command_name in ('RemovePath', 'RemoveFlagsEnv') %}
remove_path("{{ cmd.name }}", "{{ cmd.value }}", "{{ cmd.separator }}")
{% elif command_name == 'SetEnv' %}
setenv("{{ cmd.name }}", "{{ cmd.value }}")
{% elif command_name == 'UnsetEnv' %}
unsetenv("{{ cmd.name }}")
{% endif %}
{% endfor %}
{# Make sure system man pages are enabled by appending trailing delimiter to MANPATH #}
{% if has_manpath_modifications %}
append_path("MANPATH", "", ":")
{% endif %}
{% endblock %}
"""


if __name__ == "__main__":
    main()
