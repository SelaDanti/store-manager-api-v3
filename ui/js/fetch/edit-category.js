let params = (new URL(document.location)).searchParams;
let id = params.get("categoryId");
let url = `http://storemanage3000.herokuapp.com/api/v2/category/${id}`;

window.addEventListener('load',setCategory)

function setCategory()
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
		document.getElementById('oldCategory').innerHTML = data['name']
	})
	.catch((error) => {console.log(error)})
}

document.getElementsByClassName('btn-main')[1].addEventListener('click',updateCategory)

function updateCategory()
{
	let categoryName = document.getElementById('newCategory').value;
	let payload = {"category name": categoryName}
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
	.then((data) => {setCategory()})
	.catch((error) => {console.log(error)})
}
