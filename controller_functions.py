from flask import Flask, render_template, redirect, flash, request, session, jsonify, json
from config import app, db, func, IntegrityError, bcrypt, re, randint
from models import customer, shipping_address, billing_address, order, order_item, product, product_category, category, wishlist

listofviewed = []
cart = []
ordertotal = 0

#OUTSIDEFUNCTIONS

def onLoad(x):
    if checkdups(x):
        listofviewed.append(session["viewed"])
    updaterecently()

def updaterecently():
    if (int(len(listofviewed)) > int(6)):
        for i in range(6):
            temp = listofviewed[i]
            listofviewed[i] = listofviewed[i+1]
            listofviewed[i+1] = temp
        listofviewed.pop()
        print(session["viewed"])
    return

def checkdups(x):
    for i in range(len(listofviewed)):
        if listofviewed[i] == x:
            return False
    return True

#RENDERHOMEPAGE
def homepage():
    global listofviewed
    global cart
    updaterecently()
    allproducts = product.query.all()
    return render_template("home.html", listofviewed = listofviewed, allproducts = allproducts, cart = cart)

#LOGIN/REG
def register():
    validation_check = customer.validate_customer(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Registration unsuccessful. Please Try Again!")
        return redirect("/myaccount")
    else:
        try:
            new_customer = customer.add_new_customer(request.form)
            return redirect("/myaccount")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. This email already exists! Please Try Again!")
            return redirect("/myaccount")

def email():
    found = False
    precheck_email = customer.query.filter_by(email = request.form["email"]).all()
    if precheck_email:
        found = True
    return render_template("partials/email.html", found=found)

def login():
    login_user = customer.query.filter_by(email = request.form["email"]).all()

    if login_user:
        session['user_id'] = login_user[0].id
        session['first_name'] = login_user[0].first_name
        session['last_name'] = login_user[0].last_name
        hashed_password = login_user[0].password
        if bcrypt.check_password_hash(hashed_password, request.form['password']):
            session["logged_in"] = True
            session['user_id'] = login_user[0].id
            flash("You are logged in!")
            return redirect('/myaccount')
        else:
            session["logged_in"] = False
            flash("You could not be logged in. Try again or register")
        return redirect("/myaccount")
    else:
        flash("Email was not found. Please try again.")
        return redirect("/myaccount")
    return redirect("/myaccount")

def logout():
    global cart
    session['logged_in'] = False
    session.clear()
    cart = []
    flash("You have been logged out.")
    return redirect("/myaccount")

def myaccount():
    global cart
    try:
        if session['user_id']:
            return redirect("/accountinfo")
    except:
        flash("Please login or register to continue.")
        return render_template("loginreg.html", cart = cart)

def accountinfo():
    global listofviewed
    global cart
    updaterecently()
    login_id = session['user_id']
    first_name = session['first_name']
    last_name = session['last_name']
    customerinfo = db.session.query(customer).filter(customer.id == login_id)
    allproducts = product.query.all()
    allorders = db.session.query(product, order_item, order).filter(product.id == order_item.product_id).filter(order_item.order_id == order.id).filter(order.customer_id == login_id).all()
    print(allorders)
    alladdresses = db.session.query(shipping_address).filter(shipping_address.customer_id == login_id).all()
    return render_template("account.html", listofviewed = listofviewed, allproducts = allproducts, allorders = allorders, first_name = first_name, last_name = last_name, alladdresses = alladdresses, customerinfo = customerinfo, login_id = login_id, cart = cart)

def editaccountinfopage(login_id):
    global cart

    login_id = login_id
    customer_update = customer.query.get(login_id)
    print(customer_update)
    first_name = customer_update.first_name
    last_name = customer_update.last_name
    phone_number = customer_update.phone_number
    return render_template("editcustomerinfo.html", login_id = login_id, first_name = first_name, last_name = last_name, phone_number = phone_number, cart = cart)

def editaccount(login_id):
    login_id = login_id
    validation_check = customer.validate_edit_customer(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/editcustomerinformation/"+str(login_id)+"")
    else:
        edit_customer = customer.edit_customer(request.form)
        return redirect("/accountinfo")

#SHIPPINGADDRESS
def editaddresspage(address_id):
    global cart

    address_id = address_id
    shipping_instance_to_update = shipping_address.query.get(request.form["edit_shipping"])
    street = shipping_instance_to_update.street
    city = shipping_instance_to_update.city
    state = shipping_instance_to_update.state
    zipcode = shipping_instance_to_update.zipcode
    return render_template("address.html", street = street, city = city, state = state, zipcode = zipcode, address_id = address_id, cart = cart)

def editaddress():
    validation_check = shipping_address.validate_shipping(request.form)
    edited_shipping_address = request.form["address_id"]
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/editshippingaddress")
    else:
        edit_shipping = shipping_address.edit_shipping_address(request.form)
        return redirect("/accountinfo")

def deleteaddress():
    delete_address = shipping_address.delete_shipping_address(request.form)
    return redirect("/accountinfo")

def add_address():
    validation_check = shipping_address.validate_shipping(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/accountinfo")
    else:
        new_shipping = shipping_address.add_new_shipping(request.form)
        flash("You Added A New Address")
        return redirect("/accountinfo")

def add_address_from_checkout():
    validation_check = shipping_address.validate_shipping(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/proceedtocheckout")
    else:
        new_shipping = shipping_address.add_new_shipping(request.form)
        return redirect("/proceedtocheckout")


#BILLINGADDRESS
def add_billingid_from_checkout():
    login_id = session['user_id']
    validation_check = billing_address.validate_billing(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/proceedtocheckout")
    else:
        new_shipping = billing_address.add_billing_shipping(request.form)
        return redirect("/proceedtocheckout")

#WISHLIST
def wishlistpage():
    global listofviewed
    global cart
    global ordertotal
    updaterecently()
    try:
        if session['user_id']:
            login_id = session['user_id']
            user_wishlist = db.session.query(product, wishlist).filter(product.id == wishlist.product_id).filter(wishlist.customer_id == login_id).all()
            print(user_wishlist)
            return render_template("wishlist.html", user_wishlist = user_wishlist, cart = cart)
    except:
        flash("Please login or register to continue.")
        return render_template("loginreg.html")

def addtowishlist(routename):
    global listofviewed
    global cart
    
    updaterecently()
    try:
        if session['user_id']:
            login_id = session['user_id']
            product_id = request.form["product_id"]
            user_wishlist = wishlist.query.filter(wishlist.customer_id == login_id).filter(wishlist.product_id == product_id).count()
            print("Product Id",product_id)
            print("Login Id ", login_id)
            print("Wishlist count ", user_wishlist)

            if user_wishlist > 0:
                flash("Already added to wishlist")
                return redirect("/"+ str(routename) + "")
            else: #add to wishlist
                one_product = db.session.query(product).filter(product.id == product_id).all()
                add_a_wish = wishlist(
                    customer_id = login_id,
                    product_id = product_id
                )
                db.session.add(add_a_wish)
                db.session.commit()
                flash("Added to your wishlist")
                return redirect("/"+ str(routename) + "")
    except:
        flash("Please login or register to continue.")
        return render_template("loginreg.html")

def deletefromwishlist():
    delete_from_wishlist = wishlist.delete_wish(request.form)
    return redirect("/wishlist")

#CART 
def addtocart(routename):
    global cart
    global ordertotal
    
    product_id = request.form["product_id"]
    product_price = request.form["product_price"]
    for item in cart:
        if str(product_id) == str(item):
            flash("Sorry, due to high demand, only one unique item per order.")
            return redirect("/"+ str(routename) + "")
    if len(cart) < 5:
        cart += product_id
        ordertotal += int(product_price)
        flash("This item has been added to your cart.")
    else:
        flash("Due to high demand, limit is 5 items per order. Please view your cart to delete an item.")
    print(cart)
    print(ordertotal)
    return redirect("/"+ str(routename) + "")

def deletefromcart():
    global cart
    global ordertotal
    item_id = request.form["item_id"]
    product_id = request.form["product_id"]
    product_price = request.form["product_price"]
    cart.remove(product_id)
    ordertotal = ordertotal - int(product_price)
    return redirect("/viewcart")

def viewcart():
    global cart
    global listofviewed
    global ordertotal
    session['shipping_id'] = None
    session['billing_id'] = None
    print("Session shipping/billing: ", session['shipping_id'], session['billing_id'])
    
    updaterecently()
    allproducts = product.query.all()
    print(ordertotal)

    try:
        if session['user_id']:
            login_id = session['user_id']
            print(cart)
            return render_template("cart.html", cart = cart, listofviewed = listofviewed, allproducts = allproducts, login_id = login_id, ordertotal = ordertotal)
    except:
        flash("Please login or register to continue.")
        return render_template("loginreg.html", cart = cart)

def checkoutpage():
    login_id = session['user_id']
    print("Session shipping/billing: ", session['shipping_id'], session['billing_id'])
    global ordertotal
    global cart
    allproducts = product.query.all()
    if ordertotal == 0:
        flash("You have no items in your cart.")
        return redirect("/viewcart")
    else:
        shipping_addresses = db.session.query(shipping_address).filter(shipping_address.customer_id == login_id).all()
        billing_addresses = db.session.query(billing_address).filter(billing_address.customer_id == login_id).all()
        return render_template("checkout.html", shipping_addresses = shipping_addresses, billing_addresses = billing_addresses, ordertotal = ordertotal, cart = cart, allproducts = allproducts, login_id = login_id)


#ORDERPROCESSING
def verify_shipping_address():
    global cart
    global ordertotal
    session['shipping_id'] = request.form['verify_shipping_address_id']
    flash("Shipping Address #" + session['shipping_id'] + " Selected for Order")
    print("shipping id at checkout:", session['shipping_id'])
    return redirect("/proceedtocheckout")

def verify_billing_address():
    global cart
    global ordertotal
    session['billing_id'] = request.form['verify_billing_address_id']
    flash("Billing Address #" + session['billing_id'] + " Selected for Order")
    print("billing id at checkout:", session['shipping_id'])
    return redirect("/proceedtocheckout")

def submitordertodb():
    global cart
    global ordertotal
    login_id = session['user_id']
    shipping_id = session['shipping_id']
    billing_address_id = session['billing_id']
    order_total = ordertotal

    print("right above if statement ", shipping_id)
    if shipping_id == None:
        flash("Please choose a shipping address.")
        return redirect("/proceedtocheckout")
    if billing_address_id == None:
        flash("Please choose a billing address.")
        return redirect("/proceedtocheckout")
    else:
        add_order = order(
            customer_id = login_id,
            s_address_id = shipping_id,
            b_address_id = billing_address_id,
            order_total = order_total
        )
        db.session.add(add_order)
        db.session.commit()
        submitordertodb2()
        return redirect("/aftercheckout")

def submitordertodb2():
    global cart
    login_id = session['user_id']
    order_query = order.query.with_entities(order.id).all()
    print("Order Query: ", order_query)
    order_id = order_query[len(order_query)-1]
    real_order_id = order_id[0]
    session['order_id_created'] = real_order_id
    print(order_id[0])

    for i in range(len(cart)):
        add_order_item = order_item(
            order_id = real_order_id,
            product_id = cart[i]
        )
        db.session.add(add_order_item)
        db.session.commit()
    return 

def aftercheckout():
    global cart
    first_name = session['first_name']
    order_query = order.query.with_entities(order.id).all()
    order_id = order_query[len(order_query)-1]
    real_order_id = order_id[0]
    cart = []
    return render_template("aftercheckout.html", first_name = first_name, order_id = real_order_id)

#BOTTOMNAVIGATION
def sitemap():
    global listofviewed
    global cart
    updaterecently()
    allproducts = product.query.all()
    return render_template("sitemap.html", listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def momomust():
    global listofviewed
    global cart
    updaterecently()
    allproducts = product.query.all()
    return render_template("momomust.html", listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def privacy():
    global listofviewed
    global cart
    updaterecently()
    show = "show"
    allproducts = product.query.all()
    return render_template("customercare.html", showprivacy = show, allproducts = allproducts, cart = cart)

def shippinginformation():
    global listofviewed
    global cart
    updaterecently()
    show = "show"
    allproducts = product.query.all()
    return render_template("customercare.html", showshipping = show, allproducts = allproducts, cart = cart)

def returnsandexchanges():
    global listofviewed
    global cart
    updaterecently()
    show = "show"
    allproducts = product.query.all()
    return render_template("customercare.html", showreturn = show, allproducts = allproducts, cart = cart)

def productcare():
    global listofviewed
    global cart
    updaterecently()
    show = "show"
    allproducts = product.query.all()
    return render_template("customercare.html", showrepairs = show, allproducts = allproducts, cart = cart)

def contactus():
    global listofviewed
    global cart
    updaterecently()
    show = "show"
    allproducts = product.query.all()
    return render_template("customercare.html", showcontact = show, allproducts = allproducts, cart = cart)

def about():
    global listofviewed
    global cart
    updaterecently()
    allproducts = product.query.all()
    return render_template("about.html", listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def searchpage():
    global listofviewed
    global cart
    updaterecently()
    allproducts = product.query.all()
    return render_template("search.html", allproducts = allproducts, cart = cart)

def productsearch():
    global cart
    # res = db.session.query(product, category).filter(product.id == product_category.product_id).filter(product_category.category_id == category.id).all()
    # list_products = json.dumps(dict(res))
    res = product.query.all()
    list_products = [r.as_dict() for r in res]
    return jsonify(list_products)
    # return redirect("/searchpage")

#VIEWALL
def viewallproducts():
    global cart
    global listofviewed
    updaterecently()
    allproducts = product.query.all()
    return render_template("view.html", view = allproducts, listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def viewallhandbags():
    global cart
    global listofviewed
    updaterecently()
    allhandbags = db.session.query(product).join(product_category).filter(product_category.category_id == 3)
    allproducts = product.query.all()
    return render_template("view.html", view = allhandbags, listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def viewallbagcharms():
    global listofviewed
    global cart
    updaterecently()
    allbagcharms = db.session.query(product).join(product_category).filter(product_category.category_id == 5)
    allproducts = product.query.all()
    return render_template("view.html", view = allbagcharms, listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def viewallwallets():
    global listofviewed
    global cart
    updaterecently()
    allwallets = db.session.query(product).join(product_category).filter(product_category.category_id == 4)
    allproducts = product.query.all()
    return render_template("view.html", view = allwallets, listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def viewallblackcollection():
    global listofviewed
    global cart
    updaterecently()
    allblack = db.session.query(product).join(product_category).filter(product_category.category_id == 1)
    allproducts = product.query.all()
    return render_template("view.html", view = allblack, listofviewed = listofviewed, allproducts = allproducts, cart = cart)

def viewallrexy():
    global listofviewed
    global cart
    updaterecently()
    allrexy = db.session.query(product).join(product_category).filter(product_category.category_id == 2)
    allproducts = product.query.all()
    return render_template("view.html", view = allrexy, listofviewed = listofviewed, allproducts = allproducts, cart = cart)

#VIEWONE
def rogue():
    global listofviewed
    global cart
    rogue = db.session.query(product).filter(product.id == 1).all()
    x = rogue[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = rogue, allproducts = allproducts, cart = cart)

def highline():
    global listofviewed
    global cart
    highline = db.session.query(product).filter(product.id == 2).all()
    x = highline[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = highline, allproducts = allproducts, cart = cart)

def harmony():
    global listofviewed
    global cart
    harmony = db.session.query(product).filter(product.id == 3).all()
    x = harmony[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = harmony, allproducts = allproducts, cart = cart)

def rexyskeleton():
    global listofviewed
    global cart
    rexyskeleton = db.session.query(product).filter(product.id == 4).all()
    x = rexyskeleton[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = rexyskeleton, allproducts = allproducts, cart = cart)

def rexyoilslick():
    global listofviewed
    global cart
    rexyoilslick = db.session.query(product).filter(product.id == 5).all()
    x = rexyoilslick[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = rexyoilslick, allproducts = allproducts, cart = cart)

def rexygold():
    global listofviewed
    global cart
    rexygold = db.session.query(product).filter(product.id == 6).all()
    x = rexygold[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = rexygold, allproducts = allproducts, cart = cart)

def foldovercardcase():
    global listofviewed
    global cart
    foldovercardcase = db.session.query(product).filter(product.id == 7).all()
    x = foldovercardcase[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = foldovercardcase, allproducts = allproducts, cart = cart)

def rexycardholder():
    global listofviewed
    global cart
    rexycardholder = db.session.query(product).filter(product.id == 8).all()
    x = rexycardholder[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = rexycardholder, allproducts = allproducts, cart = cart)

def rexyzippywallet():
    global listofviewed
    global cart
    rexyzippywallet = db.session.query(product).filter(product.id == 9).all()
    x = rexyzippywallet[0].id
    session["viewed"] = x
    onLoad(x)
    allproducts = product.query.all()
    return render_template("viewone.html", x = x, listofviewed = listofviewed, productview = rexyzippywallet, allproducts = allproducts, cart = cart)