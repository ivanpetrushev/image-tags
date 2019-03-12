
function submitCheckboxes(){
    var aTagIds = [];
    $("input:checkbox:checked").each(function(index, element) {
        iTagId = $(element).data('tag-id');
        aTagIds.push(iTagId);
    })

    window.location = "/tag/generate_sequence/" + aTagIds.join(",");
}

