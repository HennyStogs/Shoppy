$(document).ready(function(){
  $(document).on('click', '#addToCartButton', function(){
		var _vm=$(this);
    var _quantity=$("#productquantity").val();
    var _itemid=$(".item-id").val();
    var _itemname=$(".item-name").val();
    var _itemprice=$(".item-price").val();
    var _itemimage=$(".item-image").val();
    
    $.ajax({
			url:'/addtocart',
			data:{
				'id':_itemid,
        'image':_itemimage,
				'quantity':_quantity,
				'name':_itemname,
				'price':_itemprice
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-icon").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});
  });

  $(document).on('click','.delete-item',function(){
		var _itemid=$(this).attr('data-item');
    console.log(_itemid)
		var _vm=$(this);
		
		$.ajax({
			url:'/deletefromcart',
			data:{
				'id':_itemid,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-icon").text(res.totalitems);
				_vm.attr('disabled',false);
        $("#cartlist").html(res.data);
			}
		});		
	});

  $(document).on('click','.update-item',function(){
		var _itemid=$(this).attr('data-item');
    var _itemquantity=$(".item-quantity-"+_itemid).val();
    console.log(_itemid)
		var _vm=$(this);
		
		$.ajax({
			url:'/updatecart',
			data:{
				'id':_itemid,
        'quantity': _itemquantity
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				_vm.attr('disabled',false);
        $("#cartlist").html(res.data);
			}
		});	
	});
});