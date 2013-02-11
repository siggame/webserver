$(function() {
  var opts = {
    container: 'epiceditor',
    basePath: '{{ STATIC_URL }}epiceditor',
    clientSideStorage: false,
    useNativeFullsreen: true,
    parser: marked,
    theme: {
      base:'/themes/base/epiceditor.css',
      preview:'/themes/preview/preview-dark.css',
      editor:'/themes/editor/epic-dark.css'
    },
    focusOnLoad: false,
  };

  var form_field = $('[content-for="epiceditor"]');
  var initial_contents = form_field.val();

  var editor = new EpicEditor(opts);

  editor.load();

  // Add the file contents to the epiceditor
  editor.importFile("", initial_contents);

  // When the user saves, add the contents of the epiceditor 
  // to the form
  $('[epiceditor-save-button="true"]').click(function () {
    var file_contents = editor.exportFile();
    form_field.val(file_contents);
    console.log("Saved");
  });
});
