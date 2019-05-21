from config import app
from controller_functions import homepage, register, login, logout, myaccount, accountinfo, editaddresspage, editaddress, deleteaddress, add_address, add_billingid_from_checkout, wishlistpage, addtowishlist, deletefromwishlist, addtocart, deletefromcart, viewcart, checkoutpage, verify_shipping_address, verify_billing_address, submitordertodb, aftercheckout, sitemap, momomust, privacy, shippinginformation, returnsandexchanges, productcare, contactus, about, viewallproducts, viewallhandbags, viewallbagcharms, viewallwallets, viewallblackcollection, viewallrexy, rogue, highline, harmony, rexyskeleton, rexyoilslick, rexygold, foldovercardcase, rexycardholder, rexyzippywallet, editaccountinfopage, editaccount, email, searchpage, productsearch, add_address_from_checkout

#HOMEPAGE
app.add_url_rule("/", view_func=homepage)

#LOGIN/REG
app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/logout", view_func=logout, methods=["POST"])
app.add_url_rule("/myaccount", view_func=myaccount, methods=["GET", "POST"])
app.add_url_rule("/accountinfo", view_func=accountinfo)
app.add_url_rule("/editcustomerinformation/<login_id>", view_func=editaccountinfopage, methods=["GET","POST"])
app.add_url_rule("/editaccount/<login_id>", view_func=editaccount, methods=["POST"])
app.add_url_rule("/", view_func=email, methods=["GET"])

#SHIPPING/BILLINGADDRESS
app.add_url_rule("/editshippingaddress/<address_id>", view_func=editaddresspage, methods=["POST"])
app.add_url_rule("/editshippingfinal", view_func=editaddress, methods=["POST"])
app.add_url_rule("/deleteshippingaddress", view_func=deleteaddress, methods=["POST"])
app.add_url_rule("/addshippingaddress", view_func=add_address, methods=["POST"])
app.add_url_rule("/add_address_from_checkout", view_func=add_address_from_checkout, methods=["POST"])
app.add_url_rule("/add_billingid_from_checkout", view_func=add_billingid_from_checkout, methods=["POST"])

#WISHLIST
app.add_url_rule("/wishlist", view_func=wishlistpage, methods=["GET","POST"])
app.add_url_rule("/addtowishlist/<routename>", view_func=addtowishlist, methods=["GET", "POST"])
app.add_url_rule("/deletefromwishlist", view_func = deletefromwishlist, methods=["POST"])

#CART
app.add_url_rule("/addtocart/<routename>", view_func=addtocart, methods=["POST"])
app.add_url_rule("/deletefromcart", view_func=deletefromcart, methods=["POST"])
app.add_url_rule("/viewcart", view_func=viewcart, methods=["GET","POST"])
app.add_url_rule("/proceedtocheckout", view_func=checkoutpage, methods=["GET","POST"])

#ORDERPROCESSING 
app.add_url_rule("/verifyshippingaddress", view_func=verify_shipping_address, methods=["POST"])
app.add_url_rule("/verifybillingaddress", view_func=verify_billing_address, methods=["POST"])
app.add_url_rule("/submitorder", view_func=submitordertodb, methods=["POST"])
app.add_url_rule("/aftercheckout", view_func=aftercheckout, methods=["GET","POST"])

#BOTTOMNAVIGATION
app.add_url_rule("/about", view_func=about)
app.add_url_rule("/sitemap", view_func=sitemap)
app.add_url_rule("/momomust", view_func=momomust)
app.add_url_rule("/privacy", view_func=privacy)
app.add_url_rule("/shippinginformation", view_func=shippinginformation)
app.add_url_rule("/returnsandexchanges", view_func=returnsandexchanges)
app.add_url_rule("/productcare", view_func=productcare)
app.add_url_rule("/contactus", view_func=contactus)
app.add_url_rule("/searchpage", view_func=searchpage)
app.add_url_rule("/productsearch", view_func=productsearch, methods=["GET","POST"])

#VIEWALL
app.add_url_rule("/viewallproducts", view_func=viewallproducts)
app.add_url_rule("/viewallhandbags", view_func=viewallhandbags)
app.add_url_rule("/viewallbagcharms", view_func=viewallbagcharms)
app.add_url_rule("/viewallwallets", view_func=viewallwallets)
app.add_url_rule("/viewallblackcollection", view_func=viewallblackcollection)
app.add_url_rule("/viewallrexy", view_func=viewallrexy)

#VIEWONE
app.add_url_rule("/rogue", view_func=rogue)
app.add_url_rule("/highline", view_func=highline)
app.add_url_rule("/harmony", view_func=harmony)
app.add_url_rule("/rexyskeleton", view_func=rexyskeleton)
app.add_url_rule("/rexyoilslick", view_func=rexyoilslick)
app.add_url_rule("/rexygold", view_func=rexygold)
app.add_url_rule("/foldovercardcase", view_func=foldovercardcase)
app.add_url_rule("/rexycardholder", view_func=rexycardholder)
app.add_url_rule("/rexyzippywallet", view_func=rexyzippywallet)

