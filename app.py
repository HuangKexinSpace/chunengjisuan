from flask import Flask, render_template, request

app = Flask(__name__)

def get_float(form, field, default):
    value = form.get(field, '')
    if value == '':
        return default
    try:
        return float(value)
    except ValueError:
        return default

def get_int(form, field, default):
    value = form.get(field, '')
    if value == '':
        return default
    try:
        return int(value)
    except ValueError:
        return default

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        C1 = get_float(request.form, "C1", 436500000)
        C2 = get_float(request.form, "C2", 2200000)

        lowfee = get_float(request.form, "lowfee", 0.323)
        midfee = get_float(request.form, "midfee", 0.807)
        highfee = get_float(request.form, "highfee", 1.353)
        days = get_int(request.form, "days", 330)
        efficiency = get_float(request.form, "efficiency", 0.86)
        discount_rate = get_float(request.form, "discount_rate", 0.04)

        rawcapacity1 = get_int(request.form, "rawcapacity1", 200000)
        perreduction1 = get_int(request.form, "perreduction1", 2800)
        capacities1 = [rawcapacity1 - perreduction1 * i for i in range(10)]

        percost1 = lowfee * days + midfee * days
        perprofit1 = highfee * days * 2 * efficiency
        perown1 = perprofit1 - percost1

        year1_cost1 = C1 + C2
        year1_profit1 = perown1 * capacities1[0]
        year1_netprofit1 = year1_profit1 - year1_cost1

        costs1 = [year1_cost1]
        profits1 = [year1_profit1]

        netprofits1 = [year1_netprofit1]

        for i in range(1, 10):
            year_cost = costs1[-1] + C2
            year_profit = profits1[-1] + perown1 * capacities1[i] / ((1 + discount_rate) ** i)
            year_netprofit = year_profit - year_cost
            costs1.append(year_cost)
            profits1.append(year_profit)
            netprofits1.append(year_netprofit)

        rawcapacity2 = get_int(request.form, "rawcapacity2", 200000)
        perreduction2 = get_int(request.form, "perreduction2", 1800)
        capacities2 = [rawcapacity2 - perreduction2 * i for i in range(10)]

        percost2 = lowfee * days
        perprofit2 = highfee * days * efficiency
        perown2 = perprofit2 - percost2

        year1_cost2 = C1 + C2
        year1_profit2 = perown2 * capacities2[0]
        year1_netprofit2 = year1_profit2 - year1_cost2

        costs2 = [year1_cost2]
        profits2 = [year1_profit2]

        netprofits2 = [year1_netprofit2]

        for i in range(1, 10):
            year_cost = costs2[-1] + C2
            year_profit = profits2[-1] + perown2 * capacities2[i] / ((1 + discount_rate) ** i)
            year_netprofit = year_profit - year_cost
            costs2.append(year_cost)
            profits2.append(year_profit)
            netprofits2.append(year_netprofit)

        return render_template("index.html", netprofits1=netprofits1, netprofits2=netprofits2)

    return render_template("index.html", netprofits1=None, netprofits2=None)

if __name__ == "__main__":
    app.run(debug=True)
