from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """
<h2>Payment System - v2</h2>
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
{% if msg %}<p style="color:green"><b>{{ msg }}</b></p>{% endif %}
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

@app.route("/", methods=["GET", "POST"])
def index():
    msg, errors = None, []
    name = amount = detail = ""
    method = "Card"
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]
        method = request.form["method"]
        detail = request.form["detail"]
        errors = validate(name, amount, method, detail)
        if not errors:
            msg = f"Payment details valid: {amount} by {name} via {method}"
    return render_template_string(PAGE, msg=msg, errors=errors,
                                  name=name, amount=amount,
                                  method=method, detail=detail)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)