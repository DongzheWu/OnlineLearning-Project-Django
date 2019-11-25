
(function($) {

	var defaults  = {
		width :580,
		eventType: "click",
		dropmenu:".xmenu",
		hiddenID : "selectposhidden",
		emptytext: "Please select"
	};
	
	$.fn.xMenu = function(options) {
		return $(this).each(function() {
		
			var owl = $.extend({}, defaults, options || {});

			var $this = $(this);

			var $span = $this.find("span");

			var $dropmenu= $(owl.dropmenu);

			var $Hd = $("#"+owl.hiddenID);

			//var $mli = $("dl li",$dropmenu);
			var $mli = $("dl li",$dropmenu);

			var $closebtn =$(".m-close", $dropmenu);			

			var $selectinfo = $(".select-info",$dropmenu);

			var $selectUl = $("ul",$selectinfo);

			var $okbtn = $("a[name='menu-confirm']",$selectinfo);
			

			//$("dl dt",$dropmenu).toggle(function(){
			//	var $this = $(this);
			//	if($this.hasClass('open')){
			//		$this.removeClass('open').next().slideUp('fast');
			//	}else{
			//		$this.addClass('open').next().slideDown('fast');
			//	}
			//} , function(){
			//	$(this).removeClass('open').next().slideUp('fast');
			//});
			

			$closebtn.click(function(){
				 $.powerFloat.hide();
			});

			$okbtn.click(function(){
				//var $li =$selectUl.find("li");
				var $li =$selectUl.find("li");
				var name = "";
				var id = "";			
				$li.each(function(){
					_this = $(this);
					name += _this.text()+",";
					id +=  _this.attr("rel")+",";
				})
				name = name.substring(0,name.length-1);
				id = id.substring(0,id.length-1);
				
				if(name.length>10){
					$span.attr({"title":name});
					name =name.substring(0,10)+"...";
				}
				
				$span.text(name);
				$Hd.val(id);
				$.powerFloat.hide();
			});
			
			

			$mli.click(function(){
				var $li = $(this);
				var val  =$li.text();
				var id  = $li.attr("rel");

				if($selectinfo.is(":hidden")){
					$selectinfo.show();
				}
				if($li.hasClass("current")){
					$selectUl.find("li[rel='"+id+"']").remove();					
					$li.removeClass("current");
					$(this).find('input').prop('checked',false);
				}else{					
					$("<li rel='"+id+"' class='current'>"+val+"</li>").appendTo($selectUl);
					$li.addClass("current");
					$(this).find('input').prop('checked',true);
				}				
				if($selectUl.children("li").length==0){
					$selectinfo.hide();
				}
			});
			

			$("li",$selectUl).on('click',function(){
				var $li = $(this);
				var id  = $li.attr("rel");
				$mli.filter("li[rel='"+id+"']").removeClass("current");	
				$li.remove();
				if($selectUl.children("li").length==0){
					$selectinfo.hide();
				}
			});
			
			
			
			
			
			

			$this.powerFloat({
				width: owl.width,
				eventType: owl.eventType,
				offsets: {
					x: 0,
					y: -1 
				},
				target: $dropmenu, 	 		
				showCall: function(){ 				

					setCurrentItem($Hd.val());					
					$this.addClass("menu-open");
				},
				hideCall:function(){
					$this.removeClass("menu-open");
					if($selectUl.children("li").length==0){
						$span.text(owl.emptytext);
						$Hd.val("");
					}
				}
			});

			var setCurrentItem = function (val){				
				if(val&&val!=""){
					$mli.removeClass("current");
					var array = val.split(",");
					$selectUl.empty();
					for(var i=0;i<array.length;i++){
						var $cli = $mli.filter("li[rel='"+array[i]+"']");
						$cli.addClass("current");
						$("<li rel='"+array[i]+"' class='current'>"+$cli.text()+"</li>").appendTo($selectUl);
					}					
				}else{
					$selectinfo.hide();
				}
				
			}			
		});
	};
	

	
	
})(jQuery);