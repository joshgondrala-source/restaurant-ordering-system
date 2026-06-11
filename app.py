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
    "Biryani": [
        {
            "name": "Chicken Dum Biryani",
            "price": 289,
            "serves": "2 People",
            "spice": "Medium 🌶🌶"
        },
        {
            "name": "Veg Biryani",
            "price": 229,
            "serves": "2 People",
            "spice": "Mild 🌶"
        },
        {
            "name": "Paneer Biryani",
            "price": 249,
            "serves": "2 People",
            "spice": "Medium 🌶🌶"
        }
    ],

    "Roti": [
        {
            "name": "Plain Naan",
            "price": 45,
            "serves": "2 Pieces"
        },
        {
            "name": "Butter Naan",
            "price": 50,
            "serves": "2 Pieces"
        },
        {
            "name": "Garlic Naan",
            "price": 70,
            "serves": "2 Pieces"
        }
    ],

    "Kukkad": [
        {
            "name": "Butter Chicken",
            "price": 329,
            "serves": "2-3 People",
            "spice": "Medium 🌶🌶"
        },
        {
            "name": "Chicken Curry",
            "price": 299,
            "serves": "2-3 People",
            "spice": "Medium 🌶🌶"
        },
        {
            "name": "Paneer Butter Masala",
            "price": 279,
            "serves": "2-3 People",
            "spice": "Mild 🌶"
        }
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

    orders.append({
        "order_id": order_counter,
        "table": current_table,
        "items": cart.copy(),
        "total": total,
        "time": datetime.now().strftime("%I:%M %p")
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

if __name__ == "__main__":
    app.run(debug=True) 