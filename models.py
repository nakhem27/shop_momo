from config import db, re, func, flash, bcrypt, jsonify

class customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_customer(cls, new_customer_data):
        is_valid = True
        if len(new_customer_data["first_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_customer_data["first_name"]):
            is_valid = False
            flash("Please enter a valid first name.")
        if len(new_customer_data["last_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_customer_data["last_name"]):
            is_valid = False
            flash("Please enter a valid last name. Must be between 3-20 characters in length and contain no numbers or special characters.")
        if len(new_customer_data["email"]) < 1 or not re.search("[^@]+@[^@]+\.[^@]+", new_customer_data["email"]):
            is_valid = False
            flash("Please enter a valid email address.")
        if len(new_customer_data["phone_number"]) < 1 or not re.search("^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$", new_customer_data["phone_number"]):
            is_valid = False
            flash("Please enter a valid phone number.")
        if len(new_customer_data["password"]) < 8:
            is_valid = False
            flash("Password should be at least 8 characters and contain one number and uppercase letter")
        if new_customer_data["confirm_password"] != new_customer_data["password"]:
            is_valid = False
            flash("Passwords do not match!")
        return is_valid
    
    @classmethod
    def add_new_customer(cls, new_customer_data):
        add_customer = cls(
            first_name = new_customer_data["first_name"],
            last_name = new_customer_data["last_name"],
            email = new_customer_data["email"],
            phone_number = new_customer_data["phone_number"],
            password = bcrypt.generate_password_hash(new_customer_data["password"])
        )
        db.session.add(add_customer)
        db.session.commit()
        flash("Registration successful! Log in to continue.")
        return add_customer
    
    @classmethod
    def validate_edit_customer(cls, new_customer_data):
        is_valid = True
        if len(new_customer_data["first_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_customer_data["first_name"]):
            is_valid = False
            flash("Please enter a valid first name.")
        if len(new_customer_data["last_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_customer_data["last_name"]):
            is_valid = False
            flash("Please enter a valid last name. Must be between 3-20 characters in length and contain no numbers or special characters.")
        if len(new_customer_data["phone_number"]) < 1 or not re.search("^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$", new_customer_data["phone_number"]):
            is_valid = False
            flash("Please enter a valid phone number.")
        return is_valid
    
    @classmethod
    def edit_customer(cls, edit_customer_data):
        edit_customer = customer.query.get(edit_customer_data["login_id"])
        edit_customer.first_name = edit_customer_data["first_name"]
        edit_customer.last_name = edit_customer_data["last_name"]
        edit_customer.phone_number = edit_customer_data["phone_number"]
        db.session.commit()
        flash("Customer Information Updated")
        return edit_customer

class shipping_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    customer_shipping_address = db.relationship('customer', backref='shipping_address', cascade='all')

    @classmethod
    def validate_shipping(cls, new_shipping_data):
        is_valid = True
        if len(new_shipping_data["street"]) < 1 or not re.search("^[#.0-9a-zA-Z\s,-]+$", new_shipping_data["street"]):
            is_valid = False
            flash("Please enter a valid street address.")
        if len(new_shipping_data["city"]) < 1 or not re.search("^[a-zA-Z',.\s-]{1,25}$", new_shipping_data["city"]):
            is_valid = False
            flash("Please enter a valid city.")
        if len(new_shipping_data["state"]) < 1 or not re.search("^[a-zA-Z',.\s-]{1,25}$", new_shipping_data["state"]):
            is_valid = False
            flash("Please enter a state.")
        if len(new_shipping_data["zipcode"]) < 1 or not re.search("^\d{5}(?:[-\s]\d{4})?$", new_shipping_data["zipcode"]):
            is_valid = False
            flash("Please enter a valid zipcode.")
        return is_valid

    @classmethod
    def add_new_shipping(cls, new_shipping_data):
        add_shipping = cls(
            customer_id = new_shipping_data['customer_id'],
            street = new_shipping_data['street'],
            city = new_shipping_data['city'],
            state = new_shipping_data['state'],
            zipcode = new_shipping_data['zipcode']
        )
        db.session.add(add_shipping)
        db.session.commit()
        flash("New Shipping Address Added")
        return add_shipping

    @classmethod
    def delete_shipping_address(cls, delete_shipping_data):
        delete_shipping_address = shipping_address.query.filter(shipping_address.id == delete_shipping_data["delete_shipping"]).delete()
        db.session.commit()
        flash("You Deleted This Shipping Address.")
        return delete_shipping_address
    
    @classmethod
    def edit_shipping_address(cls, edit_shipping_data):
        edit_shipping = shipping_address.query.get(edit_shipping_data['address_id'])
        edit_shipping.street = edit_shipping_data["street"]
        edit_shipping.city = edit_shipping_data["city"]
        edit_shipping.state = edit_shipping_data['state']
        edit_shipping.zipcode = edit_shipping_data['zipcode']
        db.session.commit()
        flash("Shipping Address Edited")
        return edit_shipping

class billing_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    customer_billing_address = db.relationship('customer', backref='billing_address', cascade='all')

    @classmethod
    def validate_billing(cls, new_billing_data):
        is_valid = True
        if len(new_billing_data["street"]) < 1 or not re.search("^[#.0-9a-zA-Z\s,-]+$", new_billing_data["street"]):
            is_valid = False
            flash("Please enter a valid street address.")
        if len(new_billing_data["city"]) < 1 or not re.search("^[a-zA-Z',.\s-]{1,25}$", new_billing_data["city"]):
            is_valid = False
            flash("Please enter a valid city.")
        if len(new_billing_data["state"]) < 1 or not re.search("^[a-zA-Z',.\s-]{1,25}$", new_billing_data["state"]):
            is_valid = False
            flash("Please enter a state.")
        if len(new_billing_data["zipcode"]) < 1 or not re.search("^\d{5}(?:[-\s]\d{4})?$", new_billing_data["zipcode"]):
            is_valid = False
            flash("Please enter a valid zipcode.")
        return is_valid

    @classmethod
    def add_billing_shipping(cls, new_billing_data):
        add_billing = cls(
            customer_id = new_billing_data['customer_id'],
            street = new_billing_data['street'],
            city = new_billing_data['city'],
            state = new_billing_data['state'],
            zipcode = new_billing_data['zipcode']
        )
        db.session.add(add_billing)
        db.session.commit()
        flash("New Billing Address Added")
        return add_billing
    
    @classmethod
    def delete_billing_address(cls, delete_billing_data):
        delete_billing_address = billing_address.query.filter(billing_address.customer_id == delete_billing_data["delete_billing"]).delete()
        db.session.commit()
        flash("You Deleted This Billing Address.")
        return delete_billing_address

# Many to Many table
class order(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    s_address_id = db.Column(db.Integer, db.ForeignKey('shipping_address.id'))
    b_address_id = db.Column(db.Integer, db.ForeignKey('billing_address.id'))
    order_total = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    customer = db.relationship('customer', backref='orders', cascade='all')
    shipping_address = db.relationship('shipping_address', backref= 'orders', cascade='all')
    billing_address = db.relationship('billing_address', backref= 'orders', cascade='all')

class order_item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    order = db.relationship('order', backref= 'ordered_items', cascade='all')

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.String(255))
    imgname = db.Column(db.String(255))
    imgname2 = db.Column(db.String(255))
    routename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# Many to Many table
class product_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    product = db.relationship('product', backref='products', cascade='all')
    category = db.relationship('category', backref='product_category', cascade='all')

class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '{}'.format(self.category)

    def as_dict(self):
        return {'name': self.category}

class wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    customer_who_wished = db.relationship('customer', backref='customer_made_wish', cascade='all')
    product_they_wished_for = db.relationship('product', backref='customer_loves_product', cascade='all')

    @classmethod
    def delete_wish(cls, delete_wish_data):
        wish_instance_to_delete = wishlist.query.filter(wishlist.product_id == delete_wish_data['product_id']).delete()
        db.session.commit()
        flash("You deleted this from your wishlist!")
        return wish_instance_to_delete