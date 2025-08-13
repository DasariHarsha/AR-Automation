import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import shutil
import os
from excel_utils import read_credentials_excel, read_excel_and_filter
from main import run_automation_with_inputs
import base64
# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
 
 
# Window setup
app = ctk.CTk()
app.title("ARAuto-SIM")
app.state("zoomed")  # Full screen
app.resizable(True, True)
 
# --- FAQ Button and Dialog ---
def show_faq():
    faq = ctk.CTkToplevel(app)
    faq.title("How to Use - FAQ")
    faq.geometry("520x420")
    faq.resizable(False, False)
    faq.grab_set()
    faq.attributes("-topmost", True)
    faq.configure(fg_color="#181818")
    # Center the popup
    faq_width = 520
    faq_height = 420
 
# Calculate position to center relative to main window
    x = app.winfo_x() + (app.winfo_width() // 2) - (faq_width // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (faq_height // 2)
 
    faq.geometry(f"{faq_width}x{faq_height}+{x}+{y}")
 
    title = ctk.CTkLabel(faq, text="❓ How to Use ARAuto Dashboard", font=("Consolas", 22, "bold"), text_color="#00FFFF")
    title.pack(pady=(18, 10))
    instr = (
        "1. Upload your Credentials Excel and VM Template Excel using the Browse buttons.\n"
        "2. Select 'Yes' or 'No' for both Skip RStrategy and Skip Instance.\n"
        "3. Click '🚀 Start Automation' to begin.\n\n"
        "• The automation will use the uploaded files and your choices.\n"
        "• You will see a fun animation and status popups.\n"
        "• All results and errors will be shown in dialog boxes.\n\n"
        "Note: All entries are case sensitive. Please ensure that R-Strategy, business functions, InstanceType, and region are entered with the correct capitalization.\n"
        "• The R-Strategy must adhere to Concierto's case sensitivity, for example: Rehost, Re-Platform, Retire.\n\n"
        "Tip: Make sure your Excel files are formatted as required!"
    )
    instr_label = ctk.CTkLabel(faq, text=instr, font=("Consolas", 16), text_color="#FFFFFF", wraplength=480, justify="left")
    instr_label.pack(padx=18, pady=(0, 18))
    close_btn = ctk.CTkButton(faq, text="Close", command=faq.destroy, font=("Consolas", 16), fg_color="#00FFFF", text_color="#181818", hover_color="#00CCCC", width=120)
    close_btn.pack(pady=(0, 18))
 
# Place FAQ button in top-right corner
faq_btn = ctk.CTkButton(
    app,
    text="❓ Instructions",
    command=show_faq,
    font=("Consolas", 16, "bold"),
    fg_color="#222222",
    text_color="#00FFFF",
    hover_color="#393939",
    width=80,
    height=36,
    corner_radius=18
)
faq_btn.place(relx=0.97, rely=0.02, anchor="ne")
 
# Load and place background image
 
 
# Semi-transparent overlay frame
main_frame = ctk.CTkFrame(app, corner_radius=20, fg_color="#121212")
main_frame.place(relx=0.07, rely=0.07, relwidth=0.9, relheight=0.9)
 
# Title
title = ctk.CTkLabel(main_frame, text="🌐 ARAuto Dashboard", font=("Consolas", 34, "bold"), text_color="#00FFFF")
title.pack(pady=(20, 10))
 
# Encoded developer text (Base64) - DO NOT MODIFY
_dev_encoded = "SEwgQ28tQ3JlYXRpb25zIPCfmoA="
developer_text = base64.b64decode(_dev_encoded).decode('utf-8')
# Tooltip for title
tooltip = None
def show_title_tooltip(event=None):
    global tooltip
    if tooltip is not None:
        return
    x = title.winfo_rootx() + title.winfo_width() // 2
    y = title.winfo_rooty() + title.winfo_height() + 8
    tooltip = tk.Toplevel(app)
    tooltip.overrideredirect(True)
    tooltip.geometry(f"+{x}+{y}")
    tip_label = tk.Label(tooltip, text=developer_text, font=("Consolas", 16), bg="#222", fg="#F9FAF5", padx=12, pady=6, bd=0)
    tip_label.pack()
 
def hide_title_tooltip(event=None):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None
 
title.bind("<Enter>", show_title_tooltip)
title.bind("<Leave>", hide_title_tooltip)
 
 
# Variables for file paths
credentials_path = ctk.StringVar()
vm_template_path = ctk.StringVar()
 
# Variables for radio buttons
skip_rstrategy_var = tk.StringVar(value="")
skip_instance_var = tk.StringVar(value="")
 
# File browsing function
def browse_file(var, is_vm_template=False):
    path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
    if path:
        var.set(path)
        # If this is the VM template, copy to Files/Cop.xlsx
        if is_vm_template:
            dest = os.path.join("Files", "Cop.xlsx")
            try:
                shutil.copy2(path, dest)
            except Exception as e:
                messagebox.showerror("File Copy Error", f"Failed to copy VM template: {e}")
 
# Input block function with styled browse button
def input_block(label_text, var, color, is_vm_template=False):
    block = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#1c1c1c")
    block.pack(pady=10, padx=50, fill="x")
 
    label = ctk.CTkLabel(block, text=label_text, font=("Consolas", 20), text_color=color)
    label.pack(anchor="w", padx=20, pady=(8, 3))
 
    inner = ctk.CTkFrame(block, fg_color="#282828")
    inner.pack(padx=15, pady=8, fill="x")
 
    entry = ctk.CTkEntry(inner, textvariable=var, font=("Consolas", 16), height=40)
    entry.pack(side="left", padx=10, pady=8, expand=True, fill="x")
 
    browse_icon = "🔍"
 
    button = ctk.CTkButton(inner, text=f"{browse_icon} Browse", font=("Consolas", 16), height=40,
                           width=140, fg_color="#202020", hover_color="#393939",
                           text_color="#FF69B4",
                           command=lambda: browse_file(var, is_vm_template=is_vm_template))
    button.pack(side="right", padx=10)
 
# Input blocks
input_block("🔐 Credentials File", credentials_path, "#FFD6A5")

# Note with download template for credentials
note_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
note_frame.pack(pady=(0, 5), padx=50, fill="x")

def download_cred_template():
    try:
        source = os.path.join("Files", "Sample_Cred_Template.xlsx")
        
        # Get user's Downloads folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_filename = "Sample_Cred_Template.xlsx"
        dest = os.path.join(downloads_path, base_filename)
        
        if os.path.exists(source):
            # Check if file already exists and create a copy with number
            counter = 1
            while os.path.exists(dest):
                name, ext = os.path.splitext(base_filename)
                dest = os.path.join(downloads_path, f"{name} ({counter}){ext}")
                counter += 1
            
            # Silent download like browser - no popup message
            shutil.copy(source, dest)
            
            # Optional: Brief visual feedback by changing button color temporarily
            download_btn.configure(fg_color="#2B9C45", text="✓")  # Green checkmark
            app.after(3000, lambda: download_btn.configure(fg_color="#38A2CF", text="⬇️"))  # Reset after 2 sec
            
        else:
            messagebox.showerror("File Not Found", "Sample credential template not found in Files folder!")
    except Exception as e:
        messagebox.showerror("Download Error", f"Failed to download template: {e}")

note_text = ctk.CTkLabel(note_frame, text="📝 Sample Cred template for your reference", 
                        font=("Consolas", 14), text_color="#AAAAAA")
note_text.pack(side="left", padx=(20, 10))

download_btn = ctk.CTkButton(note_frame, text="⬇️", font=("Consolas", 16, "bold"), 
                            width=30, height=30, fg_color="#38A2CF", 
                            hover_color="#2B9C45", text_color="white",
                            corner_radius=8,
                            command=download_cred_template)
download_btn.pack(side="left", padx=(20, 10))

input_block("📦 VM Template File", vm_template_path, "#FFD6A5", is_vm_template=True)

# Note with download template for VM Template
vm_note_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
vm_note_frame.pack(pady=(0, 5), padx=50, fill="x")

def download_vm_template():
    try:
        source = os.path.join("Files", "Sample_VM_Template.xlsx")
        
        # Get user's Downloads folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_filename = "Sample_VM_Template.xlsx"
        dest = os.path.join(downloads_path, base_filename)
        
        if os.path.exists(source):
            # Check if file already exists and create a copy with number
            counter = 1
            while os.path.exists(dest):
                name, ext = os.path.splitext(base_filename)
                dest = os.path.join(downloads_path, f"{name} ({counter}){ext}")
                counter += 1
            
            # Silent download like browser - no popup message
            shutil.copy(source, dest)
            
            # Optional: Brief visual feedback by changing button color temporarily
            vm_download_btn.configure(fg_color="#2B9C45", text="✓")  # Green checkmark
            app.after(3000, lambda: vm_download_btn.configure(fg_color="#38A2CF", text="⬇️"))  # Reset after 3 sec
            
        else:
            messagebox.showerror("File Not Found", "Sample VM template not found in Files folder!")
    except Exception as e:
        messagebox.showerror("Download Error", f"Failed to download VM template: {e}")

vm_note_text = ctk.CTkLabel(vm_note_frame, text="📝 Sample VM template for your reference", 
                        font=("Consolas", 14), text_color="#AAAAAA")
vm_note_text.pack(side="left", padx=(20, 10))

vm_download_btn = ctk.CTkButton(vm_note_frame, text="⬇️", font=("Consolas", 16, "bold"), 
                            width=30, height=30, fg_color="#38A2CF", 
                            hover_color="#2B9C45", text_color="white",
                            corner_radius=8,
                            command=download_vm_template)
vm_download_btn.pack(side="left", padx=(20, 10))
 
# Frame to hold radio buttons + Start Button
bottom_row = ctk.CTkFrame(main_frame, fg_color="transparent")
bottom_row.pack(pady=(10, 5), padx=20, fill="x")
 
# Frame for radio buttons
radio_frame = ctk.CTkFrame(bottom_row, fg_color="transparent")
radio_frame.pack(side="left", padx=50, fill="y")
 
# Radio buttons for Skip RStrategy
ctk.CTkLabel(radio_frame, text="Skip RStrategy Selection", font=("Consolas", 18), text_color="white").pack(anchor="w")
r_frame = ctk.CTkFrame(radio_frame, fg_color="transparent")
r_frame.pack(anchor="w", pady=(5, 15))
ctk.CTkRadioButton(r_frame, text="Yes", variable=skip_rstrategy_var, value="Yes").pack(side="left", padx=10)
ctk.CTkRadioButton(r_frame, text="No", variable=skip_rstrategy_var, value="No").pack(side="left", padx=10)
 
# Radio buttons for Skip Instance
ctk.CTkLabel(radio_frame, text="Skip Instance Selection", font=("Consolas", 18), text_color="white").pack(anchor="w")
i_frame = ctk.CTkFrame(radio_frame, fg_color="transparent")
i_frame.pack(anchor="w", pady=(5, 0))
ctk.CTkRadioButton(i_frame, text="Yes", variable=skip_instance_var, value="Yes").pack(side="left", padx=10)
ctk.CTkRadioButton(i_frame, text="No", variable=skip_instance_var, value="No").pack(side="left", padx=10)
 
 
# Glowing animation colors
glow_colors = ["#FF6B6B", "#FF8C69", "#FF6B6B", "#FF4F4F"]
color_index = 0
 
def pulse_button():
    global color_index
    run_btn.configure(fg_color=glow_colors[color_index])
    color_index = (color_index + 1) % len(glow_colors)
    app.after(500, pulse_button)
 
 
# --- Animated popup before Chrome driver opens ---
def show_loader_popup(callback):
    loader_popup = ctk.CTkToplevel(app)
    loader_popup.title("Launching Automation...")
    loader_popup.geometry("400x220")
    loader_popup.resizable(False, False)
    loader_popup.grab_set()
    loader_popup.attributes("-topmost", True)
    loader_popup.configure(fg_color="#181818")
    # Center the popup
    x = app.winfo_x() + (app.winfo_width() // 2) - 200
    y = app.winfo_y() + (app.winfo_height() // 2) - 110
    loader_popup.geometry(f"+{x}+{y}")
 
    # Animated spinner
    spinner_emojis = ["🌀", "🌟", "✨", "🚀", "💫", "🛸", "🪐"]
    spinner_label = ctk.CTkLabel(loader_popup, text="", font=("Consolas", 60, "bold"), text_color="#00FFFF")
    spinner_label.pack(pady=(30, 10))
    msg_label = ctk.CTkLabel(loader_popup, text="Preparing for launch...", font=("Consolas", 20), text_color="#FFFFFF")
    msg_label.pack()
 
    def animate_spinner(idx=0, count=0):
        spinner_label.configure(text=spinner_emojis[idx % len(spinner_emojis)])
        if count < 12:  # ~1.5s
            loader_popup.after(120, animate_spinner, idx + 1, count + 1)
        else:
            loader_popup.destroy()
            callback()
    animate_spinner()
 
def run_automation():
    cred = credentials_path.get().strip()
    vm = vm_template_path.get().strip()
    skip_r = skip_rstrategy_var.get()
    skip_i = skip_instance_var.get()
 
    if not cred or not vm:
        messagebox.showwarning("Missing Input", "Please select both files before running automation.")
        return
 
    if skip_r == "" or skip_i == "":
        messagebox.showwarning("Missing Option", "Please select Yes or No for both options.")
        return
 
    # Read credentials from Excel
    try:
        creds = read_credentials_excel(cred)
    except Exception as e:
        messagebox.showerror("Credentials Error", f"Failed to read credentials: {e}")
        return
 
    username = creds['username']
    password = creds['password']
    report_name = creds['reportname']
    business_functions = [b.strip() for b in str(creds['businessfunctions']).split(",") if b.strip()]
    region = creds['region']
 
    # Prepare filtered data for automation
    try:
        filtered, region_val = read_excel_and_filter(business_functions, region)
    except Exception as e:
        messagebox.showerror("Excel Error", f"Failed to read VM template: {e}")
        return
 
    def start_actual_automation():
        try:
            run_automation_with_inputs(
                username, password, report_name, filtered, region_val, creds['url'],
                skip_rstrategy=skip_r, skip_instance=skip_i)
            messagebox.showinfo("Automation Complete", "Automation finished successfully.")
        except Exception as e:
            messagebox.showerror("Automation Error", f"Automation failed: {e}")
 
    # Show animated popup, then start automation
    show_loader_popup(lambda: app.after(100, start_actual_automation))
 
# Run Automation Button
run_btn = ctk.CTkButton(
    bottom_row,
    text="🚀 Start Automation",
    command=run_automation,
    font=("Consolas", 22, "bold"),
    height=55,
    width=320,
    corner_radius=15,
    fg_color=glow_colors[0],
    hover_color="#DD4444",
    text_color="#FFFFFF"
)
run_btn.pack(side="left", padx=50)

# Support contact text at bottom right
support_text = ctk.CTkLabel(
    bottom_row,
    text="For support Contact:\nharshavardhan.reddy/laharesh.gali",
    font=("Consolas", 12),
    text_color="#888888",
    justify="right"
)
support_text.pack(side="right", padx=30, anchor="se")
 
# Start glowing animation
pulse_button()
 
# Start app
app.mainloop()