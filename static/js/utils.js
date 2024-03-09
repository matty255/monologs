
function toggleReplyForm(formId) {
    var form = document.getElementById(formId);
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

function navigateToDeletePage(userId) {
    const deleteUrl = `/accounts/delete/${userId}/`;
    window.location.href = deleteUrl;
}