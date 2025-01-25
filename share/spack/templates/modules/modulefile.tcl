#%Module1.0
## Module file created by spack (https://github.com/spack/spack) on {{ timestamp }}
##
## {{ spec.short_spec }}
##
{% if configure_options %}
## Configure options: {{ configure_options | wordwrap(8192 - 23, True, "\n##                    ", 0) }}
##
{% endif %}


{% block header %}
{% if short_description %}
module-whatis {{ '{' }}{{ short_description }}{{ '}' }}
{% endif %}

proc ModulesHelp { } {
    puts stderr {{ '{' }}Name   : {{ spec.name }}{{ '}' }}
    puts stderr {{ '{' }}Version: {{ spec.version }}{{ '}' }}
    puts stderr {{ '{' }}Target : {{ spec.target }}{{ '}' }}
{% if long_description %}
    puts stderr {}
{{ long_description| textwrap(72)| curly_quote()| prepend_to_line('    puts stderr ')| join() }}
{% endif %}
}
{% endblock %}

{% block autoloads %}
{% if autoload|length > 0 %}
if {![info exists ::env(LMOD_VERSION_MAJOR)]} {
{% for module in autoload %}
    module load {{ module }}
{% endfor %}
} else {
{% for module in autoload %}
    depends-on {{ module }}
{% endfor %}
}
{% endif %}
{% endblock %}
{#  #}
{% block prerequisite %}
{% for module in prerequisites %}
prereq {{ module }}
{% endfor %}
{% endblock %}
{#  #}
{% block conflict %}
{% for name in conflicts %}
conflict {{ name }}
{% endfor %}
{% endblock %}

set decompose_path [split [module-info getenv PATH] ":"]
set decompose_before {}
set decompose_after {}
set decompose_found 0
set decompose_split_sentinel "spack-sentinel"

module set-path SPACK_PATH $decompose_before

foreach dir $decompose_path {
    if {!$decompose_found && [string match $decompose_split_sentinel $dir]} {
        set decompose_found 1
    } elseif {$decompose_found} {
        lappend $decompose_after $dir
    } else {
        lappend $decompose_before $dir
    }
}

set decompose_before_path [join $decompose_before ":"]
set decompose_after_path [join $decompose_after ":"]

{% block environment %}
{% for command_name, cmd in environment_modifications %}
{% if command_name == 'PrependPath' %}
{% if cmd.separator == ':' %}
prepend-path {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% else %}
prepend-path --delim {{ '{' }}{{ cmd.separator }}{{ '}' }} {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% endif %}
{% elif command_name in ('AppendPath', 'AppendFlagsEnv') %}
{% if cmd.separator == ':' %}
append-path {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% else %}
append-path --delim {{ '{' }}{{ cmd.separator }}{{ '}' }} {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% endif %}
{% elif command_name in ('RemovePath', 'RemoveFlagsEnv') %}
{% if cmd.separator == ':' %}
remove-path {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% else %}
remove-path --delim {{ '{' }}{{ cmd.separator }}{{ '}' }} {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% endif %}
{% elif command_name == 'SetEnv' %}
setenv {{ cmd.name }} {{ '{' }}{{ cmd.value }}{{ '}' }}
{% elif command_name == 'UnsetEnv' %}
unsetenv {{ cmd.name }}
{% endif %}
{#  #}
{% endfor %}
{# Make sure system man pages are enabled by appending trailing delimiter to MANPATH #}
{% if has_manpath_modifications %}
append-path MANPATH {{ '{' }}{{ '}' }}
{% endif %}
{% endblock %}

set combined_path [join [list $decompose_before_path $decompose_split_sentinel $decompose_after_path] ":"]
module set-path PATH $combined_path

{% block footer %}
{# In case the module needs to be extended with custom Tcl code #}
{% endblock %}
