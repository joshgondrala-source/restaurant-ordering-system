from flask import Flask, render_template, request
from flask import redirect
from datetime import datetime

app = Flask(__name__)
cart=[]
current_table=None
orders = []
order_counter = 100
bill_requests = []
paid_tables = []

# MENU DATA
restaurant_menu = {
   "veg_soups": [
{"name": "Sweet Corn Soup Veg", "price": 99},
{"name": "Hot N Sour Veg", "price": 99},
{"name": "Lemon Coriander Soup", "price": 99},
{"name": "Noodles Soup Veg", "price": 99},
{"name": "Veg Manchow Soup", "price": 99}
],

"veg_starters": [
{"name": "Aloo 65", "price": 169},
{"name": "Honey Chilli Potato", "price": 199},
{"name": "Gobi Manchurian", "price": 189},
{"name": "Chilli Babycorn", "price": 229},
{"name": "Babycorn 65", "price": 229},
{"name": "Paneer 65", "price": 249},
{"name": "Chilli Paneer", "price": 249},
{"name": "Veg Manchurian", "price": 189},
{"name": "Chilli Gobi", "price": 179},
{"name": "Golden Crispy Corn", "price": 249},
{"name": "Paneer Majestic", "price": 259},
{"name": "Chilli Mushroom", "price": 239},
{"name": "Onion Rings", "price": 179},
{"name": "Creamy Paneer", "price": 169}
],

"veg_tikka": [
{"name": "Paneer Tikka", "price": 299}
],

"veg_curries": [
{"name": "Mix Veg Curry", "price": 189},
{"name": "Jeera Wale Aloo", "price": 189},
{"name": "Aloo Gobi", "price": 189},
{"name": "Gobi Mutter", "price": 189},
{"name": "Shahi Paneer", "price": 329},
{"name": "Paneer Butter Masala", "price": 249},
{"name": "Paneer Lababdar", "price": 249},
{"name": "Malai Kofta", "price": 229},
{"name": "Dum Aloo", "price": 299},
{"name": "Paneer Tikka Masala", "price": 329},
{"name": "Paneer Bhurji", "price": 329},
{"name": "Kaju Paneer", "price": 329},
{"name": "Mutter Paneer", "price": 249},
{"name": "Kadhai Paneer", "price": 249},
{"name": "Kaju Tomato", "price": 289}
],

"dal": [
{"name": "Tomato Dal", "price": 149},
{"name": "Dal Fry", "price": 149},
{"name": "Tadka Wali Dal", "price": 179}
],

"veg_biryani": [
{"name": "Veg Biryani", "price": 229},
{"name": "Paneer Biryani", "price": 249},
{"name": "Mushroom Biryani", "price": 249},
{"name": "Kaju Biryani", "price": 259}
],

"veg_chinese": [
{"name": "Veg Noodles", "price": 159},
{"name": "Veg Fried Rice", "price": 169},
{"name": "Veg Schezwan Noodles", "price": 169},
{"name": "Veg Schezwan Rice", "price": 179},
{"name": "Veg Chilli Garlic Rice", "price": 179},
{"name": "Paneer Fried Rice", "price": 199},
{"name": "Kaju Rice", "price": 199},
{"name": "Kaju Paneer Fried Rice", "price": 249}
],

"veg_combos": [
{"name": "Veg Fried Rice + Veg Manchurian Gravy", "price": 269},
{"name": "Veg Noodles + Veg Manchurian Gravy", "price": 269}
],

"veg_rice": [
{"name": "Plain Rice", "price": 99},
{"name": "Jeera Rice", "price": 159},
{"name": "Green Peas Pulao", "price": 179},
{"name": "Curd Rice", "price": 179}
],

"veg_parathas": [
{"name": "Aloo Paratha", "price": 119},
{"name": "Onion Paratha", "price": 119},
{"name": "Paneer Paratha", "price": 179},
{"name": "Gobi Paratha", "price": 119},
{"name": "Lachha Paratha", "price": 119}
],
"nonveg_soups": [
{"name": "Chicken Sweet Corn Soup", "price": 139},
{"name": "Chicken Noodles Soup", "price": 139},
{"name": "Chicken Hot N Sour Soup", "price": 139},
{"name": "Chicken Manchow Soup", "price": 139},
{"name": "Chicken Corn Soup", "price": 139}
],

"chicken_starters": [

{"name": "Chicken 65", "price":289},
{"name": "Chicken Lollipop", "price": 289},
{"name": "Drums of Heaven", "price": 289},
{"name": "Chicken Manchurian", "price": 289},
{"name": "Chicken Majestic", "price": 299},
{"name": "Pepper Chicken", "price": 299},
{"name": "Chicken 555", "price": 299},
{"name": "Spicy Fried Chicken", "price": 299},
{"name": "Chilli Chicken", "price": 269},
{"name": "Dragon Chicken", "price": 299},
{"name": "Hakka Chilli Chicken", "price": 299}


],

"egg_starters": [

{"name": "Chilli Egg", "price": 179},
{"name": "Egg 65", "price": 179},
{"name": "Egg Manchurian", "price": 189}


],

"nonveg_tikka": [

{"name": "Tandoori Chicken Half", "price": 319},
{"name": "Tandoori Chicken Full", "price": 579},
{"name": "Chicken Tikka", "price": 389}


],

"sea_food": [


{"name": "Chilli Fish", "price": 329},
{"name": "Apollo Fish", "price": 329},
{"name": "Fish Finger", "price": 329},
{"name": "Butter Garlic Prawns", "price": 349},
{"name": "Fried Prawns", "price": 349},
{"name": "Chilli Prawns", "price": 349},
{"name": "Golden Fried Prawns", "price": 349},
{"name": "Salt & Pepper Prawns", "price": 349}


],

"chicken_curries": [


{"name": "Chicken Tari Wala", "price": 299},
{"name": "Rara Chicken", "price": 299},
{"name": "Kadai Chicken", "price": 329},
{"name": "Punjabi Butter Chicken", "price": 329},
{"name": "Chicken Masala", "price": 299},
{"name": "Chicken Tikka Masala", "price": 329},
{"name": "Chicken Patyala", "price": 329},
{"name": "Chicken Roganjosh", "price": 299},
{"name": "Chicken Curry", "price": 299},
{"name": "Butter Chicken", "price": 329}


],

"egg_curries": [


{"name": "Egg Curry", "price": 159},
{"name": "Egg Bhurji", "price": 169}


],

"biryani": [


{"name": "Egg Biryani", "price": 219},
{"name": "Chicken Dum Biryani", "price": 289},
{"name": "Chicken Tikka Biryani", "price": 289},
{"name": "Chicken 65 Biryani", "price": 289},
{"name": "Chicken Fry Piece Biryani", "price": 289},
{"name": "Lollipop Biryani", "price": 299},
{"name": "Tandoori Biryani", "price": 299},
{"name": "Fish Biryani", "price": 299},
{"name": "Prawn Biryani", "price": 329},
{"name": "Special Chicken Biryani", "price": 369}


],

"nonveg_chinese": [


{"name": "Egg Noodles", "price": 179},
{"name": "Egg Schezwan Noodles", "price": 189},
{"name": "Chicken Noodles", "price": 189},
{"name": "Chicken Schezwan Noodles", "price": 209},
{"name": "Prawn Noodles", "price": 249},
{"name": "Mix Non Veg Noodles", "price": 299},
{"name": "Egg Fried Rice", "price": 179},
{"name": "Chicken Fried Rice", "price": 199},
{"name": "Chicken Schezwan Rice", "price": 209},
{"name": "Chicken Chilli Garlic Rice", "price": 199},
{"name": "Mixed Non Veg Fried Rice", "price": 299}


],

"nonveg_combos": [


{"name": "Chicken Fried Rice + Chicken Manchurian", "price": 329},
{"name": "Chicken Noodles + Chicken Manchurian", "price": 329}


],

"nonveg_rice": [


{"name": "Plain Rice", "price": 99},
{"name": "Jeera Rice", "price": 159},
{"name": "Green Peas Pulao", "price": 179},
{"name": "Curd Rice", "price": 179}


],

"nonveg_parathas": [

{"name": "Chicken Keema Paratha", "price": 179}

],
"rotis": [

{"name": "Plain Pulka", "price": 25},
{"name": "Butter Pulka", "price": 30},
{"name": "Plain Tandoori Roti", "price": 35},
{"name": "Butter Tandoori Roti", "price": 40},
{"name": "Plain Naan", "price": 45},
{"name": "Butter Naan", "price": 50},
{"name": "Plain Garlic Naan", "price": 55},
{"name": "Butter Garlic Naan", "price": 60}


],

"chopsuey": [


{"name": "Veg Chinese Chopsuey", "price": 259},
{"name": "Veg American Chopsuey", "price": 259},
{"name": "Veg Dragon Chopsuey", "price": 259},
{"name": "Chicken Chinese Chopsuey", "price": 299},
{"name": "Chicken American Chopsuey", "price": 299},
{"name": "Chicken Dragon Chopsuey", "price": 299}


],

"jumbo": [


{"name": "Chicken Family Pack", "price": 579},
{"name": "Chicken Biryani Jumbo Pack", "price": 1099},
{"name": "Veg Biryani Jumbo Pack", "price": 899}


],

"beverages": [

{"name": "Cool Drink 250ml", "price": 20},
{"name": "Sweet Lassi", "price": 69},
{"name": "Butter Milk", "price": 49},
{"name": "Water Bottle", "price": 20},
{"name": "Lemonade", "price": 59}


],

"papad": [

{"name": "Roasted Amritsari Papad", "price": 39},
{"name": "Masala Roasted Amritsari Papad", "price": 59}


]


}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dinein")
def dinein():
    return render_template("dinein.html")


