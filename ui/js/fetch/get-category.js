let categoryUrl = `http://storemanage3000.herokuapp.com/api/v2/category`;
window.addEventListener('load',getCategories)
let categoryHead = `
<table>
			<tr>
				<th colspan="5" id="product-title">Category</th>
			</tr>
			<tr id="hover-body">
				<th>ID</th>
				<th>Category Name</th>
				<th></th>
				<th></th>
			</tr>
`
function getCategories()
{
	fetch(categoryUrl,{
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
			document.getElementById('category-lists').innerHTML = `
			${categoryHead}
			<tr>
			<td colspan="3" class="center">${data['error']}</td>
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
				<td>${data[x]['name']}</td>
				<td>
				<a href="../admin/edit-category.html?categoryId=${data[x]['id']}" class="btn-edit">edit</a>
				</td>
				<td>
				<a href="../admin/delete-category.html?categoryId=${data[x]['id']}" class="btn-remove">delete</a>
				</td>
				</tr>
				`
			}
			document.getElementById('category-lists').innerHTML = `
			${categoryHead} ${body}
			`
			console.log(data)
		}
	})
}

document.getElementsByClassName('btn-main')[0].addEventListener('click',addCategory)

function addCategory()
{
	let categoryName = document.getElementById('category').value;
	let payload = {"category name": categoryName}
	fetch(categoryUrl,{
		"method": "POST",
		"mod": "cors",
		headers: {
		"Content-type": "application/json",
		"Access-Control-Allow-Origin":"*",
		"X-API-KEY": localStorage.getItem('token')
		},
		body: JSON.stringify(payload)
	})
	.then((res) => {status =res.status; return res.json()})
	.then((data) => {
		if (status != 201)
		{
			document.getElementById('error').innerHTML = data['error'];
			document.getElementById('error').style.display = 'block';
		}
		else
		{	
			getCategories()
		}
	})
}