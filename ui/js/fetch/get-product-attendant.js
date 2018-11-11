let productUrl = `http://0.0.0.0:5000/api/v2/products`;
let productHead = `
<table>
			<tr>
				<th colspan="9" id="product-title">Lists of products</th>
			</tr>
			<tr id="hover-body">
				<th>ID</th>
				<th>Product Name</th>
				<th>Inventory Quantity</th>
				<th>M.I.Q</th>
				<th>Category</th>
				<th>UOM</th>
				<th>price</th>
			</tr>
`
window.addEventListener('load',setProducts)
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
				<td>${data[x]['quantity']}</td>
				<td>${data[x]['miq']}</td>
				<td>${data[x]['category id']}</td>
				<td>${data[x]['uom']}</td>
				<td>${data[x]['price']} KSH</td>
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