
function submitCheckboxes(){
    var aBoxes = $("input:checkbox:checked");
    var aTagIds = [];
    aBoxes.each(function(){
        aTagIds.push($(this).attr('data-tag-id'));
    })

    window.location = "/tag/generate_sequence/" + aTagIds.join(",");
}

