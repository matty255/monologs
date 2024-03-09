document.addEventListener('DOMContentLoaded', (event) => {

    document.getElementById('upload-btn').addEventListener('click', function() {
        document.getElementById('file-input').click();
    });
              
    document.getElementById('file-input').addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const url = e.target.result;
                document.getElementById('image-box').innerHTML = `<img src="${url}" id="image" style="max-width: 100%;">`;
                $('#image').cropper({
                    aspectRatio: 1 / 1,
                    crop: function(event) {
                        // console.log(event.detail.x);
                        // console.log(event.detail.y);
                        // console.log(event.detail.width);
                        // console.log(event.detail.height);
                        // console.log(event.detail.rotate);
                        // console.log(event.detail.scaleX);
                        // console.log(event.detail.scaleY);
                    }
                });
                document.getElementById('image-crop-modal').showModal();
            };
            reader.readAsDataURL(file);
        }
    });
    
    document.getElementById('image-crop-form').addEventListener('submit', function(e) {
        e.preventDefault(); 
      
        $('#image').data('cropper').getCroppedCanvas().toBlob((blob) => {
            const fd = new FormData(this); 
            fd.append('file', blob, 'cropped-image.png');
      
            $.ajax({
                type: 'POST',
                url: this.action,
                enctype: 'multipart/form-data',
                data: fd,

                success: function(response) {
 
                    document.getElementById('image-crop-modal').close(); 
                    window.location.reload();
                },
                error: function(error) {
                    console.error('error', error);
                    alert(`Oops...something went wrong.`);
                },
                cache: false,
                contentType: false,
                processData: false,
            });
        });
    });

});
