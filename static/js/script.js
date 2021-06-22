//Для кнопок изменить Контакт
edc=document.getElementsByClassName('edc');
for(i=0;i<edc.length;i++){
	edc[i].onclick=function(){
		eblock=document.getElementById('ListContact');
		eblock.style.display="none";
		sblock=document.getElementById('EditContact');
		sblock.style.display="block";
		con=this.value;
		$.ajax({
			type:'POST',
			async:false,
			url:'/info_contact',
			dataType:'json',
			data:{
				'cid':con
			},
			timeout:3000,
			error:function(xhr,status,error){
				console.log(xhr);
				console.log(status);
				console.log(error);
			},
			success:function(result){
				if(result['status']!=0){
					eId=document.getElementById('edId');
					eId.value=result['id'];
					eicons=document.getElementsByName('eicons');
					for(j=0;j<eicons.length;j++){
						for(k=0;k<result['icons'].length;k++){
							if(eicons[j].value==result['icons'][k]){
								eicons[j].checked=true;
							}
						}
					}
				} else {
					alert(result['msg']);
				}
				console.log(result)
			}
		});
	}
}
document.getElementById('btnAboutEdit').onclick=function(){
	eblock=document.getElementById('EditAbout');
	eblock.style.display = "block";
	sblock=document.getElementById('ShowAbout');
	sblock.style.display = "none";
}
document.getElementById('btnCancelAbout').onclick=function(){
	eblock=document.getElementById('EditAbout');
	eblock.style.display = "none";
	sblock=document.getElementById('ShowAbout');
	sblock.style.display = "block";
}
document.getElementById('btnShowAbout').onclick=function(){
	eblock=document.getElementById('EditAbout');
	eblock.style.display = "none";
	sblock=document.getElementById('ShowAbout');
	sblock.style.display = "block";
}
$('#btnDeleteAbout').on('click',function(){
	about_id=$('#frmEditAbout').find('#about_id').val();
	if(about_id!=''||about_id!=None){
		var res=$.ajax({
			url:'/deleteAbout',
			type:'POST',
			data:{
				'id':about_id
			},
			dataType:'JSON'
		});
		res.done(function(msg){
			alert(msg.msg);
		});
		res.fail(function(jqXHR, textStatus){
			//alert('error'+jqXHR+' '+textStatus);
			console.log(jqXHR);
			console.log(textStatus);
		})
	}else{
		alert('Нет общей информации по данной дате!!');
	}
});
$('#btnAddCont').on('click',function(){
	$('#winType').val("1");
	$('#AdminModalLabel').html('Новый контакт');
});
$('#AdminModal').on('shown.bs.modal', function (e) {
	console.log('fasdfafd');
	t=$("#winType").val();
	console.log(t);
})
