-- -*- lua -*-
-- Module rc created by spack (https://github.com/spack/spack) on {{ timestamp }}
--

{% block hidden %}
{% if hidden_modules|length > 0 %}
{% for module in hidden_modules %}
hide_version("{{ module }}")
{% endfor %}
{% endif %}
{% endblock %}
