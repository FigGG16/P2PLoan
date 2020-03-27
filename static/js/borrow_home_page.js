
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



// 异步用户基本信息提交
$(function(){
verify(
    [
        {id: '#mobile', tips: Dml.Msg.epPhone, require: true}
    ]
);
//保存个人资料
$('#jsEditUserBasicProfileBtn').on('click', function(){

    $form = $('#jsEditUserBasicProfileForm');

    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:'/userAccountView/user/basic_info_Save/',
        data:$form.serialize(),
        async: true,
        beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
        success: function(data) {

                    if(data.status == "success"){
                                // {#提交数据成功，进行局部刷新#}
                        $(".people-basic-profile").load(" .people-basic-profile > *");

                        console.log("保存数据成功");

                        $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);


                    }else if(data.status == "failure"){

                         $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);

                    }
            },
        complete: function(XMLHttpRequest){


            }
    });
});
});


// 异步用户家庭信息提交
$(function(){

//保存个人资料
$('#jsEditUserFamlityProfileBtn').on('click', function(){

    $form = $('#jsEditUserFamilyProfileForm');

    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/userAccountView/user/family_info_Save/",
        data:$form.serialize(),
        async: true,
        beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
        success: function(data) {

                    if(data.status == "success"){
                               //  {#提交数据成功，进行局部刷新#}
                        $(".family-profile").load(" .family-profile > *");

                        console.log("保存数据成功");

                        $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);


                    }else if(data.status == "failure"){

                         $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);

                    }
            },
        complete: function(XMLHttpRequest){


            }
    });
});
});


// 异步保存家庭信息提交
$(function(){

//保存个人资料
$('#jsEditUserCompanyProfileBtn').on('click', function(){

    $form = $('#jsEditUserCompanyProfileForm');

    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/userAccountView/user/company_info_Save/",
        data:$form.serialize(),
        async: true,
        beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
        success: function(data) {

                    if(data.status == "success"){
                            //     {#提交数据成功，进行局部刷新#}
                        $(".company-profile").load(" .company-profile > *");

                        console.log("保存数据成功");

                        $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);


                    }else if(data.status == "failure"){

                         $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);

                    }
            },
        complete: function(XMLHttpRequest){


            }
    });
});
});


//投资者信息保存jsEditInvestorBasicProfileForm
    $(function(){
$('#jsEditInvestorBasicProfileBtn').on('click', function(){

    $form = $('#jsEditInvestorBasicProfileForm');

    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:'/userAccountView/user/investor_info_Save/',
        data:$form.serialize(),
        async: true,
        beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
        success: function(data) {

                    if(data.status == "success"){
                                // {#提交数据成功，进行局部刷新#}
                        $(".people-basic-profile").load(" .people-basic-profile > *");

                        console.log("保存数据成功");

                        $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);


                    }else if(data.status == "failure"){

                         $('#WarnModal').modal('show');
                        $("#alert-message").text(data.message);

                    }
            },
        complete: function(XMLHttpRequest){


            }
    });
});
});