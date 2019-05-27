import requests as r
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_restful import Api, Resource, reqparse

from f5_manager import F5Manager

app = Flask(__name__)
api = Api(app)
f5man = F5Manager()

virtual_parser = reqparse.RequestParser()
virtual_parser.add_argument("name")
virtual_parser.add_argument("partition")
virtual_parser.add_argument("source")
virtual_parser.add_argument("destination")
virtual_parser.add_argument("description")


class Virtual(Resource):
    def get(self, v_partition, v_name):
        args = {"partition": v_partition, "name": v_name}
        v = f5man.get_virtual(**args)
        data = {
            "name": v.raw["name"],
            "partition": v.raw["partition"],
            "enabled": True if "enabled" in v.raw else False,
            "source": v.raw["source"],
            "destination": v.raw["destination"].split("/")[-1],
            "description": v.raw["description"] if "description" in v.raw else "",
        }
        return jsonify(data)

    def delete(self, v_partition, v_name):
        args = {"partition": v_partition, "name": v_name}
        f5man.delete_virtual(**args)
        return "", 204

    def put(self, v_partition, v_name):
        args = {}
        r_args = virtual_parser.parse_args()
        args.update(r_args)
        args.update({"partition": v_partition, "name": v_name})
        f5man.update_virtual(**args)
        return "", 200


class VirtualList(Resource):
    def get(self):
        virtuals = f5man.get_virtuals()
        data = []
        for v in virtuals:
            data.append(
                {
                    "name": v.raw["name"],
                    "partition": v.raw["partition"],
                    "enabled": True if "enabled" in v.raw else False,
                    "source": v.raw["source"],
                    "destination": v.raw["destination"].split("/")[-1],
                    "description": v.raw["description"]
                    if "description" in v.raw
                    else "",
                }
            )
        return jsonify(data)

    def post(self):
        args = virtual_parser.parse_args()
        f5man.create_virtual(**args)
        return "", 201


api.add_resource(VirtualList, "/api/virtuals")
api.add_resource(Virtual, "/api/virtuals/<string:v_partition>/<string:v_name>")


@app.route("/")
def home():
    return render_template("home.html", connected=f5man.is_connected())


@app.route("/virtuals")
def virtual_servers_list():
    result = r.get("http://localhost:5000/api/virtuals")
    return render_template(
        "virtuals/virtuals.html", connected=f5man.is_connected(), virtuals=result.json()
    )


@app.route("/virtuals/<string:partition>/<string:name>", methods=["GET", "POST"])
def virtual_server(name, partition):
    if request.method == "POST":
        if "action" in request.form and request.form["action"] == "delete":
            r.delete(f"http://localhost:5000/api/virtuals/{partition}/{name}")
        else:
            r.put(
                f"http://localhost:5000/api/virtuals/{partition}/{name}",
                data=request.form,
            )
        return redirect(url_for("virtual_servers_list"))
    if request.method == "DELETE":
        r.delete(f"http://localhost:5000/api/virtuals/{partition}/{name}")
        return redirect(url_for("virtual_servers_list"))
    result = r.get(f"http://localhost:5000/api/virtuals/{partition}/{name}")
    return render_template(
        "virtuals/virtual.html", connected=f5man.is_connected(), virtual=result.json()
    )


@app.route("/virtuals/create", methods=["GET", "POST"])
def virtual_server_create():
    if request.method == "POST":
        r.post(f"http://localhost:5000/api/virtuals", data=request.form)
        return redirect(url_for("virtual_servers_list"))
    return render_template("virtuals/virtual.html", connected=f5man.is_connected())


if __name__ == "__main__":
    f5man.connect()
    app.run()
