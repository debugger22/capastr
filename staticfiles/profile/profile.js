$(document).ready(function () {
	var on_list = null;
	$('#updatable_list li').not('.close-btn').click(function (event){
		//var list_items = ['name','email','mobile','tags']
		if(event.target.id!="tags")
			$(this).css({'height':'80px','background':'rgb(210,210,250)'});
		else{
			$(this).css({'height':'150px','background':'rgb(210,210,250)'});
		}
		$("#"+event.target.id+"_form").css({'display':'block'});
		$("#"+event.target.id+"_close").css({'display':'block'});
		//var index = list_items.indexOf(event.target.id);
		//if (index > -1) {
		//    list_items.splice(index, 1);
		//}
		//for(var i=0;i<list_items.length;i++){
		//	$('#'+list_items[i]).css({'height':'30px','background':'rgb(240,240,240)'});
		//	$("#"+list_items[i]+"_form").css({'display':'none'});
		//}
	}).children().not('input').click(function(e){
			$('#'+$(this).data('for')).css({'height':'30px','background':'rgb(240,240,240)'});
			$("#"+$(this).data('for')+"_form").css({'display':'none'});
			$("#"+$(this).data('for')+"_close").css({'display':'none'});		
	});

	$('.close-btn').click(function (event){
			$('#'+$(this).data('for')).css({'height':'30px','background':'rgb(240,240,240)'});
			//$("#"+$(this).data('for')+"_form").css({'display':'none'});
			//$("#"+$(this).data('for')+"_close").css({'display':'none'});
	})

});