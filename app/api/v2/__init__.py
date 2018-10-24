from flask import Blueprint
from flask_restplus import Api

from .view.users import ns_user, ns_attendant
from .view.sales import ns_sales
from .view.products import ns_products, ns_categories


app_v2 = Blueprint('app_v2',__name__,url_prefix='/api/v2')
api_v2 = Api(app_v2,title='Store Manager',version='2.0',description='Store management api v2')

api_v2.add_namespace(ns_user)
api_v2.add_namespace(ns_attendant)
api_v2.add_namespace(ns_sales)
api_v2.add_namespace(ns_products)
api_v2.add_namespace(ns_categories)