@app.route("/menu")
def menu():

    global current_table

    table = request.args.get("table")

    if table:
        current_table = table

    return render_template(
        "menu.html",
        table=current_table
    )

@app.route("/items")
def items():

    table = request.args.get("table")
    category = request.args.get("category")

    return render_template(
        "items.html",
        table=table,
        category=category,
        items=restaurant_menu[category]
    )


@app.route("/itemdetails")
def itemdetails():

    name = request.args.get("name")

    item_data = None

    for category in restaurant_menu.values():

        for item in category:

            if item["name"] == name:
                item_data = item
                break

    return render_template(
        "item_details.html",
        item=item_data
    )
@app.route("/addtocart", methods=["POST"])
def addtocart():

    item_name = request.form.get("item_name")
    price = int(request.form.get("price"))
    quantity = int(request.form.get("quantity"))
    instructions = request.form.get("instructions")

    cart.append({
        "name": item_name,
        "price": price,
        "quantity": quantity,
        "instructions": instructions
    })
    grand_total = 0

    for item in cart:
      grand_total += item["price"] * item["quantity"]

    return render_template(
        "cart.html",
        cart=cart,
        grand_total=grand_total
    )
@app.route("/deleteitem", methods=["POST"])
def deleteitem():

    item_name = request.form.get("item_name")

    for item in cart:

        if item["name"] == item_name:
            cart.remove(item)
            break
    grand_total = 0

    for item in cart:
      grand_total += item["price"] * item["quantity"]
    return render_template(
        "cart.html",
        cart=cart,
        grand_total=grand_total
    )
