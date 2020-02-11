

//自动打开下拉列表
// const $dropdown = $(".dropdown");
// const $dropdownToggle = $(".dropdown-toggle");
// const $dropdownMenu = $(".dropdown-menu");
// const showClass = "show";
//
//
// $(window).on("load resize", function() {
// 	if (this.matchMedia("(min-width: 768px)").matches) {
// 		$dropdown.hover(
// 			function() {
// 				const $this = $(this);
// 				$this.addClass(showClass);
// 				$this.find($dropdownToggle).attr("aria-expanded", "true");
// 				$this.find($dropdownMenu).addClass(showClass);
// 			},
// 			function() {
// 				const $this = $(this);
// 				$this.removeClass(showClass);
// 				$this.find($dropdownToggle).attr("aria-expanded", "false");
// 				$this.find($dropdownMenu).removeClass(showClass);
// 			}
// 		);
// 	} else {
// 		$dropdown.off("mouseenter mouseleave");
// 	}
// });

//获取登录类型切换点击事件
			$(function(){
			$("#borrowLoginBtn").click(function () {
				$("#borrowLoginView").hide();

				$("#lendLoginView").show();

				});

			});

			//获取按钮添加点击事件

			$(".lendLoginBtn").click(function () {
				$("#borrowLoginView").show();

				$("#lendLoginView").hide();

			});

//轮播图
				var timer = null;
				var num = 0;
				
				//图片轮播
				function scroll(){
					timer = setInterval(go,3000);
				}
				
				
				function go(){
					num++;
					num%=3;
					$('#banner_pic').css('margin-left','-'+num*100+'%');
					$('#point').find('li').attr('class','');
					$('#point').find('li').eq(num).attr('class','in');
				}
				
				scroll();

//我要借入导航鼠标事件
				$('nav').find('li').eq(2).on({
					mouseover:function(){
						$('.borrow_in_bg').css('display','block');
					},
					
					mouseout:function(){
						$('.borrow_in_bg').css('display','none');
					}
				})
				
				$('.borrow_in_bg').on({
					mouseover:function(){
						$(this).css('display','block');
						$('nav').find('li').eq(2).find('span').attr('class','ul-img');
					},
					
					mouseout:function(){
						$(this).css('display','none');
						$('nav').find('li').eq(2).find('span').attr('class','');
					}
				})
				
//我要借出导航鼠标事件
				$('nav').find('li').eq(1).on({
					mouseover:function(){
						$('.lend_out_bg').css('display','block');
					},
					
					mouseout:function(){
						$('.lend_out_bg').css('display','none');
					}
				})
				
				$('.lend_out_bg').on({
					mouseover:function(){
						$(this).css('display','block');
						$('nav').find('li').eq(1).find('span').attr('class','ul-img');
					},
					
					mouseout:function(){
						$(this).css('display','none');
						$('nav').find('li').eq(1).find('span').attr('class','');
					}
				})
				
//导航三角图标
				$("#nav").find('li').each(function(index,elem){
					$(this).on({
						"mouseover":function(){
							if(index != 0){
								$(this).find("span").attr('class','ul-img');
							}
						},	
						"mouseout":function(){
							if(index != 0){
								$(this).find("span").attr('class','');
						}
						}
					})
				})
				
//首页-我需要钱-我要借入
				$("#btn1").click(function(){
					$(location).attr("href","borrow.html");
				})
				
//borrow页面
				$("#borrow_content_btn1, #borrow_content_btn2").click(function(){
					$(location).attr("href","borrow_details.html");
				})
				
//新闻-社区
				$(".news_content_message").find("li").each(function(index,elem){
					$(this).click(function(){
						$(location).attr("href","news_content.html");
					})
				})
				
				
//隐藏选项卡
				$(".Right_Main").children("div").each(function(index,elem){
					if (index == 0) {
						$(this).show();
					} else{
						$(this).hide();
					}
				})
				
				$(".account_recharge_main2").hide();
				$(".BlackScreen").hide();
				$(".account_withdrawals_main_popup1, .account_withdrawals_main_popup2").hide();
				$(".borrow_list2_table2").hide();
				$(".borrow_list2_table3").hide();
				
				$(".momey_query_main_page2").hide();
				$(".momey_query_main_page3").hide();
				$(".momey_query_main_page2_table1_11").hide();
				$(".momey_query_main_page2_table1_12").hide();
				$(".momey_query_main_page2_table1_13").hide();
				
//账户充值
				$(".account_recharge_main_header").find('p').each(function(index,elem){
					$(this).click(function(){
						$(this).attr('class','lend_follow_main_right_header_focus').siblings('p').attr('class','');
						
						switch (index){
							case 0:
								$(".account_recharge_main1").show();
								$(".account_recharge_main2").hide();
								break;
							case 1:
								$(".account_recharge_main1").hide();
								$(".account_recharge_main2").show();
								break;
							default:
								break;
						}
					})
				})
				
