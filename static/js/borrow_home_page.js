
    var selectedAddress = {'province':'', 'city':'', 'area':'', 'town':''};
    var $town = $('select[name="town"]');
    var clearTown = function(){
        $town.hide().empty();
    }
    var townFormat = function(info){
        clearTown();
        if(info['code']%1e4&&info['code']<7e5){ //是否为“区”且不是港澳台地区
            $.ajax({
                url:'http://passer-by.com/data_location/town/'+info['code']+'.json',
                dataType:'json',
                success:function(town){
                    $town.show();
                    $town.append('<option value=""> - 街道、乡镇 - </option>');
                    for(i in town){
                        $town.append('<option value="'+i+'">'+town[i]+'</option>');
                    }
                }
            });
        }
    };
       $('#demo4').citys({
        onChange: function(info){
            clearTown();
            selectedAddress.province = info.province;
            selectedAddress.city = info.city;
            selectedAddress.area = info.area;
        },
        onAreaChange:function(info){
            townFormat(info);
        }
    },function(api){
        var info = api.getInfo();
        townFormat(info);
    });
    $town.on('change', function(){
        selectedAddress.town = $(this).find("option:selected").text();
    });

    $('#demo3').citys({
        onChange: function(info){
            clearTown();
            selectedAddress.province = info.province;
            selectedAddress.city = info.city;
            selectedAddress.area = info.area;
        },
        onAreaChange:function(info){
            townFormat(info);
        }
    },function(api){
        var info = api.getInfo();
        townFormat(info);
    });
    $town.on('change', function(){
        selectedAddress.town = $(this).find("option:selected").text();
    });

    console.log(selectedAddress); //输出最终选择的省、市、区县、街道

        				$(".lend_follow_main_left").find("a").each(function(index,elem){
					$(this).click(function(){
						var TabName = $(this).html();
						var Page = index;
						$(".lend_follow_main_titleNew").find("h4").html(TabName);
					})
				})
                   $(document).ready(function(e) {
                $('.yearselect').yearselect();
            });

// // 异步用户基本信息提交
//     $(function(){
//    verify(
//         [
//             {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
//         ]
//     );
//     //保存个人资料
//     $('#jsEditUserBasicProfileBtn').on('click', function(){
//         var _self = $(this),
//             $jsEditUserBasicProfileForm = $('#jsEditUserBasicProfileForm');
//             verify = verifySubmit(
//             [
//                 {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
//             ]
//         );
//         if(!verify){
//            return;
//         }
//         $.ajax({
//             cache: false,
//             type: 'post',
//             dataType:'json',
//             url:"/userAccountView/basic_info_Save/",
//             data:$jsEditUserBasicProfileForm.serialize(),
//             async: true,
//             beforeSend:function(XMLHttpRequest){
//                 _self.val("保存中...");
//                 _self.attr('disabled',true);
//             },
//             success: function(data) {
//                if(data.status == "failure"){
//                      Dml.fun.showTipsDialog({
//                         title: '保存失败',
//                         h2: data.msg
//                     });
//                 }else if(data.status == "success"){
//                     Dml.fun.showTipsDialog({
//                         title: '保存成功',
//                         h2: '个人信息修改成功！'
//                     });
//                     // setTimeout(function(){window.location.href = window.location.href;},1500);
//                 }
//             },
//             complete: function(XMLHttpRequest){
//                 _self.val("保存");
//                 _self.removeAttr("disabled");
//             }
//         });
//     });
// });

// 异步用户家庭信息提交
    $(function(){
   verify(
        [
            {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserFamlityProfileBtn').on('click', function(){
        var _self = $(this),
            $jsEditUserFamilyProfileForm = $('#jsEditUserFamilyProfileForm')
            verify = verifySubmit(
            [
                {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
            ]
        );
        if(!verify){
           return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/userAccountView/family_info_Save/",
            data:$jsEditUserFamilyProfileForm.serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("保存中...");
                _self.attr('disabled',true);
            },
            success: function(data) {
               if(data.status == "failure"){
                     Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: data.msg
                    });
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    // setTimeout(function(){window.location.href = window.location.href;},1500);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });
});

// 异步用户公司信息提交
    $(function(){
   verify(
        [
            {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserCompanyProfileBtn').on('click', function(){
        var _self = $(this),
            $jsEditUserCompanyProfileForm = $('#jsEditUserCompanyProfileForm')
            verify = verifySubmit(
            [
                {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
            ]
        );
        if(!verify){
           return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/userAccountView/company_info_Save/",
            data:$jsEditUserCompanyProfileForm.serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("保存中...");
                _self.attr('disabled',true);
            },
            success: function(data) {
               if(data.status == "failure"){
                     Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: data.msg
                    });
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    // setTimeout(function(){window.location.href = window.location.href;},1500);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });
});