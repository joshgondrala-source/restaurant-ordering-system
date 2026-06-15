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
{"name": "Sweet Corn Soup Veg", "price": 0},
{"name": "Hot N Sour Veg", "price": 0},
{"name": "Lemon Coriander Soup", "price": 0},
{"name": "Noodles Soup Veg", "price": 0},
{"name": "Veg Manchow Soup", "price": 0}
],

"veg_starters": [
{"name": "Aloo 65", "price": 0},
{"name": "Honey Chilli Potato", "price": 0},
{"name": "Gobi Manchurian", "price": 0},
{"name": "Chilli Babycorn", "price": 0},
{"name": "Babycorn 65", "price": 0},
{"name": "Paneer 65", "price": 0},
{"name": "Chilli Paneer", "price": 0},
{"name": "Veg Manchurian", "price": 0},
{"name": "Chilli Gobi", "price": 0},
{"name": "Golden Crispy Corn", "price": 0},
{"name": "Paneer Majestic", "price": 0},
{"name": "Chilli Mushroom", "price": 0},
{"name": "Onion Rings", "price": 0},
{"name": "Creamy Paneer", "price": 0}
],

"veg_tikka": [
{"name": "Paneer Tikka", "price": 0}
],

"veg_curries": [
{"name": "Mix Veg Curry", "price": 0},
{"name": "Jeera Wale Aloo", "price": 0},
{"name": "Aloo Gobi", "price": 0},
{"name": "Gobi Mutter", "price": 0},
{"name": "Shahi Paneer", "price": 0},
{"name": "Paneer Butter Masala", "price": 0},
{"name": "Paneer Lababdar", "price": 0},
{"name": "Malai Kofta", "price": 0},
{"name": "Dum Aloo", "price": 0},
{"name": "Paneer Tikka Masala", "price": 0},
{"name": "Paneer Bhurji", "price": 0},
{"name": "Kaju Paneer", "price": 0},
{"name": "Mutter Paneer", "price": 0},
{"name": "Kadhai Paneer", "price": 0},
{"name": "Kaju Tomato", "price": 0}
],

"dal": [
{"name": "Tomato Dal", "price": 0},
{"name": "Dal Fry", "price": 0},
{"name": "Tadka Wali Dal", "price": 0}
],

"veg_biryani": [
{"name": "Veg Biryani", "price": 0},
{"name": "Paneer Biryani", "price": 0},
{"name": "Mushroom Biryani", "price": 0},
{"name": "Kaju Biryani", "price": 0}
],

"veg_chinese": [
{"name": "Veg Noodles", "price": 0},
{"name": "Veg Fried Rice", "price": 0},
{"name": "Veg Schezwan Noodles", "price": 0},
{"name": "Veg Schezwan Rice", "price": 0},
{"name": "Veg Chilli Garlic Rice", "price": 0},
{"name": "Paneer Fried Rice", "price": 0},
{"name": "Kaju Rice", "price": 0},
{"name": "Kaju Paneer Fried Rice", "price": 0}
],

"veg_combos": [
{"name": "Veg Fried Rice + Veg Manchurian Gravy", "price": 0},
{"name": "Veg Noodles + Veg Manchurian Gravy", "price": 0}
],

"veg_rice": [
{"name": "Plain Rice", "price": 0},
{"name": "Jeera Rice", "price": 0},
{"name": "Green Peas Pulao", "price": 0},
{"name": "Curd Rice", "price": 0}
],

"veg_parathas": [
{"name": "Aloo Paratha", "price": 0},
{"name": "Onion Paratha", "price": 0},
{"name": "Paneer Paratha", "price": 0},
{"name": "Gobi Paratha", "price": 0},
{"name": "Lachha Paratha", "price": 0}
],
"nonveg_soups": [
{"name": "Chicken Sweet Corn Soup", "price": 0},
{"name": "Chicken Noodles Soup", "price": 0},
{"name": "Chicken Hot N Sour Soup", "price": 0},
{"name": "Chicken Manchow Soup", "price": 0},
{"name": "Chicken Corn Soup", "price": 0}
],

"chicken_starters": [

{"name": "Chicken 65", "price": 0},
{"name": "Chicken Lollipop", "price": 0},
{"name": "Drums of Heaven", "price": 0},
{"name": "Chicken Manchurian", "price": 0},
{"name": "Chicken Majestic", "price": 0},
{"name": "Pepper Chicken", "price": 0},
{"name": "Chicken 555", "price": 0},
{"name": "Spicy Fried Chicken", "price": 0},
{"name": "Chilli Chicken", "price": 0},
{"name": "Dragon Chicken", "price": 0},
{"name": "Hakka Chilli Chicken", "price": 0}


],

