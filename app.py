from datetime import datetime
import uuid

from flask import Flask, request, render_template_string

app = Flask(__name__)

FORM = """
<h2>Payment System - v3</h2>
<form method="POST">
  Name: <input name="name" value="{{ name }}" required><br><br>
  Amount: <input name="amount" type="number" value="{{ amount }}" required><br><br>
  Payment method:
  <select name="method">
    <option {{ 'selected' if method == 'Card' }}>Card</option>
    <option {{ 'selected' if method == 'UPI' }}>UPI</option>
  </select><br><br>
  Card number / UPI ID:
  <input name="detail" value="{{ detail }}" required><br><br>
  <button type="submit">Validate &amp; Pay</button>
</form>
{% if errors %}
  <ul style="color:red">
    {% for e in errors %}<li>{{ e }}</li>{% endfor %}
  </ul>
{% endif %}
"""

RECEIPT = """
<h2>Payment System - v3</h2>
<div style="border:2px solid green; padding:16px; width:360px">
  <h3 style="color:green">Payment Successful</h3>
  <p><b>Transaction ID:</b> {{ r.txn_id }}</p>
  <p><b>Name:</b> {{ r.name }}</p>
  <p><b>Amount:</b> {{ r.amount }}</p>
  <p><b>Method:</b> {{ r.method }}</p>
  <p><b>Paid with:</b> {{ r.masked }}</p>
  <p><b>Date &amp; time:</b> {{ r.time }}</p>
  <p><b>Status:</b> CONFIRMED</p>
</div>
<p><a href="/">Make another payment</a></p>
"""

def validate(name, amount, method, detail):
    errors = []
    if len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")
    try:
        value = float(amount)
        if value <= 0:
            errors.append("Amount must be greater than 0.")
        elif value > 100000:
            errors.append("Amount cannot exceed 100000.")
    except ValueError:
        errors.append("Amount must be a number.")
    if method == "Card":
        digits = detail.replace(" ", "")
        if not (digits.isdigit() and len(digits) == 16):
            errors.append("Card number must be 16 digits.")
    elif method == "UPI":
        if "@" not in detail or len(detail) < 5:
            errors.append("UPI ID must look like name@bank.")
    return errors

def mask(method, detail):
    if method == "Card":
        digits = detail.replace(" ", "")
        return "**** **** **** " + digits[-4:]
    return detail

@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    name = amount = detail = ""
    method = "Card"
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]
        method = request.form["method"]
        detail = request.form["detail"]
        errors = validate(name, amount, method, detail)
        if not errors:
            receipt = {
                "txn_id": "TXN-" + uuid.uuid4().hex[:10].upper(),
                "name": name.strip(),
                "amount": amount,
                "method": method,
                "masked": mask(method, detail),
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
            return render_template_string(RECEIPT, r=receipt)
    return render_template_string(FORM, errors=errors, name=name,
                                  amount=amount, method=method, detail=detail)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)