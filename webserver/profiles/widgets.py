from django import forms
from django.conf import settings
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from string import Template


TEMPLATE = """
<div id="${id}_epiceditor" style="margin-bottom:10px;"></div>

<textarea ${attrs}>${body}</textarea>

<script type="text/javascript" defer>
    $$(function() {
    var opts = {
        container: '${id}_epiceditor',
        basePath: '//cdnjs.cloudflare.com/ajax/libs/epiceditor/0.2.0/',
        clientSideStorage: false,
        useNativeFullsreen: true,
        parser: marked,
        theme: {
          base:'/themes/base/epiceditor.css',
          preview:'/themes/preview/preview-dark.css',
          editor:'/themes/editor/epic-dark.css'
        },
        focusOnLoad: false,
    }

    $$('#${id}').hide();

    var editor = new EpicEditor(opts);
    editor.on('load', function() {
      this.importFile("", $$('#${id}').val());
    });
    editor.on('update', function (file) {
      $$('#${id}').val(file.content);
    });

    editor.load();
  });
</script>
"""


class EpicEditorInput(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value == None:
            value = ""

        template = Template(TEMPLATE)
        context = {
            'id': attrs['id'],
            'static': settings.STATIC_URL,
            'attrs': flatatt(self.build_attrs(attrs, name=name)),
            'body': conditional_escape(force_unicode(value)),
        }

        return mark_safe(template.substitute(context))
