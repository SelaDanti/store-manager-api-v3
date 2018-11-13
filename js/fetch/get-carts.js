let productUrl = `http://storemanage3000.herokuapp.com/api/v2/products`;
let cartUrl = `http://storemanage3000.herokuapp.com/api/v2/cart`;
let saleUrl = `http://storemanage3000.herokuapp.com/api/v2/sales`;
let productHead = `
<table>
			<tr>
				<th colspan="9" id="product-title">Lists of products</th>
			</tr>
			
			<tr id="hover-body" class="margin-top-40">
				<th>ID</th>
				<th>Product Name</th>
				<th>UOM</th>
				<th>price</th>
				<th>Quantity</th>
			</tr>
`;
let cartHead = `
		<h1>My Cart</h1>
		<table>
			<tr>
				<th colspan="5" id="cart-title">TOTAL COST: 2000ksh</th>
			</tr>
			<tr id="hover-body" class="margin-top-40">
				<th>Product Id</th>
				<th>item price</th>
				<th>quantity</th>
				<th>sub total</th>
			</tr>
`;
let cartEnd = `
	<tr>
				<th colspan="5" id="product-end">
				<button class="btn-ok">CHECKOUT</button>
				</th>
			</tr>
`;
window.addEventListener('load',function(){setProducts();setCart();})
function setProducts()
{
	fetch(productUrl,{
		"method": "GET",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		}
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		if (status != 200)
		{
			if (data['error'] == 'token is invalid')
			{
				window.location.replace('../index.html');
			}
			document.getElementsByClassName('table-product')[0].innerHTML = `
			${productHead}
			<tr>
				<td colspan="8" class="center">${data['error']}</td>
			</tr>
			`
		}
		else
		{
			let body = ``
			for (x in data)
			{
				body += `
				<tr>
				<td>${data[x]['id']}</td>
				<td>${data[x]['product name']}</td>
				<td>${data[x]['miq']}</td>
				<td>${data[x]['price']} KSH</td>
				<td>${data[x]['quantity']}</td>
				</tr>
				`;
			}
			document.getElementsByClassName('table-product')[0].innerHTML = `
			${productHead}
			${body}
			`;
		}
	})
	.catch((error) => {console.log(error)})
}
function setCart()
{
	fetch(cartUrl,{
		"method": "GET",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		}
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		if (status != 200)
		{
			document.getElementsByClassName('table-product')[1].innerHTML = `
			${cartHead}
			<tr>
				<td colspan="8" class="center">${data['error']}</td>
			</tr>
			`;
			document.getElementById('cart-title').innerHTML = `TOTAL COST: 0 KSH`;
		}
		else
		{
			let body = ``
			for (x in data)
			{
				if (x != 0)
				{
					body += `
				<tr>
				<td>${data[x]['product id']}</td>
				<td>${data[x]['price']} KSH</td>
				<td>${data[x]['quantity']}</td>
				<td class="sub-total">${data[x]['quantity'] * data[x]['price']}</td>
				<td><a href="delete-cart.html?cartId=${data[x]['product id']}" class="btn-category">remove</a></td>
				</tr>
				`;}
			}
			document.getElementsByClassName('table-product')[1].innerHTML = `
			${cartHead}
			${body}
			${cartEnd}
			`;
			let subTotal = document.getElementsByClassName('sub-total')
			let total = 0;
			let index = 0;
			while (index < subTotal.length)
			{
				total += parseInt(subTotal[index].innerHTML);
				index++;
			}
			document.getElementById('cart-title').innerHTML = `TOTAL COST: ${total} KSH`;
			document.getElementsByClassName('btn-ok')[0].addEventListener('click',makeSale);
		}
	})
	.catch((error) => {console.log(error)})	
}

document.getElementsByClassName('btn-category')[0].addEventListener('click',addCart)
function addCart()
{
	let id = parseInt(document.getElementById('id').value);
	let quantity = parseInt(document.getElementById('quantity').value);
	let payload = {"product id": id,"quantity": quantity}
	fetch(cartUrl,{
		"method": "POST",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		},
		body: JSON.stringify(payload)
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		if (status != 201)
		{
			document.getElementById('error').innerHTML = data['error'];
			document.getElementById('error').style.display = 'block';
		}
		else
		{
			document.getElementById('error').style.display = 'none';
			setCart();
			setProducts();
		}
	})
	.catch((error) => {console.log(error)})
}


function makeSale()
{
	fetch(saleUrl,{
		"method": "POST",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		},
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		item = document.getElementsByClassName('cart-box')
		item[0].innerHTML = `<div class="table-product  margin-top-20">
			<h1>My Cart</h1>
			<br>
			<div class="confirm center">
				<h1>Item Purchased</h1>
				<button onclick="location.reload();">OK</button>
			</div>
			</div>`;
	})
	.catch((error) => {console.log(error)})
}
