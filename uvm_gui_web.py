from flask import Flask, render_template, request, jsonify
import json
import traceback

from uvm_asm import assemble_json
from uvm_interp import execute

app = Flask(__name__)


def default_demo_program():
    return [
        { "op": "load_const", "B": 10, "C": 2 },
        { "op": "load_const", "B": 11, "C": 3 },

        { "op": "write_value", "B": 10, "C": 100 },
        { "op": "write_value", "B": 11, "C": 101 },

        { "op": "load_const", "B": 0, "C": 101 },

        { "op": "pow", "B": 0, "C": 120, "D": 100 }
    ]


@app.route("/")
def index():
    return render_template(
        "index.html",
        demo_program=json.dumps(default_demo_program(), indent=2)
    )


@app.route("/run", methods=["POST"])
def run_program():
    try:
        program = request.json.get("program")
        dump_range = request.json.get("range", "95-135")

        bytecode, IR = assemble_json(program)
        memory = execute(bytecode)

        start, end = map(int, dump_range.split("-"))
        dump = [
            {"addr": i, "value": memory[i]}
            for i in range(start, end + 1)
        ]

        return jsonify({
            "ok": True,
            "bytecode": " ".join(f"{b:02X}" for b in bytecode),
            "ir": [str(x) for x in IR],
            "dump": dump
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "ok": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