@app.route("/placeorder", methods=["POST"])
def placeorder():

    global order_counter
    global cart

    order_counter += 1

    total = 0

    for item in cart:
        total += item["price"] * item["quantity"]
    table_order_count = 0

    for order in orders:

      if order["table"] == current_table:
          table_order_count += 1
    orders.append({
        "order_id": order_counter,
        "table": current_table,
        "items": cart.copy(),
        "total": total,
        "time": datetime.now().strftime("%I:%M %p"),
        "status": "NEW TABLE" if table_order_count == 0 else "RUNNING TABLE"
    })

    cart.clear()

    table_orders = []

    table_total = 0

    for order in orders:

        if order["table"] == current_table:

            table_orders.append(order)

            table_total += order["total"]

    return render_template(
        "order_success.html",
        order_id=order_counter,
        table=current_table,
        total=total,
        table_orders=table_orders,
        table_total=table_total
    )
@app.route("/kitchen")
def kitchen():

    return render_template(
        "kitchen.html",
        orders=orders
    )
@app.route("/requestbill", methods=["POST"])
def requestbill():

    bill_requests.append({
        "table": current_table
    })

    return render_template(
        "bill_requested.html",
        table=current_table
    )
@app.route("/manager")
def manager():

    return render_template(
        "manager.html",
        bill_requests=bill_requests,
        orders=orders
    )
@app.route("/generatebill", methods=["POST"])
def generatebill():

    table = request.form.get("table")

    food_total = float(
        request.form.get("food_total")
    )

    discount = float(
        request.form.get("discount")
    )

    gst = food_total * 0.05

    subtotal = food_total + gst

    discount_amount = (
        subtotal * discount / 100
    )

    final_total = (
        subtotal - discount_amount
    )

    rounded_total = round(final_total)

    return render_template(
        "final_bill.html",
        table=table,
        food_total=food_total,
        gst=gst,
        discount=discount,
        discount_amount=discount_amount,
        final_total=final_total,
        rounded_total=rounded_total
    )
@app.route("/markpaid", methods=["POST"])
def markpaid():

    table = request.form.get("table")

    global orders
    global bill_requests

    orders = [
        order
        for order in orders
        if order["table"] != table
    ]

    bill_requests = [
        request
        for request in bill_requests
        if request["table"] != table
    ]

    return redirect("/manager")
@app.route("/veg")
def veg():

    table = request.args.get("table")

    return render_template(
        "veg.html",
        table=table
    )


@app.route("/nonveg")
def nonveg():

    table = request.args.get("table")

    return render_template(
        "nonveg.html",
        table=table
    )

takeaway_token = 1

@app.route("/takeaway")
def takeaway():

    global takeaway_token

    token = f"TK{takeaway_token:03d}"

    takeaway_token += 1

    return redirect(f"/menu?table={token}")
if __name__ == "__main__":
    app.run(debug=True) 