"egg_starters": [

{"name": "Chilli Egg", "price": 0},
{"name": "Egg 65", "price": 0},
{"name": "Egg Manchurian", "price": 0}


],

"nonveg_tikka": [

{"name": "Tandoori Chicken Half", "price": 0},
{"name": "Tandoori Chicken Full", "price": 0},
{"name": "Chicken Tikka", "price": 0}


],

"sea_food": [


{"name": "Chilli Fish", "price": 0},
{"name": "Apollo Fish", "price": 0},
{"name": "Fish Finger", "price": 0},
{"name": "Butter Garlic Prawns", "price": 0},
{"name": "Fried Prawns", "price": 0},
{"name": "Chilli Prawns", "price": 0},
{"name": "Golden Fried Prawns", "price": 0},
{"name": "Salt & Pepper Prawns", "price": 0}


],

"chicken_curries": [


{"name": "Chicken Tari Wala", "price": 0},
{"name": "Rara Chicken", "price": 0},
{"name": "Kadai Chicken", "price": 0},
{"name": "Punjabi Butter Chicken", "price": 0},
{"name": "Chicken Masala", "price": 0},
{"name": "Chicken Tikka Masala", "price": 0},
{"name": "Chicken Patyala", "price": 0},
{"name": "Chicken Roganjosh", "price": 0},
{"name": "Chicken Curry", "price": 0},
{"name": "Butter Chicken", "price": 0}


],

"egg_curries": [


{"name": "Egg Curry", "price": 0},
{"name": "Egg Bhurji", "price": 0}


],

"biryani": [


{"name": "Egg Biryani", "price": 0},
{"name": "Chicken Dum Biryani", "price": 0},
{"name": "Chicken Tikka Biryani", "price": 0},
{"name": "Chicken 65 Biryani", "price": 0},
{"name": "Chicken Fry Piece Biryani", "price": 0},
{"name": "Lollipop Biryani", "price": 0},
{"name": "Tandoori Biryani", "price": 0},
{"name": "Fish Biryani", "price": 0},
{"name": "Prawn Biryani", "price": 0},
{"name": "Special Chicken Biryani", "price": 0}


],

"nonveg_chinese": [


{"name": "Egg Noodles", "price": 0},
{"name": "Egg Schezwan Noodles", "price": 0},
{"name": "Chicken Noodles", "price": 0},
{"name": "Chicken Schezwan Noodles", "price": 0},
{"name": "Prawn Noodles", "price": 0},
{"name": "Mix Non Veg Noodles", "price": 0},
{"name": "Egg Fried Rice", "price": 0},
{"name": "Chicken Fried Rice", "price": 0},
{"name": "Chicken Schezwan Rice", "price": 0},
{"name": "Chicken Chilli Garlic Rice", "price": 0},
{"name": "Mixed Non Veg Fried Rice", "price": 0}


],

"nonveg_combos": [


{"name": "Chicken Fried Rice + Chicken Manchurian", "price": 0},
{"name": "Chicken Noodles + Chicken Manchurian", "price": 0}


],

"nonveg_rice": [


{"name": "Plain Rice", "price": 0},
{"name": "Jeera Rice", "price": 0},
{"name": "Green Peas Pulao", "price": 0},
{"name": "Curd Rice", "price": 0}


],

"nonveg_parathas": [

{"name": "Chicken Keema Paratha", "price": 0}

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
{"name": "Veg Biryani Jumbo Family Pack", "price": 899}


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
@app.route("/roti")
def roti():

    table = request.args.get("table")

    return render_template(
        "roti.html",
        table=table
    )
@app.route("/chopsuey")
def chopsuey():

    table = request.args.get("table")

    return render_template(
        "chopsuey.html",
        table=table
    )


@app.route("/jumbo")
def jumbo():

    table = request.args.get("table")

    return render_template(
        "jumbo.html",
        table=table
    )


@app.route("/beverages")
def beverages():

    table = request.args.get("table")

    return render_template(
        "beverages.html",
        table=table
    )


@app.route("/papad")
def papad():

    table = request.args.get("table")

    return render_template(
        "papad.html",
        table=table
    )
if __name__ == "__main__":
    app.run(debug=True) 