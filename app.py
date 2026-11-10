"""Week 3: look at the features of one address, and at the prepared data."""
import pandas as pd
from flask import Flask, render_template, request

from urlfeatures import check_url, extract

app = Flask(__name__)
data = pd.read_csv("data/urls.csv")


@app.route("/")
def check():
    text = request.args.get("url", "")
    features, error, clean = None, None, None
    if text:
        clean, error = check_url(text)
        if error is None:
            features = extract(clean)
    return render_template("check.html", text=text, clean=clean, error=error, features=features)


@app.route("/data")
def data_page():
    counts = data["is_phishing"].value_counts().to_dict()
    samples = {"phishing": data[data["is_phishing"] == 1]["url"].head(10).tolist(),
               "legitimate": data[data["is_phishing"] == 0]["url"].head(10).tolist()}
    return render_template("data.html", n=len(data), counts=counts, hosts=data["host"].nunique(), samples=samples)


if __name__ == "__main__":
    app.run(debug=True)
