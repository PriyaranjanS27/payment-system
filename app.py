from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """
<h2>Payment System - v1</h2>
<form method="POST">
  Name: <input name="name" required><br><br>
  Amount: <input name="amount" type="number" required><br><br>
  Payment method:
  <select name="method">
    <option>Card</option><option>UPI</option>
  </select><br><br>
  <button type="submit">Pay</button>
</form>
{% if msg %}<p><b>{{ msg }}</b></p>{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    msg = None
    if request.method == "POST":
        msg = f"Payment of {request.form['amount']} by {request.form['name']} received via {request.form['method']}"
    return render_template_string(PAGE, msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)