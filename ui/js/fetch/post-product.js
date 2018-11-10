productsUrl = `http://0.0.0.0:5000/api/v2/products`

document.getElementsByClassName('btn-main')[0].addEventListener('click',postProduct)
function postProduct()
{
	let name = document.getElementById('name').value;
	let inventoryQuantity = parseInt(document.getElementById('inventoryQuantity').value);
	let MIQ = parseInt(document.getElementById('MIQ').value);
	let category = parseInt(document.getElementById('category').value);
	let uom = document.getElementById('uom').value;
	let price = parseInt(document.getElementById('price').value);
	let payload = {
	  "miq": MIQ,
	  "price": price,
	  "category id": category,
	  "quantity": inventoryQuantity,
	  "product name": name,
	  "uom": uom
	}
	fetch(productsUrl,{
		"method":"POST",
    	"mod":"cors",
    	headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
    	},
    	body:JSON.stringify(payload)
	})
	.then((res) => {status = res.status; return res.json()})
	.then((data) => {
		if (status != 201)
		{
			document.getElementById('error').innerHTML = `Error ${data['error']}`;
			document.getElementById('error').style.display = 'block'
			document.getElementById('success').style.display = 'none'
		}
		else
		{
			document.getElementById('success').innerHTML = data['message'];
			document.getElementById('error').style.display = 'none'
			document.getElementById('success').style.display = 'block'
		}
	})
	.catch((error) => {console.log(error)})
}