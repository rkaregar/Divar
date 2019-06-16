$('#select1').change(function () {
    $.ajax({
        url: '/ads/dropdown/',
        data: {
            'parent_id': $(this).val(),
        },
        success: function (data) {
            $('#select2').html(data);
        }
    });
});
$('#select2').change(function () {
    $.ajax({
        url: '/ads/dropdown/',
        data: {
            'parent_id': $(this).val(),
        },
        success: function (data) {
            $('#category').html(data);
        }
    });
});
