#%Module
## Module rc created by spack (https://github.com/spack/spack) on {{ timestamp }}
##

{% block hidden %}
{% if hidden_modules|length > 0 %}
if {[info exists ModuleTool] && $ModuleTool eq {Modules} && [versioncmp $ModuleToolVersion 4.7] >= 0} {
{% for module in hidden_modules %}
    module-hide --soft --hidden-loaded {{ module }}
{% endfor %}
} elseif {[info exists ::env(LMOD_VERSION_MAJOR)]} {
{% for module in hidden_modules %}
    hide-version {{ module }}
{% endfor %}
}
{% endif %}
{% endblock %}
