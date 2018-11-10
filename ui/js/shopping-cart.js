function removeItem()
{
	item = document.getElementsByClassName('cart-box')
	item[0].innerHTML = `<div class="table-product  margin-top-20">
		<h1>My Cart</h1>
		<br>
		<div class="confirm center">
			<h1>Do you want to remove item?</h1>
			<button onclick="backToCart()">OK</button><button onclick="backToCart()">Cancel</button>
		</div>
		</div>`
}

function backToCart()
{
	item = document.getElementsByClassName('cart-box')
	item[0].innerHTML = `<div class="table-product  margin-top-20">
		<h1>My Cart</h1>
		<table>
			<tr>
				<th colspan="5" id="product-title">TOTAL COST: 2000ksh</th>
			</tr>
			<tr id="hover-body">
				<th>Name of Product</th>
				<th>Item Price</th>
				<th>quantity</th>
				<th>sub total</th>
				<th></th>
			</tr>
			<tr>
				<td>Kiwi</td>
				<td>50 ksh</td>
				<td>3</td>
				<td>150</td>
				<td><button class="btn-remove" onclick="removeItem()">Remove</button></td>
			</tr>
			<tr>
				<td>Kiwi</td>
				<td>50 ksh</td>
				<td>3</td>
				<td>150</td>
				<td><button class="btn-remove" onclick="removeItem()">Remove</button></td>
			</tr>
			<tr>
				<th colspan="5" id="product-end">
				<button class="btn-ok" onclick="checkOut()">CHECKOUT</button>
				<button class="btn-danger" onclick="removeAll()">CLEAR CART</button>
				</th>
			</tr>
		</table>
	</div>`
}

function removeAll()
{
	item = document.getElementsByClassName('cart-box')
	item[0].innerHTML = `<div class="table-product  margin-top-20">
		<h1>My Cart</h1>
		<br>
		<div class="confirm center">
			<h1>Do you want to remove All item?</h1>
			<button onclick="backToCart()">OK</button><button onclick="backToCart()">Cancel</button>
		</div>
		</div>`
}

function checkOut()
{
	item = document.getElementsByClassName('cart-box')
	item[0].innerHTML = `<div class="table-product  margin-top-20">
		<h1>My Cart</h1>
		<br>
		<div class="confirm center">
			<h1>Item Purchased</h1>
			<button onclick="backToCart()">OK</button>
		</div>
		</div>`
}