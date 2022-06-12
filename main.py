from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from flask_cors import CORS
import json
from json import JSONEncoder
from flasgger import Swagger, LazyString, LazyJSONEncoder

app = Flask(__name__)
api = Api(app)
CORS(app)

app.json_encoder = LazyJSONEncoder

swagger = Swagger(app, template_file='Swagger.json')

class status (Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


class Sum(Resource):
    def get(self, a, b):
        return jsonify({'data': a+b})

class Send (Resource):
    def post(self):
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']
        #args = parser.parse_args()
        #un = str(args['username'])
        #pw = str(args['password'])
        return jsonify(u=un, p=pw)		

class AuthToken (Resource):
    def post(self):
        json_data = request.get_json(force=True)
        client_id = json_data['client_id']
        client_secret = json_data['client_secret']
        grant_type = json_data['grant_type']
        scope = json_data['scope']
        
        if(client_id=='45a6209ff442402588224f59a641d82b' and client_secret=='XeiWbI7gGodalrzk'):
		  #success
          res = {"access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Il9kZWZhdWx0IiwidHlwIjoiSldUIn0","token_type": "Bearer", "expires_in": 604799}
          return jsonify(res)
        else:
          #failed
          #res = {"access_token" : None}
          return abort(401)

def checkToken(hdtoken):
    if(hdtoken == "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Il9kZWZhdWx0IiwidHlwIjoiSldUIn0"):
       return True
    else:
       return False	
		  
class MenuList (Resource):
    def get(self):
        authhd = request.headers.get('Authorization')
        #print(authhd)
        if(checkToken(authhd)):
           args = request.args
           id = args['merchantID']
           f = open('menu.json')
           datas = json.load(f)
           res = {'kode':'err','pesan':'user not found'}
           for data in datas:
              if(data['merchantID'] == id):
                 res = data
           return jsonify(res)
        else:
           return abort(401)           		  

class SubmitOrder (Resource):
    def post(self):
        authhd = request.headers.get('Authorization')
        if(checkToken(authhd)):
           json_data = request.get_json(force=True)
           orderID = json_data['orderID']
           print("Order data received: "+orderID)
           return '', 204
        else:
           return abort(401)

class PushOrderState (Resource):
    def put(self):
        authhd = request.headers.get('Authorization')
        if(checkToken(authhd)):
           json_data = request.get_json(force=True)
           orderID = json_data['orderID']
           print("Order data updated: "+orderID)
           return '', 204
        else:
           return abort(401)
		   
class Menu (Resource):
    def get(self):
        args = request.args
        id = args['merchantID']
        print(id)
        f = open('menu.json')
        datas = json.load(f)
        res = {'kode':'err','pesan':'user not found'}
        for data in datas:
           if(data['merchantID'] == id):
              res = data
        return jsonify(res)

class Store (Resource):
    def get(self):
        args = request.args
        id = args['merchantID']
        print(id)
        f = open('store.json')
        datas = json.load(f)
        res = {'kode':'err','pesan':'user not found'}
        for data in datas:
           if(data['merchantID'] == id):
              res = data
        return jsonify(res)
		
class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()

class Category(JsonSerializable):
  def __init__(self, code, desc):
    self.code = code
    self.desc = desc

class Response(JsonSerializable):
  def __init__(self, lsdata):
    self.data = lsdata	

def getCategory(code, desc):
        res = {"code":code, "desc":desc}
        return res

def getDict(id, name):
        res = {"id":id, "name":name}
        return res

def getItemDict(merchantid, items):
        res = {"merchantid":merchantid, "items":items}
        return res		

class Kategori (Resource):
    def get(self):
        lskategori = []
        kategori = getCategory('A001','Makanan Pokok')		
        lskategori.append(kategori)
        kategori2 = getCategory('A002','Buah')
        lskategori.append(kategori2)
        return jsonify(lskategori)

class ProductCategory (Resource):
    def get(self):
        f = open('product-category.json')
        datas = json.load(f)      
        return jsonify(datas)

class ProductSubcategory (Resource):
    def get(self):
        args = request.args
        id = args['categoryID']
        f = open('product-category.json')
        datas = json.load(f)
        subcategories=[]
        for data in datas:
           if(data['id'] == id):
              subcategories=data['subCategories']		   
        return jsonify(subcategories)		

class ProductItems (Resource):
    def get(self):
        args = request.args
        id = args['subcategoryID']
        items = []
        f = open('store.json')
        datas = json.load(f)
        for data in datas:
           for sec in data['sections']:
              categs = sec['categories']
              for cat in categs:
                 subcategs = cat['subCategories']
                 for subcat in subcategs:
                    if(subcat['id'] == id):
                       items.extend(subcat['items'])
        return jsonify(items)

class ProductItems2 (Resource):
    def get(self):
        args = request.args
        id = args['subcategoryID']
        items = []
        f = open('store.json')
        datas = json.load(f)
        for data in datas:
           for sec in data['sections']:
              categs = sec['categories']
              for cat in categs:
                 subcategs = cat['subCategories']
                 for subcat in subcategs:
                    if(subcat['id'] == id):
                       item = getItemDict(data['merchantID'], subcat['items'])
                       items.append(item)
        return jsonify(items)		

class ComodityItems (Resource):
    def get(self):
        args = request.args
        id = args['zoneId']
        demands = []
        f = open('comodity.json')
        datas = json.load(f)
        for data in datas:
           for cities in data['cities']:
              zones = cities['zones']
              for zone in zones:                 
               if(zone['zoneId'] == id):
                  demands.extend(zone['demands'])
        return jsonify(demands)

class ComodityProv (Resource):
    def get(self):
        args = request.args
        id = args['provId']
        demands = []
        f = open('comodity.json')
        datas = json.load(f)
        for data in datas:
          if(data['provinceId'] == id):
             demands = data
        return jsonify(demands)		

class ComodityCity (Resource):
    def get(self):
        args = request.args
        id = args['cityId']
        demands = []
        f = open('comodity.json')
        datas = json.load(f)
        for data in datas:
           for city in data['cities']:
              if(city['cityId'] == id):
                 demands = city 
        return jsonify(demands)
		
api.add_resource(status, '/')
api.add_resource(Sum, '/add/<int:a>,<int:b>')
api.add_resource(Send, '/send')
api.add_resource(Menu, '/menu')
api.add_resource(Store, '/store')
api.add_resource(ProductCategory, '/product/category')
api.add_resource(ProductSubcategory, '/product/subcategory')
api.add_resource(ProductItems, '/product/items')
api.add_resource(ProductItems2, '/product/merchant_items')
api.add_resource(ComodityItems, '/predictor/demands/zone')
api.add_resource(ComodityProv, '/predictor/demands/prov')
api.add_resource(ComodityCity, '/predictor/demands/city')
api.add_resource(AuthToken, '/grab-ep/oauth/token')
api.add_resource(MenuList, '/grab-ep/merchant/menu')
api.add_resource(SubmitOrder, '/grab-ep/orders')
api.add_resource(PushOrderState, '/grab-ep/order/state')
api.add_resource(Kategori, '/kategori')

if __name__ == '__main__':
    app.run()