//借入-我的借款列表
				$(".lend_follow_main_right_header").find('p').each(function(index,elem){
					$(this).click(function(){
						$(this).attr('class','lend_follow_main_right_header_focus').siblings('p').attr('class','');
						
						switch (index){
							case 0:
								$(".borrow_list2_table1").show();
								$(".borrow_list2_table2").hide();
								$(".borrow_list2_table3").hide();
								break;
							case 1:
								$(".borrow_list2_table1").hide();
								$(".borrow_list2_table2").show();
								$(".borrow_list2_table3").hide();
								break;
							case 2:
								$(".borrow_list2_table1").hide();
								$(".borrow_list2_table2").hide();
								$(".borrow_list2_table3").show();
								break;
							default:
								break;
						}
					})
				})
				
//借出-我的借款列表
				var arr = [".momey_query_main_page2_table1_11",".momey_query_main_page2_table1_12",".momey_query_main_page2_table1_13"];
				
				$(".lend_follow_main_right_header").find('p').each(function(index,elem){
					$(this).click(function(){
						$(this).attr('class','lend_follow_main_right_header_focus').siblings('p').attr('class','');
						
						switch (index){
							case 0:
								$(".momey_query_main_page1").show();
								$(".momey_query_main_page2").hide();
								$(".momey_query_main_page3").hide();
								break;
							case 1:
								$(".momey_query_main_page1").hide();
								$(".momey_query_main_page2").show();
								$(".momey_query_main_page3").hide();
								break;
							case 2:
								$(".momey_query_main_page1").hide();
								$(".momey_query_main_page2").hide();
								$(".momey_query_main_page3").show();
								break;
							default:
								break;
						}
					})
				})
				
				$(".momey_query_main_page2_table1_menu1, .momey_query_main_page2_table1_menu2, .momey_query_main_page2_table1_menu3").click(function(){
					var a = $(this).attr('class');
					var num1 = a[a.length-1];
					
					var status = $(this).attr("data-status");
					
					if(status == "menuhide"){
						$(this).css("background-image","url(images/momey_query_main_hide.jpg)");
						$(arr[num1-1]).show();
						$(this).attr("data-status","menushow");
					}else{
						$(this).css("background-image","url(images/momey_query_main_show.jpg)");
						$(arr[num1-1]).hide();
						$(this).attr("data-status","menuhide");
					}
					
				})
				
				$(".lend_follow_main_left").find("p").each(function(index,elem){
					$(this).click(function(){
//						先进行删除当前选择标签栏的span操作,防止获取内容时把span也一同获取
						$(this).find('span').remove();
						var TabName = $(this).html();
						var Page = index;
//						左侧选择
						$(this).css("background-color","#FFFFFF").siblings("p").css("background-color","#F8F8F8");
						$(this).append("<span style='color: #555555; float: right;'>&gt;</span>").siblings("p").find('span').empty();
						$(".lend_follow_main_title").find("h1").html(TabName);
						
//						选项卡切换
						$(".Right_Main").children("div").each(function(index,elem){
							if ($(this).attr("data-page") == Page) {
								$(this).show();
							} else{
								$(this).hide();
							}
						})
						
					})
				})
				
//账户提现
				$(".BlackScreen").click(function(){
					$(".BlackScreen").hide();
					$(".account_withdrawals_main_popup1, .account_withdrawals_main_popup2").hide();
				});
				
				$(".account_withdrawals_main_form_a1").click(function(){
					$(".BlackScreen").show();
					$(".account_withdrawals_main_popup1").show();
				})
				
				$(".account_withdrawals_main_form_a2").click(function(){
					$(".BlackScreen").show();
					$(".account_withdrawals_main_popup2").show();
				})
				
				$(".account_withdrawals_main_popup1 h5 >span, .account_withdrawals_main_popup2 h5 >span").click(function(){
					$(".BlackScreen").hide();
					$(".account_withdrawals_main_popup1, .account_withdrawals_main_popup2").hide();
				})
				
//本金保障
				$(".Principal_protection_main").children("div").each(function(index,elem){
									if (index == 0) {
										$(this).show();
									} else{
										$(this).hide();
									}
					})
				
				$(".upload_message_main_left").find("p").each(function(index,elem){
					if(index == 0){
						$(this).css("background-color",'#CCCCCC');
					}
					$(this).click(function(){
						$(this).css("background-color",'#CCCCCC').siblings().css("background-color","");
						var page = index;
						var Name = $(this).text();
						var TabName = Name.substring(0,Name.length-1);
						$(".upload_message_main_right_title > h1").html(TabName);
						
						$(".Principal_protection_main").children("div").each(function(index,elem){
							if (index == page) {
								$(this).show();
							} else{
								$(this).hide();
							}
						})
						
						
					})
				})
				
//发布借款
				$("#borrow_details_content_btn2").click(function(){
					$(location).attr("href","borrow_success.html");
				})
				

//我要借入
				$("#lend_list_box2_table").find("tr").each(function(index,elem){
					if(index != 0){
							$(this).css("cursor","pointer");
						}
					$(this).click(function(){
							$(location).attr("href","lend_list_details.html");
					})
				})

