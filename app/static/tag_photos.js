if ($('.image_workspace').length > 0) {
    var aTagLinks = [];
    var iLastFileId = 0;
    var aTagMap = {};

    var bTagifyEventsEnabled = false;
    var inputTagify = document.querySelector('input[name=tags-outside]'),
    tagify = new Tagify(inputTagify, {
        delimiters: ", ",
        dropdown: {
            enabled: 1,
        },
        callbacks: {
            add: function(e) {
                if (! bTagifyEventsEnabled) {
                    return;
                }
                var iTagId = e.detail.data.id;
                var iFileId = $("#image_here").attr('file_id');
                if (typeof iFileId != 'undefined') {
                    $.ajax({
                        type: 'GET',
                        url: '/tag/toggle/' + iFileId + '/' + iTagId
                    })
                    $('a[tag_id="'+iTagId+'"]').toggleClass('tag_selected');
                }
            },
            remove: function(e) {
                if (! bTagifyEventsEnabled) {
                    return;
                }
                var iTagId = e.detail.data.id;
                var iFileId = $("#image_here").attr('file_id');
                if (typeof iFileId != 'undefined') {
                    $.ajax({
                        type: 'GET',
                        url: '/tag/toggle/' + iFileId + '/' + iTagId
                    })
                    $('a[tag_id="'+iTagId+'"]').toggleClass('tag_selected');
                }
            },
        }
    });


    function refreshTagcloud(){
        $("#tagcloud").empty();
        $.ajax({
            type: 'GET',
            url: '/tag/get_cloud',
            dataType: 'json'
        }).done(function(res){
            // res = jQuery.parseJSON(res);
            var aTags = res.data;
            var aWhitelist = [];
            for (var i in aTags){
                if (typeof aTags[i] == 'function') continue;
                var sName = aTags[i].name;
                var cNav = aTags[i].navigation;
                sName = sName.charAt(0).toUpperCase() + sName.slice(1) + "";
                var oNewLink = $(' <a href="#" class="tag" title="' + sName + '"/>').
                    text(sName).
                    attr('tag_id', aTags[i].id);

                aTagLinks.push(oNewLink);

                if (cNav != ''){
                    var txt = oNewLink.html();
                    var sId = "id_" + cNav;
                    txt = '<span id="' + sId +'" class="nav">(' + cNav + ')</span>' + txt;
                    oNewLink.html(txt)
                }

                oNewLink.click(function(e){
                    e.preventDefault();
                    $(this).toggleClass('tag_selected');
                    var iTagId = $(this).attr('tag_id');
                    var iFileId = $("#image_here").attr('file_id');
                    $.ajax({
                        type: 'GET',
                        url: '/tag/toggle/' + iFileId + '/' + iTagId
                    })

                    // update tagify
                    var oTagifyTag = {
                        id: iTagId,
                        value: $(this).attr('title')
                    }
                    bTagifyEventsEnabled = false;
                    if ($(this).hasClass('tag_selected')) {
                        tagify.addTags([oTagifyTag]);
                    } else {
                        tagify.removeTag(oTagifyTag.value);
                    }
                    bTagifyEventsEnabled = true;
                })

                $('#tagcloud').append(oNewLink);

                aWhitelist.push({
                    value: sName,
                    id: aTags[i].id
                })
            }
            tagify.settings.whitelist = aWhitelist;

        })
    }
    $(document).ready(function(){

        // създаване на tagcloud
        refreshTagcloud();

        // клик върху картинката - взимане на следващия имг
        $("#image_here").click(function(){
            // предния file id се отбелязва като тагнат и не се повтаря
            $.ajax({
                type: 'GET',
                url: '/tag/set_is_tagged/'+iLastFileId,
            })

            $.ajax({
                type: 'GET',
                url: '/tag/get_needs_tagging',
                dataType: 'json'
            }).done(function(res){
                // res = jQuery.parseJSON(res);
                res = res.data;
                var iFileId = res.id;
                iLastFileId = iFileId;
                var aTags = res.files_tags;
                // var sUrl = 'ajax.php?action=getImageById&f_id=' + iFileId;
                var sUrl = '/tag/get_file/' + iFileId;
                $("#image_here").attr('src', sUrl);
                $("#image_here").attr('file_id', iFileId);

                document.title = iFileId;

                // изчистване на селекшъните от тагоблака
                for (var i in aTagLinks){
                    if (typeof aTagLinks[i] == 'function') continue;
                    var iThisTagId = aTagLinks[i].attr('tag_id');
                    aTagLinks[i].removeClass('tag_selected');

                    var bTagFound = false;
                    for (var j in aTags){
                        if (aTags[j] == iThisTagId) bTagFound = true;
                    }
                    if (bTagFound){
                        aTagLinks[i].addClass('tag_selected')
                    }
                }

                tagify.removeAllTags();
                bTagifyEventsEnabled = false;
                tagify.addTags(res.files_tags_tagify)
                bTagifyEventsEnabled = true;
            })
        })

        // autoscale image at load time
        $("#image_here").load(function(){
            $(this).removeAttr('width');
            $(this).removeAttr('height');

            var iMaxWidth = window.innerWidth - 10;
            var iMaxHeight = window.innerHeight - 200;

            // get image original dimensions
            var iWidth = $("#image_here")[0].naturalWidth;
            var iHeight = $("#image_here")[0].naturalHeight;

            var fRatio = Math.min(iMaxWidth / iWidth, iMaxHeight / iHeight);
            var iNewWidth = iWidth * fRatio;
            var iNewHeight = iHeight * fRatio;

            $(this).width(iNewWidth + 'px');
            $(this).height(iNewHeight + 'px');
        });

        // добавяне на таг
        $("#newtag").keyup(function(evn){
            if (evn.keyCode == 13){
                var sTagName = $(this).val();
                var oField = $(this);
                $.ajax({
                    type: 'POST',
                    url: '/tag/new',
                    data: {
                        tag_name: sTagName
                    }
                }).done(function(){
                    refreshTagcloud();
                    $("#newtag").val('');
                })
            }
        })

        // toggle tag on keypress in page body
        // if keypress is in text input, ignore it
        $(document).keypress(function(e){
            var bInputFocused = $('input:focus').length;
            if (bInputFocused) {
                return;
            }

            if (e.keyCode == 32) {
                $('.tagify__input').focus();
            }

            bInputFocused = $('.tagify__input:focus').length;
            if (bInputFocused) {
                return;
            }

            if (e.keyCode == 13){
                $("#image_here").trigger('click');
                return;
            }
            var cBtn = String.fromCharCode(e.charCode)
            var sSearchedId = "id_" + cBtn;
            $("#" + sSearchedId).each(function(){
                $(this).parent('a').trigger('click')
            })

        })
    });
}