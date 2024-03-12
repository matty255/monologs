class EasyQuill {
    constructor(quillInstance) {
        if (!quillInstance) {
            throw new Error('No Quill instance provided');
        }
        this.quill = quillInstance;
    }

    getContents() {
        return this.quill.getContents();
    }

    getText(index, length) {
        return this.quill.getText(index, length);
    }

    insertText(index, text, formats) {
        this.quill.insertText(index, text, formats);
    }

    formatText(index, length, formats) {
        this.quill.formatText(index, length, formats);
    }

    deleteText(index, length) {
        this.quill.deleteText(index, length);
    }

    setContents(contents) {
        this.quill.setContents(contents);
    }

    getFormat(range) {
        return this.quill.getFormat(range);
    }

    setText(text) {
        this.quill.setText(text);
    }

    setContents(contents) {
        contents.push({ insert: '\n' }); // Add a newline at the end
        this.quill.setContents(contents);
    }
    // 기타 필요한 API 메서드를 여기에 추가하세요.
}
