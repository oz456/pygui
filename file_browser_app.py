import tkinter as tk
from tkinter import filedialog


def browse_file():
    filepath = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as file:
                content = file.read()
        
        text_area.config(state=tk.NORMAL)
        text_area.delete('1.0', tk.END) # Clears previous content
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)
        result_label.config(text="")  # Clears previous result


def search_text():
    text_area.tag_remove("highlight", "1.0", tk.END) # Clears previous highlights
    search_term = search_entry.get()
    if not search_term:
        return

    text_area.config(state=tk.NORMAL)
    start_pos = "1.0"
    count = 0
    line_numbers = set()

    while True:
        start_pos = text_area.search(search_term, start_pos, stopindex=tk.END, nocase=True)
        if not start_pos:
            break
        end_pos = f"{start_pos}+{len(search_term)}c"
        text_area.tag_add("highlight", start_pos, end_pos)
        count += 1

        line_num = int(start_pos.split('.')[0])
        line_numbers.add(line_num)

        start_pos = end_pos

    if count > 0:
        sorted_lines = sorted(line_numbers)
        line_text = ", ".join(str(line) for line in sorted_lines)
        result_text = f"Found '{search_term}' {count} times on lines: {line_text}"
    else:
        result_text = f"'{search_term}' not found."

    result_label.config(text=result_text)
    text_area.config(state=tk.DISABLED)



### GUI ###

# Main Window Setup
root = tk.Tk()
root.title("Simple File Viewer")
root.geometry("700x500")


# Browse and Search Controls
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

browse_btn = tk.Button(top_frame, text="Browse File", command=browse_file)
browse_btn.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(top_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(top_frame, text="Analyze", command=search_text)
search_btn.pack(side=tk.LEFT, padx=5)


# Text Area with Scrollbar
text_frame = tk.Frame(root)
text_frame.pack(fill="both", expand=True)

text_area = tk.Text(text_frame, wrap="word", state=tk.DISABLED)
text_area.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
text_area.config(yscrollcommand=scrollbar.set)


# Tag for highlighting
text_area.tag_config("highlight", background="yellow")


# Result Label
result_label = tk.Label(root, text="", fg="blue", wraplength=680, justify="left")
result_label.pack(pady=5)





### Run the app ###
root.mainloop()
