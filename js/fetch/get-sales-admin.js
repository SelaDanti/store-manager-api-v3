let params = (new URL(document.location)).searchParams;
let id = params.get("user");
let saleUrl = `http://storemanage3000.herokuapp.com/api/v2/sales/${id}`;
let saleHead = `
<table>
			<tr>
				<th colspan="9" id="product-title">Sales</th>
			</tr>
			<tr id="hover-body">
				<th>ID</th>
				<th>Product price</th>
				<th>product id</th>
				<th>Total price</th>
			</tr>
`
window.addEventListener('load',setProducts)
function setProducts()
{
	fetch(saleUrl,{
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
			document.getElementsByClassName('table-product')[0].innerHTML = `
			${saleHead}
			<tr>
				<td colspan="8" class="center">${data['error']}</td>
			</tr>
			`;
			
		}
		else
		{
			let body = ``
			for (x in data)
			{
					let price = data[x]['products info'].slice(data[x]['products info'].lastIndexOf(':')+1,-2)
					let id = data[x]['products info'].slice(data[x]['products info'].indexOf(':')+1,data[x]['products info'].indexOf(','))
					body += `
				<tr>
				<td>${data[x]['id']}</td>
				<td>${price}</td>
				<td>${id}</td>
				<td class="salePrice">${data[x]['total sale']}</td>
				</tr>
				`;
			}
			document.getElementsByClassName('table-product')[0].innerHTML = `
			${saleHead}
			${body}
			`;
			calcSale()
			
			
			
		}
	})
	.catch((error) => {console.log(error)})
}

function calcSale()
{
	let index  = 0;
	let salesPrice = document.getElementsByClassName('salePrice')
	let total = 0;
	while (index < salesPrice.length)
	{
		total += parseInt(salesPrice[index].innerHTML);
		index++;
	} 
	document.getElementById('sale-record').innerHTML = index;
	document.getElementById('sale-worth').innerHTML = total;
}