var code_editor = CodeMirror(document.getElementById("code-editor"), {
    lineNumbers: true,
    lineWrapping: true,
    extraKeys: {Tab: false}
});

var input_editor = CodeMirror(document.getElementById("input-editor"), {
    lineNumbers: true,
    lineWrapping: true,
    extraKeys: {Tab: false}
});