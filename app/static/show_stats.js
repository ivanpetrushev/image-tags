
function submitCheckboxes(){
    var aTagIds = [];
    $("input:checkbox:checked").each(function(index, element) {
        iTagId = $(element).data('tag-id');
        aTagIds.push(iTagId);
    })

    window.location = "/tag/generate_sequence/" + aTagIds.join(",");
}

$(document).ready(function(){
    $("input:checkbox").change(function(){
        var aTagIds = [];
        $("input:checkbox:checked").each(function(index, element) {
            iTagId = $(element).data('tag-id');
            aTagIds.push(iTagId);
        })

        if (aTagIds.length == 0) {
            $('.inactive').removeClass('inactive').addClass('active');
            $('.number').each(function() {
                $(this).html($(this).data('orig-value'));
            })

            return;
        }

        $.ajax({
            type: 'POST',
            url: '/tag/get_counts',
            data: {
                selected_tags: aTagIds
            },
            success: function(data) {
                $('.number').html('0');
                $('.active').removeClass('active').addClass('inactive');
                for (var i in data.data) {
                    var el = $('.number[data-tag-id="' + i + '"]');
                    el.html(data.data[i]);
                    el.parent('.col').addClass('active').removeClass('inactive');
                }
            }
        })
    })
})