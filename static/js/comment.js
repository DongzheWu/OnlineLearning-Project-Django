function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 };

$(function(){
    function validateTextarea(val){
        if(val.length < 3){
            Dml.fun.showTipsDialog({
                title: 'Error message',
                h2: 'The number of comments can be no less than 3 characters!',
                type: 'failbox'
            });
            return false;
        }
        return true;
    }

    var userAvatar = $('#userAvatar').val();
    $('.comenlist').on('focus','.wordbox',function(){
        $(this).parent('.text-box').addClass('text-box-on');
        $(this).keyup();
    });

    
    $('.comenlist').on('input propertychange','.wordbox',function(){
        var val = this.value;
        var len = val.length;
        var els = this.parentNode.children;
        var btn = els[1];
        var word = els[2];
        if (len <= 0 ) {
            word.innerHTML = 'You have no input';
            $(btn).addClass('btn-off');
        }else if(len > 140){
            word.innerHTML = 'You have exceeded length limit';
            btn.style.background='#ccc';
        }else{
            word.innerHTML = len + '/140';  
            btn.style.background='#717171';
        }
    });


    $('.praisebtn').click(function(){
        var txt = $(this).html();
        var btn = $(this);
        var praisesTotal = $(this).parent('div').find('.praiseword');
        var oldTotal = parseInt(praisesTotal.attr('total'));
        var newTotal;
        var newTotal2;

        var request_url = "/common/addpraise/"
        var typeid = 2
        if($(this).hasClass("collected")){
            request_url = "/common/delpraise/"
        }
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            type:"POST",
            url: request_url,
            dataType:"json",
            async: true,
            data:{
                typeid: typeid,
                favid: $(this).attr("data"),
            },
            success:function(data){
                if (!btn.hasClass('collected')) {
                    newTotal = oldTotal + 1;
                    praisesTotal.attr('total', newTotal);
                    if(newTotal == 1){
                        praisesTotal.html('I like it');
                    }else{
                        praisesTotal.html(newTotal + 'I think it is good');
                    }
                    btn.html('Dislike').addClass('collected');
                }else{
                    newTotal2 = oldTotal-1;
                    praisesTotal.attr('total', newTotal2);
                    if(newTotal == 0){
                        praisesTotal.html('No one has liked it yet.');
                    }else{
                         praisesTotal.html( newTotal2 + 'I like it');
                    }
                    btn.html('Like').removeClass('collected');
                }
            },
            beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }

        });
    });


    if(isLogin == 'True'){
        $('.comenlist').on('mouseover','.btn',function(){
            $(this).parents('.textinput').find('.wordbox').blur().css('height','60px');
        });

       $('.commentbtn').on('click',function(){
            var _self = $(this),
                textarea = _self.parent().find('textarea:first'),
                comment = textarea.val(),
                diary_id = _self.attr("diaryid"),
                csrftoken = getCookie('csrftoken'),
                validate = validateTextarea(comment);
            if(!validate){
                return false;
            }
            $.ajax({
                type: "POST",
                url:"/diary/add_comment/",
                data:{
                    comment:comment,
                    diaryid:diary_id,
                },
                success: function(data) {
                    if (data.id){
                        var textareaval = textarea.val(),
                            len = textareaval.length,
                            evalbox =
                            '<div class="commentbox clearfix" >'+
                                '<div class="head"><img width="50" src="'+ userAvatar +'" alt=""/></div>'+
                                '<div class="comment-content2">' +
                                    '<div class="oldcomment">'+
                                        '<p class="comment-text"><span class="user"><i>make comments</i>：</span>' + textareaval + '</p>' +
                                        '<p class="comment-time">'+ Dml.fun.getDate() +'</p>' +
                                        '<p class="replycomment btn btntop" diaryid="'+diary_id+'" commentid="'+data.id+'" selfName="selfName" parentName="parentName">reply</p>'+
                                    '</div>'+
                                '</div>'+
                            '</div>';
                        _self.parents('.commentbox').after(evalbox);
                        textarea.val('');
                        $('.word').html('0/140');
                        $('.wordbox').blur();
                    }
                },
                beforeSend: function(xhr, settings) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });
    });

       $('.comenlist').on('click','.replycomment',function(){
           var _self = $(this),
                diary_id = _self.attr("diaryid"),
                comment_id = _self.attr("commentid"),
                parentName = _self.attr('parentName'),
                selfName = _self.attr('selfName'),
                evalbox =
                '<div class="replycommentbox textinput">'+
                    '<textarea class="replybox wordbox" autocomplete="off" maxlength="140" placeholder="reply'+ selfName +'..."></textarea>'+
                    '<button class="replycommentbtn btn btnbottom" diaryid="'+diary_id+'" commentid="'+comment_id+'" replyid="'+comment_id+'" selfName="'+selfName+'" parentName="'+parentName+'">reply</button>'+
                    '<span class="word"><span class="length">0</span>/140</span>'+
                '</div>';

            _self.parents('.comment-content2').find('.textinput').remove();
            _self.parents('.comment-content2').append(evalbox);
            _self.parents('.comment-content2').find('.replybox').focus();
        });


       $('.comenlist').on('click','.replycommentbtn',function(){
            var _self = $(this),
                textarea = _self.parent().find('textarea:first'),
                comment = textarea.val(),
                diary_id = _self.attr("diaryid"),
                comment_id = _self.attr("commentid"),
                parent_id = _self.attr("replyid"),
                parentName = _self.attr('parentName'),
                selfName = _self.attr('selfName'),
                csrftoken = getCookie('csrftoken'),
                validate = validateTextarea(comment);
            if(!validate){
                return false;
            }
            $.ajax({
                    type: "POST",
                    url:"/diary/add_comment/",
                    data:{
                        comment:comment,
                        diaryid:diary_id,
                        parentid:parent_id,
                        maincommentid:comment_id,
                    },
                    success: function(data) {
                        if (data.id){
                            var textareaval = _self.parent('.replycommentbox').find('.replybox').val(),
                                evalbox =
                                '<div class="replycommentword">' +
                                '<img class="myhead" src="'+ userAvatar+'" alt=""/>' +
                                '<p class="comment-text"><span class="user"><i>I</i> replied <i>'+ parentName +'</i>：</span>' + textareaval + '</p>' +
                                '<p class="comment-time">'+ Dml.fun.getDate() +'</p>' +
                                '<p class="replycsomeone btn btntop" diaryid="' + diary_id + '" commentid="' + data.id + '" replyid="'+parent_id+'" selfName="'+selfName+'" parentName="'+parentName+'">reply</p>' +
                                '</div>'
                            _self.parents('.comment-content2').append(evalbox);
                            _self.parents('.comment-content2').find('.replycommentbox').remove();
                        }
                    },
                    beforeSend: function(xhr, settings) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
            });
        });

        $('.comenlist').on('click','.replycsomeone',function(){
            var _self = $(this),
                diary_id = _self.attr("diaryid"),
                comment_id = _self.attr("commentid"),
                parent_id = _self.attr("replyid"),
                parentName = _self.attr('parentName'),
                selfName = _self.attr('selfName'),
                evalbox = '<div class="replysomeonebox textinput">'+
                                '<textarea class="replybox wordbox" autocomplete="off" maxlength="140" placeholder="reply'+ selfName +'..."></textarea>'+
                                '<button class="replysomeonebtn btn btnbottom" diaryid="'+diary_id+'" commentid="'+comment_id+'" replyid="'+parent_id+'" selfName="'+selfName+'" parentName="'+parentName+'">reply</button>'+
                                '<span class="word"><span class="length">0</span>/140</span>'+
                            '</div>';

            _self.parents('.comment-content2').find('.textinput').remove();
            _self.parents('.comment-content2').append(evalbox);
            _self.parents('.comment-content2').find('.replybox').focus();
        });


        $('.comenlist').on('click','.replysomeonebtn',function(){
            var _self = $(this),
                textarea2 = _self.parent('.replysomeonebox').find('.replybox'),
                textareaval2 = textarea2.val(),
                textarea = _self.parent().find('textarea:first'),
                comment = textarea.val(),
                diary_id = _self.attr("diaryid"),
                comment_id = _self.attr("commentid"),
                parent_id = _self.attr("replyid"),
                parentName = _self.attr('parentName'),
                selfName = _self.attr('selfName'),
                csrftoken = getCookie('csrftoken'),
                validate = validateTextarea(comment);
            if(!validate){
                return false;
            }
            $.ajax({
                type: "POST",
                url:"/diary/add_comment/",
                data:{
                    comment:comment,
                    diaryid:diary_id,
                    parentid:parent_id,
                    maincommentid:comment_id,
                },
                success: function(data) {
                    if (data.id){
                        var evalbox =
                            '<div class="comment-box clearfix">'+
                                '<img class="myhead" src="'+ userAvatar +'" alt=""/>' +
                                '<div class="comment-content">' +
                                '<p class="comment-text"><span class="user"><i>I</i>' +' replied <i>'+ parentName +'</i>:</span>  '+ textareaval2 + '</p>' +
                                '<p class="comment-time">'+ Dml.fun.getDate() +'</p>' +
                                '<button class="replycsomeone btn btntop" diaryid="'+diary_id+'" commentid="'+comment_id+'" replyid="'+data.id+'" selfName="'+selfName+'" parentName="'+parentName+'">reply</button>'+
                                '</div>'+
                            '</div>'
                        _self.parents('.comment-content2 ').append(evalbox);
                        _self.parents('.comment-content2').find('.replysomeonebox').remove();
                    }
                },
                beforeSend: function(xhr, settings) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });

        });
    }
});
