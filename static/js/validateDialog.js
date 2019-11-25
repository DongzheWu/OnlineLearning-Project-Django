function verifyDialogSubmit(array){
    var i = 0,
        length = array.length,
        validata = true;
    for(i; i < length; i++) {
        var obj = array[i],
            _this = $(obj.id);
        validata = validate(obj, _this);
        if(!validata){
             return validata;
        }
    }
    return validata;
}

function validate(obj,_this){
    var tips = obj.tips,
        errorTips = obj.errorTips,
        regName = obj.regName,
        require = obj.require,
        repwd = obj.repwd,
        minlength = obj.minlength,
        strlength = obj.strlength,
        value = $.trim(_this.val());

        if ( require && ( !value || value == 'Select fee' ) ) {
            return Dml.fun.showValidateError(_this,tips);
        }else{
            if (regName && !Dml.regExp[regName].test(value)) {
                 return Dml.fun.showValidateError(_this,errorTips);
            }


            if(minlength != undefined && value.length <= minlength){
                return Dml.fun.showValidateError(_this,'The length shoud be longer than '+minlength);
            }



            if(strlength != undefined && value.length != strlength){
                 return Dml.fun.showValidateError(_this,'The length must be '+strlength);
            }


        //重复密码校验
            if(repwd != undefined && value != $(repwd).val()){
                return Dml.fun.showValidateError(_this,Dml.Msg.erRePwd);
            }

        }
        _this.parent().removeClass('errorput');
        _this.parent().siblings('.error').hide();
        return true;
}

$(function(){
    $('input[type=text]').focus(function(){
        $(this).parent().removeClass('errorput');
        $(this).parent().siblings('.error').hide();
    })
})