//信息
			$(".message_btn_bg").click(function(){
				$(location).attr("href","write_letter.html");
			})
			
			$("#message_setting2").find("li").each(function(index,elem){
				$(this).click(function(){
					switch (index){
					case 0:
						$(location).attr("href","personal_center.html");
						break;
					case 1:
						$(location).attr("href","safety_center.html");
						break;
					case 2:
						$(location).attr("href","head_portrait.html");
						break;
					case 3:
						$(location).attr("href","security.html");
						break;
					case 4:
						$(location).attr("href","friends.html");
						break;
					default:
						break;
				    }
				})
				
			})
			
			var onOff = true;
				
				function settings(onOff){
					if(onOff){
						$('#message_setting1').css('display','block');
						$('#message_setting2').css('display','block');
						
					}
					else{
						$('#message_setting1').css('display','none');
						$('#message_setting2').css('display','none');
						
					}
				}
					
					$('#person_message').find('li').eq(3).click(function(ev){
						onOff = true
						settings(onOff);
						
						return false;
					})
					
					$('#message_setting1').click(function(ev){
						onOff = false;
						settings(onOff);
						
						return false;
						
					})
				
				$('body').click(function(ev){
					onOff = false;
					settings(onOff);
					
				})

//好友
				$(".add_friends_bg").hide();
				$(".add_friends").hide();
				
				$("#friends_btn").click(function(){
					$(".add_friends_bg").show();
					$(".add_friends").show();
				})
				
				$(".add_friends_bg, .add_friends_header > span").click(function(){
					$(".add_friends_bg").hide();
					$(".add_friends").hide();
				});
				
//借款列表详情
				$(".lend_list_details_box2_page1").show();
				$(".lend_list_details_box2_page2").hide();
				
				
				$(".lend_list_details_box2_header").find('li').each(function(index,elem){
					$(this).click(function(){
						$(this).attr('class','lend_list_details_box2_header_status').siblings('li').attr('class','');
						switch (index){
							case 0:
							$(".lend_list_details_box2_page1").show();
							$(".lend_list_details_box2_page2").hide();
								break;
							case 1:
							$(".lend_list_details_box2_page1").hide();
							$(".lend_list_details_box2_page2").show();
								break;
							default:
								break;
						}
					})
					
					$(".personal_center_btn_bg1").find("p").click(function(){
						$(location).attr("href","private_letter.html");
					})
					
					$(".personal_center_btn_bg2").find("p").click(function(){
						$(location).attr("href","error.html");
					})
					
				})
				
//				我要投标按钮
				$(".BlackScreen").hide();
				$(".lend_list_details_box1_p2_btn_ev").hide();
				$("#lend_list_details_box1_p2_btn").click(function(){
					$(".BlackScreen").show();
					$(".lend_list_details_box1_p2_btn_ev").show();
				});
				
				$(".BlackScreen, .lend_list_details_box1_p2_btn_ev > h5 > span").click(function(){
					$(".BlackScreen").hide();
				$(".lend_list_details_box1_p2_btn_ev").hide();
				})
				
//注册

				//隐藏提示
				$('.register_main_message_tips').hide();
				$('.register_main_message_tips2').hide();
				
				//确认密码提示
				$('.register_main').find('input').eq(3).one({
					mousedown:function(){
				$('.register_main_message_tips').show();
						
						setTimeout(function(){
							$('.register_main_message_tips').hide();
							
						},3000)
					}
				})
				
				$('#register_main_btn').click(function(){
					
					$('.register_main').find('input[type = text], input[type = password], input[type = checkbox]').each(function(){
//						alert($('#register_main_checkbox').is(':checked'))
						var value = $(this).val();
							if(value == '' && $(this).attr('type') != 'checkbox'){
//								alert(value)
							$('.register_main_message_tips2').show();
								}
							
							else if($('#register_main_checkbox').is(':checked') == false){
							$('.register_main_message_tips2').show();
							}
							
							else{
							$('.register_main_message_tips2').hide();
							}
								
					
					})
					
				})
				
//封装一个 设置Cookie的函数：
function setCookie(key, value, t) {
	var oDate = new Date();
	oDate.setDate( oDate.getDate() + t );
	document.cookie = key + '=' + value + ';expires=' + oDate.toGMTString();
}

//封装一个 读取Cookie方法的函数：
function getCookie(key) {
	var arr1 = document.cookie.split('; ');
	for (var i=0; i<arr1.length; i++) {
		var arr2 = arr1[i].split('=');
		if ( arr2[0] == key ) {
			return decodeURI(arr2[1]);
		}
	}
}

//移除cookie
function removeCookie (key) {
setCookie(key, ' ', -1);
}
				
//退出
		$('#leave').click(function(){
			removeCookie('username');
			$(location).attr('href','index.html');
		})
		
//登录

		$("#entry_btn").click(function(){
			setCookie('username','123','5');
			$(location).attr("href","index.html");
		})
