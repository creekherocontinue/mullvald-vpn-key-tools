"""Minimal Tkinter shell for the Mullvald key generator.

The GUI is a thin wrapper: it collects parameters, calls the same
handlers the CLI uses, and renders the resulting keys. No business
logic lives here.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from mullvald.core.context import KeygenContext
from mullvald.core.engine import KeygenEngine
from mullvald.handlers.generate import GenerateHandler


def launch() -> None:
    ctx = KeygenContext.load(None, allow_network=False)
    ctx.engine = KeygenEngine(ctx)

    root = tk.Tk()
    root.title("Mullvald VPN Key Generator")
    root.geometry("620x420")

    tier = tk.StringVar(value="plus")
    days = tk.IntVar(value=30)
    count = tk.IntVar(value=1)

    ttk.Label(root, text="Tier").pack(anchor="w", padx=12, pady=(12, 0))
    ttk.Combobox(root, textvariable=tier, values=["basic", "plus", "pro", "team"]).pack(
        anchor="w", padx=12
    )
    ttk.Label(root, text="Days").pack(anchor="w", padx=12, pady=(8, 0))
    ttk.Spinbox(root, from_=1, to=3650, textvariable=days).pack(anchor="w", padx=12)
    ttk.Label(root, text="Count").pack(anchor="w", padx=12, pady=(8, 0))
    ttk.Spinbox(root, from_=1, to=500, textvariable=count).pack(anchor="w", padx=12)

    output = tk.Text(root, height=12, font=("Consolas", 10))
    output.pack(fill="both", expand=True, padx=12, pady=12)

    def on_generate() -> None:
        handler = GenerateHandler(ctx)
        keys = handler.run(tier=tier.get(), days=days.get(), count=count.get(), out_path=None)
        output.delete("1.0", tk.END)
        output.insert(tk.END, "\n".join(keys))

    def on_export() -> None:
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(output.get("1.0", tk.END).strip())
        messagebox.showinfo("Mullvald", f"Written to {path}")

    bar = ttk.Frame(root)
    bar.pack(fill="x", padx=12, pady=(0, 12))
    ttk.Button(bar, text="Generate", command=on_generate).pack(side="left")
    ttk.Button(bar, text="Export", command=on_export).pack(side="left", padx=8)

    root.mainloop()


def main() -> None:
    launch()