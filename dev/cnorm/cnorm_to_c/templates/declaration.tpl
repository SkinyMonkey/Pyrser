{%- extends 'statement.tpl' -%}

{%- macro pointer(decl) %}
{%- if "pointer" in decl -%}
{%- for ptr in decl.pointer -%}
  *
{%- if "type_qualifier"  in ptr %} {{ptr.type_qualifier}}{% endif -%}
{%- endfor %}
{%- endif -%}
{%- endmacro -%}

{%- macro parameters(decl) -%}
{%- if "parameters" in decl.ctype -%}
  ({%- for parameter in decl.ctype.parameters -%}
    {# ne pas faire a la main mais faire avec un appel de methode#}
    {%- if loop.index > 1 -%}, {% endif -%}
    {{ctype(parameter.ctype)}}
    {%- if "name" in parameter %} {{array(parameter)}}{%- endif -%}
  {%- endfor %})
{%- endif -%}
{%- endmacro -%}

{%- macro ctype(decl) -%}
{%- if decl.type in ['__struct__', '__union__', '__enum__'] -%}
  {{getattr(self, decl.type)(decl)}}
{%- else -%}
{%- if decl.storage_class_specifier != 'auto'-%}
  {{decl.storage_class_specifier}} {% endif -%}
{%- if decl.sign != 'signed'-%}{{decl.sign}} {% endif -%}
{{decl.type_specifier}}
{%- if decl.type_qualifier != None %} {{decl.type_qualifier}}{% endif -%}
{{pointer(decl)}}
{%- endif -%}
{%- endmacro -%}

{%- macro array(decl) -%}
{{decl.name}}
{%- if "array" in decl -%}
[{# FIXME : expression#}]
{%- endif -%}
{%- endmacro %}

{%- macro __prototype__(decl) -%}
{{ctype(decl.ctype)}} {{decl.name}}{{- parameters(decl)}};
{%- endmacro -%}

{%- macro __func_ptr__(decl) -%}
{{ctype(decl.ctype.return)}} ({{pointer(decl.ctype)}}{{array(decl)}})
{{- parameters(decl)}}
{%- endmacro -%}

{%- macro __struct__(decl) -%}
struct {{decl.type_specifier}}
{%- if "declarations"  in decl -%}
{
  {%- for declaration in decl.declarations -%}
  {{getattr(self, declaration.type)(declaration)}}
  {%- endfor -%}
}
{%- endif -%}
{%- endmacro -%}

{%- macro __union__(decl) -%}
union {{decl.type_specifier}}
{%- if "declarations" in decl -%}
{
  {%- for declaration in decl.declarations -%}
  {{getattr(self, declaration.ctype.type)(declaration)}}
  {%- if "bitfield" in declaration -%}
  : {{expression(declaration.bitfield)}}
  {%- endif -%};
  {%- endfor -%}
}
{%- endif -%}
{%- endmacro -%}

{%- macro __enum__(decl) -%}
enum {{decl.type_specifier}}
{%- if "declarations" in decl -%}
{
  {%- for declaration in decl.declarations -%}
  {{declaration.name}}{% if loop.index < loop.length %},{% endif %}
  {%- endfor -%}
}
{%- endif -%}
{%- endmacro -%}

{%- macro __function__(decl) -%}
{{ctype(decl.ctype)}} {{decl.name}}{{- parameters(decl)}}
{%- if "body" in decl -%}
{}
{%- endif -%}
{%- endmacro -%}

{%- macro __variable__(decl) -%}
{{ctype(decl.ctype)}} {{array(decl)}};
{%- endmacro -%}

{#- not the best way to do this-#}
{%- macro __struct_field__(decl) -%}
{{ctype(decl.ctype)}} {{array(decl)}}
{%- endmacro -%}

{%- macro __declaration__(decl) -%}
{{getattr(self, decl.ctype.type)(decl)}};
{%- endmacro -%}

{#- voir pour les variables de base macro ()-#}

{%- macro declaration(decl) -%}
{{getattr(self, decl.sub_type)(decl)}}
{%- endmacro -%}

{%- macro external_declaration(decl) -%}
  {%- for sub_declaration in decl.external_declaration -%}
  {{declaration(sub_declaration)}}
  {%- endfor -%}
{%- endmacro -%}

{%- block main -%}
{{external_declaration(tree)}}
{%- endblock -%}
