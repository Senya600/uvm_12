import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import traceback
import json
import os

from uvm_asm import assemble_json
from uvm_interp import execute


class UVMGuiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UVM — Variant 12 (Assembler + Interpreter)")
        self.geometry("1100x700")

        self.bytecode = None
        self.IR = None
        self.memory = None

        self.create_widgets()

    def create_widgets(self):
        top = ttk.Frame(self)
        top.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # ===== LEFT: JSON editor =====
        left = ttk.Frame(top)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Program (JSON, Variant 12):").pack(anchor="w")

        self.text_prog = tk.Text(left, wrap="none")
        self.text_prog.pack(fill=tk.BOTH, expand=True)

        self.text_prog.insert("1.0", self.default_program())

        # ===== RIGHT =====
        right = ttk.Frame(top, width=420)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        controls = ttk.LabelFrame(right, text="Controls")
        controls.pack(fill=tk.X, padx=4, pady=4)

        ttk.Button(controls, text="Assemble & Run", command=self.on_run).pack(fill=tk.X, pady=2)
        ttk.Button(controls, text="Save binary...", command=self.save_binary).pack(fill=tk.X, pady=2)
        ttk.Button(controls, text="Save dump CSV...", command=self.save_dump).pack(fill=tk.X, pady=2)

        frm = ttk.Frame(controls)
        frm.pack(fill=tk.X, pady=4)
        ttk.Label(frm, text="Dump range:").pack(side=tk.LEFT)
        self.ent_range = ttk.Entry(frm, width=12)
        self.ent_range.pack(side=tk.LEFT, padx=4)
        self.ent_range.insert(0, "95-135")

        # ===== MEMORY TABLE =====
        mem = ttk.LabelFrame(right, text="Memory dump")
        mem.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.tree = ttk.Treeview(mem, columns=("addr", "value"), show="headings")
        self.tree.heading("addr", text="addr")
        self.tree.heading("value", text="value")
        self.tree.column("addr", width=80, anchor="center")
        self.tree.column("value", width=120, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # ===== BOTTOM =====
        bottom = ttk.Frame(self)
        bottom.pack(fill=tk.X, padx=6, pady=6)

        ttk.Label(bottom, text="Bytecode (hex):").pack(anchor="w")
        self.txt_bytecode = tk.Text(bottom, height=4)
        self.txt_bytecode.pack(fill=tk.X)

        ttk.Label(bottom, text="IR:").pack(anchor="w")
        self.txt_ir = tk.Text(bottom, height=6)
        self.txt_ir.pack(fill=tk.X)

        self.status = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def default_program(self):
        return json.dumps([
            { "op": "load_const", "B": 27, "C": 898 },
            { "op": "read_value", "B": 4, "C": 54, "D": 396 },
            { "op": "write_value", "B": 24, "C": 562 },
            { "op": "pow", "B": 82, "C": 17, "D": 125 }
        ], indent=2)

    def on_run(self):
        try:
            prog = json.loads(self.text_prog.get("1.0", tk.END))
            bytecode, IR = assemble_json(prog)

            self.bytecode = bytecode
            self.IR = IR

            # bytecode hex
            self.txt_bytecode.delete("1.0", tk.END)
            self.txt_bytecode.insert(
                "1.0",
                " ".join(f"{b:02X}" for b in bytecode)
            )

            # IR
            self.txt_ir.delete("1.0", tk.END)
            self.txt_ir.insert("1.0", "\n".join(str(x) for x in IR))

            # execute
            self.memory = execute(bytecode)

            # dump
            for i in self.tree.get_children():
                self.tree.delete(i)

            s, e = map(int, self.ent_range.get().split("-"))
            for addr in range(s, e + 1):
                self.tree.insert("", "end", values=(addr, self.memory[addr]))

            self.status.config(text=f"Executed {len(IR)} instructions")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            traceback.print_exc()

    def save_binary(self):
        if not self.bytecode:
            return
        path = filedialog.asksaveasfilename(defaultextension=".bin")
        if path:
            with open(path, "wb") as f:
                f.write(self.bytecode)

    def save_dump(self):
        if not self.memory:
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if not path:
            return
        s, e = map(int, self.ent_range.get().split("-"))
        with open(path, "w", encoding="utf-8") as f:
            f.write("addr,value\n")
            for i in range(s, e + 1):
                f.write(f"{i},{self.memory[i]}\n")


if __name__ == "__main__":
    app = UVMGuiApp()
    app.mainloop()
