
if (typeof(aSequenceContents) != 'undefined') {
    var iCurrentFileId;
    var oInterval;
    var iMsInterval = 3000;

    function writeTitle(sMsg){
        if (typeof sMsg == 'undefined'){
            sMsg = "";
        }

        var iTotalCount = aSequenceContents.length;
        var iCurrentCount = 0;
        for (var i = 0; i < iTotalCount; i++){
            if (iCurrentFileId == aSequenceContents[i]){
                iCurrentCount = i + 1;
            }
        }

        $("#play_sequence_title_section").text(iCurrentCount + '/' + iTotalCount +
            " ... file id: " + iCurrentFileId + " " + sMsg);
    }

    function loadImage(iFileId){
        var sUrl = '/tag/get_file/' + iFileId;
        $("#image_here").attr('src', sUrl);

        document.title = iFileId;
        iCurrentFileId = iFileId;

        writeTitle();
    }

    function loadNextImage(){
        for (var i = 0; i < aSequenceContents.length-1; i++){
            if (aSequenceContents[i] == iCurrentFileId){
                loadImage(aSequenceContents[i+1]);
                return;
            }
        }
    }

    function loadPrevImage(){
        for (var i = 1; i < aSequenceContents.length; i++){
            if (aSequenceContents[i] == iCurrentFileId){
                loadImage(aSequenceContents[i-1]);
                return;
            }
        }
    }

    $(document).ready(function(){
        $(document).keydown(function(evn){
            var iCode = evn.keyCode;
            if (iCode == 27){ // ESC
                $.ajax({
                    type: 'GET',
                    url: '/tag/set_needs_tagging/' + iCurrentFileId
                })
                writeTitle("MARKED")
            }
            if (iCode == 39){ // RIGHT ARROW
                clearInterval(oInterval);
                loadNextImage();
                oInterval = setInterval("loadNextImage()", iMsInterval);
            }
            if (iCode == 37){ // LEFT ARROW
                clearInterval(oInterval);
                loadPrevImage();
                oInterval = setInterval("loadNextImage()", iMsInterval);
            }
        })

        // преоразмеряване на картинката по време на зареждането ѝ
        $("#image_here").load(function(){
            $(this).removeAttr('width');
            $(this).removeAttr('height');

            var iWidth = $("#image_here").width();
            var iHeight = $("#image_here").height();
            var fRatio = parseFloat(iWidth / iHeight);

            var iMaxWidth = window.innerWidth - 10;
            var iMaxHeight = window.innerHeight - 100;

            var iDeltaWidth = iWidth - iMaxWidth;
            var iDeltaHeight = iHeight - iMaxHeight;

            if (iDeltaWidth > iDeltaHeight){
                $(this).attr('width', iMaxWidth);
                var fCorrection = iWidth / iMaxWidth;
                $(this).attr('height', iHeight / fCorrection);
            }
            else {
                $(this).attr('height', iMaxHeight);
                var fCorrection = iHeight / iMaxHeight;
                $(this).attr('width', iWidth / fCorrection)
            }

        });

        loadImage(aSequenceContents[0]);
        oInterval = setInterval("loadNextImage()", iMsInterval);
    })
}