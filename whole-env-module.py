import argparse
import os
import pathlib

import spack.environment as ev
import spack.environment.shell
import spack.paths
import spack.tengine as tengine
from spack.util.environment import EnvironmentModifications


def main():
    # parser.add_argument('name', type=str, help="Your name")
    # parser.add_argument('--age', type=int, help="Your age", default=18)
    # parser.add_argument('--greet', action='store_true', help="Greet the user")
    parser = argparse.ArgumentParser(description="Generate sourcing script")
    parser.add_argument('path', type=str, help="Where to generate the file")
    parser.add_argument('--shell', type=str, help="Target shell", default=None)
    args = parser.parse_args()
    generate_module(args)


def generate_module(args):
    active_env = ev.active_environment()

    view = None
    if active_env.has_view(ev.default_view_name):
        view = ev.default_view_name

    env_mods = EnvironmentModifications()
    env_mods.extend(spack.environment.shell.activate(env=active_env, view=view))
    context = {"environment_modifications": [(type(x).__name__, x) for x in env_mods]}

    import jinja2
    #env = tengine.make_environment()
    #import pdb; pdb.set_trace()
    template = jinja2.Template(lmod_template())
    import pdb; pdb.set_trace()
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