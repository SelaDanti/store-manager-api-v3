let params = (new URL(document.location)).searchParams;
let id = params.get("productId");
let url = `http://storemanage3000.herokuapp.com/api/v2/products/${id}`;

window.addEventListener('load',setProduct)
function setProduct()
{
	fetch(url,{
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
		document.getElementById('oldName').innerHTML = data['product name'];
		document.getElementById('oldQuantity').innerHTML = data['quantity'];
		document.getElementById('oldMiq').innerHTML = data['miq'];
		document.getElementById('oldCategory').innerHTML = data['category id'];
		document.getElementById('oldPrice').innerHTML = data['price'];
		document.getElementById('oldUom').innerHTML = data['uom'];
	})
	.catch((error) => {console.log(error)})
}

document.getElementsByClassName('btn-main')[1].addEventListener('click',updateProduct)
function updateProduct()
{
	let name = document.getElementById('newName').value;
	let quantity = document.getElementById('newQuantity').value;
	let miq = document.getElementById('newMiq').value;
	let category = document.getElementById('newCategory').value;
	let price = document.getElementById('newPrice').value;
	let uom = document.getElementById('newUom').value;
	let payload = {
	  "miq": parseInt(miq),
	  "price": parseInt(price),
	  "category id": parseInt(category),
	  "quantity": parseInt(quantity),
	  "product name": name,
	  "uom": uom
	}
	fetch(url,{
		"method": "PUT",
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
		console.log(data)
		if (status != 201)
		{
			document.getElementById('error').innerHTML = data['error'];
			document.getElementById('error').style.display = 'block';
		}
		else
		{
			setProduct()
			document.getElementById('error').style.display = 'none';
		}
	})
	.catch((error) => {console.log(error)}) 
}