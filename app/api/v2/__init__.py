from flask import Blueprint
from flask_cors import CORS
from flask_restplus import Api

from .view.users import ns_auth, ns_attendant
from .view.products import ns_category, ns_products
from .view.cart import ns_cart
from .view.sales import ns_sale

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

app_v2 = Blueprint('app_v2',__name__,url_prefix='/api/v2')
CORS(app_v2)
api_v2 = Api(app_v2,title='Store Manager',version='2.0',description='Store management api v3',
	authorizations=authorizations)

api_v2.add_namespace(ns_auth)
api_v2.add_namespace(ns_attendant)
api_v2.add_namespace(ns_category)
api_v2.add_namespace(ns_products)
api_v2.add_namespace(ns_cart)
api_v2.add_namespace(ns_sale)