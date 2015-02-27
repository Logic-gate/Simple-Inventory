from app import app
from flask import request, render_template, jsonify, abort, make_response, flash, url_for, send_from_directory
import re
import os
import json
from forms import product_submit
from werkzeug import secure_filename



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def data(sku, name, stock_location, company, place_of_origin, weight, stock, product, orig_stock):
	dict_ = {
    "PRODUCTS": [
        {
            "SKU": sku,
            "NAME": name,
            "STOCK_LOCATION": stock_location,
            "COMPANY": company,
            "PLACE_OF_ORIGIN": place_of_origin,
            "WEIGHT": weight,
            "STOCK": stock,
            "IMAGE": product,
            "ORIGINAL_STOCK": orig_stock
        },
      
    ]
}

	out = open('app/sku/sku_'+sku+'.data', 'w+')
	json.dump(dict_, out, indent=4)
	out.close()

@app.route('/')
def home():
	return render_template('home.html', title='SIMS', display='SYSBASE', display1='Inventory Managment System')

@app.route('/form', methods = ['GET', 'POST'])
def submit_form():
	sku_input = request.args.get('sku', None)
	quick = request.args.get('quick', None)
	form = product_submit()
	if request.method == 'POST':
			sku = request.form.get('sku', None)
			name = request.form.get('name', None)
			company = request.form.get('company', None)
			stock_location = request.form.get('stock_location', None)
			place_of_origin = request.form.get('place_of_origin', None)
			weight = request.form.get('weight', None)
			qty = request.form.get('qty', None)
			file = request.files['file']
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				data(sku, name, stock_location, company, place_of_origin, weight, qty, filename, qty)

			flash('Saved')
			return render_template('form.html', form=form, sku=sku, title=' ', display='Saved', display1=sku, extra=' ')

		


	elif request.method == 'GET':
		if sku_input is None:
			return render_template('form.html', form=form, title='Product Input', display='New', display1='Product', extra=' ', sku_default=' ', name_default=' ',
				weight_default=' ', company_default=' ', stock_default=' ', place_default=' ', qty_default=' ')
		elif sku_input is not None:
			

			if sku_input in open('app/sku/sku_'+sku_input+'.data').read() and quick is None:

				##DEFINE WH PRODUCTS

				a = open('app/sku/sku_'+sku_input+'.data')
				u = json.load(a)
							
				try:
					if u['PRODUCTS'][0]['SKU'] == sku_input:
						name = u['PRODUCTS'][0]['NAME']
						stock = u['PRODUCTS'][0]['STOCK_LOCATION']
						company = u['PRODUCTS'][0]['COMPANY']
						poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
						w = u['PRODUCTS'][0]['WEIGHT']
						stock_qty = u['PRODUCTS'][0]['STOCK']
						product = u['PRODUCTS'][0]['IMAGE']
						return render_template('form.html', form=form, title='Product Input', display='Edit', display1=sku_input, extra='Please Reselect The Image', sku_default=sku_input, name_default=name,
					weight_default=w, company_default=company, stock_default=stock, place_default=poo, qty_default=stock_qty)
				except u['PRODUCTS'][0]['SKU'] != sku_input:
						return 'NO SKU FOUND'


						#return u['PRODUCTS'][0]['SKU']
						#return render_template('index.html', stat=sku, Company_Name=u[sku]['NAME'], product='http://sysbase.org/check/images/'+i)


@app.route('/quick', methods = ['GET', 'POST'])
def quick():
	sku_input = request.args.get('sku', None)
	form = product_submit()
	a = open('app/sku/sku_'+str(sku_input)+'.data')
	u = json.load(a)
	if request.method == 'POST':
		q = request.form.get('qty', None)
		qty = int(u['PRODUCTS'][0]['STOCK']) - int(q)
		sku = u['PRODUCTS'][0]['SKU']
		name = u['PRODUCTS'][0]['NAME']
		stock = u['PRODUCTS'][0]['STOCK_LOCATION']
		company = u['PRODUCTS'][0]['COMPANY']
		poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
		w = u['PRODUCTS'][0]['WEIGHT']
		product = u['PRODUCTS'][0]['IMAGE']
		data(sku, name, stock, company, poo, w, qty, product, u['PRODUCTS'][0]['STOCK'])
		flash('Saved')
		return render_template('quick.html', form=form, sku=sku, title=' ', display='Saved', display1=sku, extra=' ', sku_default=sku_input, name_default=name, image=product, qty_default=qty)

	elif request.method == 'GET':
		if sku_input in open('app/sku/sku_'+sku_input+'.data').read():
			a = open('app/sku/sku_'+sku_input+'.data')
			u = json.load(a)
								
			try:
				if u['PRODUCTS'][0]['SKU'] == sku_input:
					name = u['PRODUCTS'][0]['NAME']
					product = u['PRODUCTS'][0]['IMAGE']
					stock_qty = u['PRODUCTS'][0]['STOCK']

					return render_template('quick.html', form=form, title='Product Input', display='Quick Edit', display1=sku_input, sku_default=sku_input, name_default=name, image=product, qty_default=stock_qty)

			except u['PRODUCTS'][0]['SKU'] != sku_input:
				return 'NO SKU FOUND'

