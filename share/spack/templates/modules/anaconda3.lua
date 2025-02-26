{% extends "modules/modulefile.lua" %}
{% block footer %}
source_sh("bash", pathJoin("{{ spec.prefix }}", "etc", "profile.d", "conda.sh"))
{% endblock %}
