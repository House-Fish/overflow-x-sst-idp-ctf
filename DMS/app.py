from lxml import etree
from flask import Flask, request, render_template

app = Flask(__name__)
parser = etree.XMLParser(load_dtd=True, resolve_entities=True)

@app.route("/", methods=["GET","POST"])
def username():
    if request.method == "POST":
        xml_data = request.data
        print(str(xml_data))
        try:
            root = etree.fromstring(xml_data, parser=parser)
            name = root.findtext('name')
            print(f"Extracted name: {name}")
            return name
        except etree.XMLSyntaxError as e:
            print(f"Error parsing XML: {e}")
        return "Posted!"
    elif request.method == "GET":
        return render_template("index.html")
