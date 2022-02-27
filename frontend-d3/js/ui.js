const req_url = 'http://localhost:5001';

$('#loading').hide();

$('#file').on('change', function(e) {
    const files = $('#file')[0].files;
    if (files.length > 0) {
        $('#uploadForm').hide();
        $('#loading').show();


        const fd = new FormData($('#uploadForm')[0]);
        $.ajax({
            url: req_url,
            type: 'POST',
            cache: false,
            data: fd,
            processData: false,
            contentType: false
        })
        .done(function(res) {
            $('#loading').hide();
            const midijson = res['json'];
            const path = res['file'];
            $('#audioplayer').html(`
                <audio controls="controls" autoplay="autoplay" id="player">
                    <source src="${req_url}/static/${path}" />
                </audio>
            `);

            $("#player")[0].play();

            drawAnimation(midijson);
        })
        .fail(function(res) {
            console.log(res);
        });
    }
})