@app.route('/all')
def view_products():
	product_path = 'app/sku/'
	f = []
	origin_sku = []
	company = []
	location = []
	name_of_product = []
	qty = []
	skus = []
	images = []
	orig_qty = []
	for (dirpath, dirnames, filenames) in os.walk(product_path):
		f.extend(filenames)
		break
	for dele in f:
		params = re.split('\W', dele)
		origin_sku.append(params[2])
		#company.append(params[1])
		location.append(params[0])

	# Count the products
	warehouse_products = len([ii for ii, s in enumerate(location) if 'sku_WH' in s])
	drop_shipping_products = len([ii for ii, s in enumerate(location) if 'sku_DS' in s]) 
	all_products = len(f)



	for name_of in f:
		a = open('app/sku/'+name_of)
		u = json.load(a)
		name = u['PRODUCTS'][0]['NAME']
		company_name = u['PRODUCTS'][0]['COMPANY']
		stock_qty = u['PRODUCTS'][0]['STOCK']
		sku = u['PRODUCTS'][0]['SKU']
		image = u['PRODUCTS'][0]['IMAGE']
		orig_qty_level = u['PRODUCTS'][0]['ORIGINAL_STOCK']
		name_of_product.append(name)
		company.append(company_name)
		qty.append(stock_qty)
		skus.append(sku)
		images.append(image)
		orig_qty.append(orig_qty_level)


	return render_template('all.html', title='All Products', display='Showing All Products', 
		product=zip(name_of_product, origin_sku, company, qty, skus, images, orig_qty), number_of_products=all_products, warehouse=warehouse_products, ds_products=drop_shipping_products)

 

@app.route('/product/check', methods = ['GET', 'POST'])
def index():
	sku = request.args.get('sku', None)
	company_name = ' '
	location = ' ' 
	if sku is None:
		try:
			abort(400)
		except:
			return make_response(jsonify({'error':'wrong param'}))

	elif sku is not None:
		if sku in open('app/sku/sku_'+sku+'.data').read():

				##DEFINE WH PRODUCTS

			sku_origin = re.findall('\d+', sku)
			for i in sku_origin:
				pass
			a = open('app/sku/sku_'+sku+'.data')
			u = json.load(a)
						
			try:
				if u['PRODUCTS'][0]['SKU'] == sku:
					name = u['PRODUCTS'][0]['NAME']
					stock = u['PRODUCTS'][0]['STOCK_LOCATION']
					company = u['PRODUCTS'][0]['COMPANY']
					poo = u['PRODUCTS'][0]['PLACE_OF_ORIGIN']
					w = u['PRODUCTS'][0]['WEIGHT']
					stock_qty = u['PRODUCTS'][0]['STOCK']
					product = u['PRODUCTS'][0]['IMAGE']
					orig_qty = u['PRODUCTS'][0]['ORIGINAL_STOCK']
					return render_template('index.html', title=sku, display=company, p_name=name, stock_location=stock, display1=poo, weight=w, qty=stock_qty,
														 product=product, orig_=orig_qty)
			except u['PRODUCTS'][0]['SKU'] != sku:
					return 'NO SKU FOUND'
						#return u['PRODUCTS'][0]['SKU']
						#return render_template('index.html', stat=sku, Company_Name=u[sku]['NAME'], product='http://sysbase.org/check/images/'+i)

		else:
			return 'Could not find SKU'

@app.route('/stat')
def stats():
	places = []
	f = []
	places_count = {}
	getPlaces = []
	location = []
	skus = []
	qty = []
	orig_qty = []
	product_path = 'app/sku/'
	#Get all unique places
	for (dirpath, dirname, filnames) in os.walk(product_path):
		f.extend(filnames)
		for ii in filnames:
			print ii
			i = open(product_path+ii)
			u=json.load(i)
			skus.append(str(u['PRODUCTS'][0]['SKU']))
			places.append(u['PRODUCTS'][0]['PLACE_OF_ORIGIN'])
			qty.append(int(u['PRODUCTS'][0]['STOCK']))
			orig_qty.append(int(u['PRODUCTS'][0]['ORIGINAL_STOCK']))
			i.close()
	for dele in f:
		params = re.split('\W', dele)
		location.append(params[0])
	for place in places:
		if place not in getPlaces:
			getPlaces.append(place)

	for o in getPlaces:
		places_count[o] = places.count(o)

	warehouse_products = len([ii for ii, s in enumerate(location) if 'sku_WH' in s])
	drop_shipping_products = len([ii for ii, s in enumerate(location) if 'sku_DS' in s]) 
	all_products = len(f)

	return render_template('stat.html', title='Stats', display='Showing All Products', number_of_products=all_products, 
		warehouse=warehouse_products, ds_products=drop_shipping_products, places=places_count, sku=str(skus), qty=str(qty), orig_qty=str(orig_qty))





    