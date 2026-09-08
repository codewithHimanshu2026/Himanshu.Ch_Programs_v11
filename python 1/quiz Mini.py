import random
import tkinter as tk
from tkinter import messagebox, scrolledtext

# -----------------------------
# Dynamic Technical Question Bank
# -----------------------------
TECH_QUESTIONS = [
    {
        "id": 1,
        "category": "PYTHON",
        "question": "What is the average time complexity of searching an item in a Python Dictionary (hash map)?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "answer": "O(1)",
        "explanation": "Python dictionaries use hash tables, offering average O(1) time complexity for key lookups.",
    },
    {
        "id": 2,
        "category": "NETWORKING",
        "question": "Which OSI layer is responsible for encryption and compression (e.g., SSL/TLS)?",
        "options": [
            "Transport Layer",
            "Presentation Layer",
            "Application Layer",
            "Session Layer",
        ],
        "answer": "Presentation Layer",
        "explanation": "Layer 6 (Presentation) formats, encrypts, and compresses data before sending it to Layer 7.",
    },
    {
        "id": 3,
        "category": "CYBER SECURITY",
        "question": "Which cryptographic approach uses a pair of Public and Private keys?",
        "options": [
            "Symmetric Encryption",
            "Asymmetric Encryption",
            "Hashing",
            "Steganography",
        ],
        "answer": "Asymmetric Encryption",
        "explanation": "Asymmetric algorithms (like RSA) use a public key for encryption and a private key for decryption.",
    },
    {
        "id": 4,
        "category": "DEV-OPS",
        "question": "Which command in Docker builds an image from a Dockerfile in the current directory?",
        "options": [
            "docker run .",
            "docker build -t app .",
            "docker create .",
            "docker compile",
        ],
        "answer": "docker build -t app .",
        "explanation": "'docker build' reads instructions in Dockerfile and tags (-t) the generated container image.",
    },
    {
        "id": 5,
        "category": "DATA STRUCTURES",
        "question": "Which data structure is optimal for implementing Breadth-First Search (BFS) in a Graph?",
        "options": ["Stack", "Queue", "Priority Queue", "Binary Search Tree"],
        "answer": "Queue",
        "explanation": "BFS explores nodes level by level using FIFO ordering provided by a Queue.",
    },
    {
        "id": 6,
        "category": "WEB DEV",
        "question": "In JavaScript, which array method creates a new array filled with the results of calling a provided function?",
        "options": ["forEach()", "map()", "filter()", "reduce()"],
        "answer": "map()",
        "explanation": "map() transforms every element in an array and returns a new array with transformed values.",
    },
    {
        "id": 7,
        "category": "AI / ML",
        "question": "Which evaluation metric is ideal for highly imbalanced classification datasets?",
        "options": [
            "Accuracy",
            "Precision-Recall / F1-Score",
            "Mean Squared Error",
            "R-Squared",
        ],
        "answer": "Precision-Recall / F1-Score",
        "explanation": "F1-Score balances Precision and Recall, preventing false high accuracy scores on skewed data.",
    },
    {
        "id": 8,
        "category": "OPERATING SYSTEMS",
        "question": "What is 'Thrashing' in Operating Systems?",
        "options": [
            "CPU executing an infinite loop",
            "Excessive page swapping between RAM and Disk",
            "Hardware overheating deadlock",
            "Kernel crash due to memory leak",
        ],
        "answer": "Excessive page swapping between RAM and Disk",
        "explanation": "Thrashing occurs when the OS spends more time swapping pages in/out of virtual memory than executing actual tasks.",
    },
    {
        "id": 9,
        "category": "DATABASE",
        "question": "Which SQL isolation level prevents both Dirty Reads and Non-Repeatable Reads?",
        "options": [
            "Read Uncommitted",
            "Read Committed",
            "Repeatable Read",
            "Serializable",
        ],
        "answer": "Repeatable Read",
        "explanation": "Repeatable Read locks data accessed during a transaction, eliminating dirty and non-repeatable reads.",
    },
    {
        "id": 10,
        "category": "CLOUD / AWS",
        "question": "Which AWS service provides serverless compute execution based on events?",
        "options": ["EC2", "ECS", "AWS Lambda", "Elastic Beanstalk"],
        "answer": "AWS Lambda",
        "explanation": "AWS Lambda runs code automatically in response to events without requiring server provisioning.",
    },
]

TOTAL_TEST_TIME = 300  # 300 seconds (5 mins)

# Color Palette (Dark Cyber Theme)
COLOR_BG = "#0f1016"
COLOR_CARD = "#1a1c28"
COLOR_TEXT = "#c0caf5"
COLOR_ACCENT = "#7aa2f7"
COLOR_MUTED = "#565f89"
COLOR_PRIMARY = "#bb9af7"
COLOR_SUCCESS = "#9ece6a"
COLOR_WARNING = "#e0af68"
COLOR_ERROR = "#f7768e"


class MajorQuizEngineApp:

    def __init__(self, root):
        self.root = root
        self.root.title("CYBER-TEST ASSESSMENT SYSTEM - MAJOR PROJECT")
        self.root.geometry("850x680")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        # User Profile Data
        self.user_name = tk.StringVar()
        self.user_roll = tk.StringVar()
        self.user_domain = tk.StringVar(value="Software Engineering")

        # Exam State Data
        self.questions = []
        self.current_idx = 0
        self.user_responses = {}
        self.time_left = TOTAL_TEST_TIME
        self.timer_job = None

        # Container Frame for Switching Pages
        self.container = tk.Frame(self.root, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True)

        # GRID WEIGHTS FIX: Enables frame expansion & visibility
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Page Initializations
        for PageClass in (
            WelcomePage,
            InstructionsPage,
            TestPage,
            ScorecardPage,
        ):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("WelcomePage")

    def show_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def start_exam(self):
        self.questions = TECH_QUESTIONS.copy()
        random.shuffle(self.questions)
        self.user_responses = {
            i: {"selected": "", "status": "unvisited"}
            for i in range(len(self.questions))
        }
        self.current_idx = 0
        self.time_left = TOTAL_TEST_TIME
        self.show_page("TestPage")

    def end_exam(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.show_page("ScorecardPage")


# -----------------------------
# PAGE 1: WELCOME & USER PROFILE
# -----------------------------
class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = tk.Frame(self, bg=COLOR_CARD, bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=550, height=520)

        tk.Label(
            card,
            text="⚡ CYBER-TEST PORTAL ⚡",
            font=("Consolas", 18, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_CARD,
        ).pack(pady=20)

        tk.Label(
            card,
            text="Candidate Identification & Setup",
            font=("Segoe UI", 11),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
        ).pack(pady=5)

        # Input Form
        form_frame = tk.Frame(card, bg=COLOR_CARD)
        form_frame.pack(pady=20, padx=40, fill="x")

        tk.Label(
            form_frame,
            text="Candidate Name:",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
        ).grid(row=0, column=0, sticky="w", pady=10)
        tk.Entry(
            form_frame,
            textvariable=controller.user_name,
            font=("Segoe UI", 10),
            bg="#24283b",
            fg="white",
            insertbackground="white",
            bd=0,
        ).grid(row=0, column=1, sticky="ew", pady=10, padx=10)

        tk.Label(
            form_frame,
            text="Registration No / Roll:",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
        ).grid(row=1, column=0, sticky="w", pady=10)
        tk.Entry(
            form_frame,
            textvariable=controller.user_roll,
            font=("Segoe UI", 10),
            bg="#24283b",
            fg="white",
            insertbackground="white",
            bd=0,
        ).grid(row=1, column=1, sticky="ew", pady=10, padx=10)

        tk.Label(
            form_frame,
            text="Specialization Domain:",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
        ).grid(row=2, column=0, sticky="w", pady=10)

        domains = [
            "Software Engineering",
            "DevOps & Cloud",
            "Cyber Security",
            "AI & Data Engineering",
        ]
        domain_menu = tk.OptionMenu(
            form_frame, controller.user_domain, *domains
        )
        domain_menu.config(
            bg="#24283b",
            fg=COLOR_TEXT,
            activebackground=COLOR_CARD,
            bd=0,
            highlightthickness=0,
        )
        domain_menu.grid(row=2, column=1, sticky="ew", pady=10, padx=10)

        form_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            card,
            text="PROCEED TO INSTRUCTIONS ➔",
            command=self.validate_and_proceed,
            font=("Consolas", 11, "bold"),
            bg=COLOR_PRIMARY,
            fg="#15161e",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(pady=25)

    def validate_and_proceed(self):
        if (
            not self.controller.user_name.get().strip()
            or not self.controller.user_roll.get().strip()
        ):
            messagebox.showwarning(
                "Input Missing", "Please enter Candidate Name and Roll Number."
            )
            return
        self.controller.show_page("InstructionsPage")


# -----------------------------
# PAGE 2: INSTRUCTIONS DASHBOARD
# -----------------------------
class InstructionsPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = tk.Frame(self, bg=COLOR_CARD, bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=620, height=550)

        tk.Label(
            card,
            text="EXAM PROTOCOLS & GUIDELINES",
            font=("Consolas", 16, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_CARD,
        ).pack(pady=15)

        rules_text = (
            "1. TEST STRUCTURE:\n"
            "   • Total Questions: 10 Advanced Technical MCQs.\n"
            "   • Time Limit: 05:00 Minutes (300 Seconds).\n\n"
            "2. MARKING SCHEME:\n"
            "   • Correct Answer: +1 Point.\n"
            "   • Incorrect / Unanswered: 0 Points (No Negative Marking).\n\n"
            "3. EVALUATION BEHAVIOR:\n"
            "   • NO immediate feedback will be provided during the live test.\n"
            "   • Answers will NOT show green/red colors or validation status.\n"
            "   • You can modify your answers anytime before final submission.\n\n"
            "4. NAVIGATION:\n"
            "   • Use the Question Palette on the right panel to jump across questions.\n"
            "   • Click 'Mark for Review' if you wish to revisit a question later."
        )

        txt_box = tk.Text(
            card,
            font=("Segoe UI", 9),
            bg="#24283b",
            fg=COLOR_TEXT,
            bd=0,
            wrap="word",
            padx=15,
            pady=15,
        )
        txt_box.insert("1.0", rules_text)
        txt_box.config(state="disabled")
        txt_box.pack(padx=25, pady=10, fill="both", expand=True)

        btn_bar = tk.Frame(card, bg=COLOR_CARD)
        btn_bar.pack(pady=15)

        tk.Button(
            btn_bar,
            text="⬅ BACK",
            command=lambda: controller.show_page("WelcomePage"),
            font=("Consolas", 10, "bold"),
            bg=COLOR_MUTED,
            fg="white",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="left", padx=10)

        tk.Button(
            btn_bar,
            text="START ASSESSMENT ⚡",
            command=controller.start_exam,
            font=("Consolas", 10, "bold"),
            bg=COLOR_SUCCESS,
            fg="#15161e",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="left", padx=10)


# -----------------------------
# PAGE 3: LIVE ASSESSMENT INTERFACE
# -----------------------------
class TestPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # Layout Split: Main Question Area (Left) + Palette (Right)
        self.left_panel = tk.Frame(self, bg=COLOR_CARD, bd=1, relief="solid")
        self.left_panel.place(x=20, y=20, width=560, height=630)

        self.right_panel = tk.Frame(self, bg=COLOR_CARD, bd=1, relief="solid")
        self.right_panel.place(x=600, y=20, width=230, height=630)

        # --- Left Panel Components ---
        self.header_frame = tk.Frame(self.left_panel, bg=COLOR_CARD)
        self.header_frame.pack(fill="x", padx=15, pady=10)

        self.badge_lbl = tk.Label(
            self.header_frame,
            text="[DOMAIN]",
            font=("Consolas", 9, "bold"),
            bg=COLOR_PRIMARY,
            fg="#15161e",
            padx=6,
            pady=2,
        )
        self.badge_lbl.pack(side="left")

        self.timer_lbl = tk.Label(
            self.header_frame,
            text="⏱ Time Left: 05:00",
            font=("Consolas", 11, "bold"),
            fg=COLOR_WARNING,
            bg=COLOR_CARD,
        )
        self.timer_lbl.pack(side="right")

        self.question_lbl = tk.Label(
            self.left_panel,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_CARD,
            wraplength=520,
            justify="left",
        )
        self.question_lbl.pack(anchor="w", padx=20, pady=15)

        self.opt_var = tk.StringVar(value="")
        self.opt_buttons = []

        for _ in range(4):
            rb = tk.Radiobutton(
                self.left_panel,
                text="",
                variable=self.opt_var,
                value="",
                font=("Segoe UI", 10),
                fg=COLOR_TEXT,
                bg=COLOR_CARD,
                activebackground=COLOR_CARD,
                activeforeground=COLOR_ACCENT,
                selectcolor="#24283b",
                anchor="w",
                cursor="hand2",
                wraplength=480,
                justify="left",
                command=self.on_option_selected,
            )
            rb.pack(fill="x", padx=30, pady=8)
            self.opt_buttons.append(rb)

        self.act_frame = tk.Frame(self.left_panel, bg=COLOR_CARD)
        self.act_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        tk.Button(
            self.act_frame,
            text="Mark for Review",
            command=self.mark_review,
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_WARNING,
            fg="#15161e",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            self.act_frame,
            text="Clear Selection",
            command=self.clear_selection,
            font=("Segoe UI", 9),
            bg=COLOR_MUTED,
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
        ).pack(side="left", padx=10)

        self.next_btn = tk.Button(
            self.act_frame,
            text="Save & Next ➔",
            command=self.next_question,
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT,
            fg="#15161e",
            bd=0,
            padx=12,
            pady=5,
            cursor="hand2",
        )
        self.next_btn.pack(side="right")

        self.prev_btn = tk.Button(
            self.act_frame,
            text="⬅ Previous",
            command=self.prev_question,
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_MUTED,
            fg="white",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
        )
        self.prev_btn.pack(side="right", padx=5)

        # --- Right Panel (Question Palette) ---
        tk.Label(
            self.right_panel,
            text="QUESTION PALETTE",
            font=("Consolas", 10, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_CARD,
        ).pack(pady=10)

        self.palette_grid = tk.Frame(self.right_panel, bg=COLOR_CARD)
        self.palette_grid.pack(pady=10, padx=10)

        self.palette_btns = []
        for i in range(10):
            r, c = divmod(i, 3)
            btn = tk.Button(
                self.palette_grid,
                text=str(i + 1),
                width=4,
                height=2,
                font=("Consolas", 9, "bold"),
                bg="#24283b",
                fg="white",
                bd=0,
                command=lambda idx=i: self.jump_to_question(idx),
            )
            btn.grid(row=r, column=c, padx=5, pady=5)
            self.palette_btns.append(btn)

        tk.Button(
            self.right_panel,
            text="SUBMIT TEST 🏁",
            command=self.confirm_finish,
            font=("Consolas", 10, "bold"),
            bg=COLOR_ERROR,
            fg="white",
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
        ).pack(side="bottom", pady=20, fill="x", padx=15)

    def on_show(self):
        self.run_timer()
        self.render_current_question()

    def run_timer(self):
        mins, secs = divmod(self.controller.time_left, 60)
        self.timer_lbl.config(text=f"⏱ Time Left: {mins:02d}:{secs:02d}")

        if self.controller.time_left > 0:
            self.controller.time_left -= 1
            self.controller.timer_job = self.after(1000, self.run_timer)
        else:
            messagebox.showinfo(
                "Time Expired", "Test time is over! Submitting automatically."
            )
            self.controller.end_exam()

    def render_current_question(self):
        idx = self.controller.current_idx
        q = self.controller.questions[idx]

        self.badge_lbl.config(text=f"[{q['category']}]")
        self.question_lbl.config(
            text=f"Question {idx + 1} of {len(self.controller.questions)}:\n{q['question']}"
        )

        saved_resp = self.controller.user_responses[idx]["selected"]
        self.opt_var.set(saved_resp)

        for i, opt in enumerate(q["options"]):
            self.opt_buttons[i].config(text=f" {opt}", value=opt)

        self.update_palette_colors()

    def on_option_selected(self):
        idx = self.controller.current_idx
        self.controller.user_responses[idx]["selected"] = self.opt_var.get()
        if self.controller.user_responses[idx]["status"] != "review":
            self.controller.user_responses[idx]["status"] = "answered"
        self.update_palette_colors()

    def clear_selection(self):
        idx = self.controller.current_idx
        self.opt_var.set("")
        self.controller.user_responses[idx]["selected"] = ""
        self.controller.user_responses[idx]["status"] = "unvisited"
        self.update_palette_colors()

    def mark_review(self):
        idx = self.controller.current_idx
        self.controller.user_responses[idx]["status"] = "review"
        self.update_palette_colors()

    def update_palette_colors(self):
        for i in range(len(self.controller.questions)):
            status = self.controller.user_responses[i]["status"]
            btn = self.palette_btns[i]

            if i == self.controller.current_idx:
                btn.config(bd=2, relief="solid")
            else:
                btn.config(bd=0, relief="flat")

            if status == "answered":
                btn.config(bg=COLOR_SUCCESS, fg="#15161e")
            elif status == "review":
                btn.config(bg=COLOR_WARNING, fg="#15161e")
            else:
                btn.config(bg="#24283b", fg="white")

    def jump_to_question(self, idx):
        self.controller.current_idx = idx
        self.render_current_question()

    def next_question(self):
        if self.controller.current_idx < len(self.controller.questions) - 1:
            self.controller.current_idx += 1
            self.render_current_question()

    def prev_question(self):
        if self.controller.current_idx > 0:
            self.controller.current_idx -= 1
            self.render_current_question()

    def confirm_finish(self):
        if messagebox.askyesno(
            "Confirm Final Submission", "Are you sure you want to end the test?"
        ):
            self.controller.end_exam()


# -----------------------------
# PAGE 4: DETAILED SCORECARD & AUDIT
# -----------------------------
class ScorecardPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.card = tk.Frame(self, bg=COLOR_CARD, bd=1, relief="solid")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=720, height=620)

    def on_show(self):
        for child in self.card.winfo_children():
            child.destroy()

        score = 0
        attempted = 0
        total = len(self.controller.questions)

        for i, q in enumerate(self.controller.questions):
            user_ans = self.controller.user_responses[i]["selected"]
            if user_ans:
                attempted += 1
                if user_ans == q["answer"]:
                    score += 1

        pct = (score / total) * 100

        if pct == 100:
            rank = "CYBER ARCHITECT ⚡ (GRADE S)"
        elif pct >= 80:
            rank = "SENIOR ENGINEER 💻 (GRADE A)"
        elif pct >= 50:
            rank = "ASSOCIATE DEVELOPER 🛠 (GRADE B)"
        else:
            rank = "TRAINEE / NOVICE 🐒 (GRADE C)"

        header_text = (
            f"Candidate: {self.controller.user_name.get()} | Roll: {self.controller.user_roll.get()}\n"
            f"Domain: {self.controller.user_domain.get()}\n"
            f"Score: {score}/{total} ({pct:.0f}%) | Attempted: {attempted}/{total} | Rank: {rank}"
        )

        tk.Label(
            self.card,
            text="PERFORMANCE AUDIT REPORT",
            font=("Consolas", 15, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_CARD,
        ).pack(pady=10)

        tk.Label(
            self.card,
            text=header_text,
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT,
            bg="#24283b",
            padx=15,
            pady=8,
            justify="center",
        ).pack(padx=20, pady=5, fill="x")

        txt = scrolledtext.ScrolledText(
            self.card,
            font=("Consolas", 9),
            bg="#0f1016",
            fg=COLOR_TEXT,
            bd=0,
            wrap="word",
        )
        txt.pack(padx=20, pady=10, fill="both", expand=True)

        for i, q in enumerate(self.controller.questions, start=1):
            user_ans = (
                self.controller.user_responses[i - 1]["selected"] or "Not Answered"
            )
            is_correct = user_ans == q["answer"]
            mark = "✓" if is_correct else "✗"

            detail = (
                f"[{mark}] Q{i} [{q['category']}]: {q['question']}\n"
                f"    Your Answer : {user_ans}\n"
                f"    Correct Ans : {q['answer']}\n"
                f"    💡 Reason   : {q['explanation']}\n"
                f"------------------------------------------------------------------------\n"
            )
            txt.insert(tk.END, detail)

        txt.config(state="disabled")

        btn_bar = tk.Frame(self.card, bg=COLOR_CARD)
        btn_bar.pack(pady=10)

        tk.Button(
            btn_bar,
            text="NEW ASSESSMENT 🔄",
            command=lambda: self.controller.show_page("WelcomePage"),
            font=("Consolas", 10, "bold"),
            bg=COLOR_SUCCESS,
            fg="#15161e",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="left", padx=10)

        tk.Button(
            btn_bar,
            text="EXIT SYSTEM",
            command=self.controller.root.destroy,
            font=("Consolas", 10, "bold"),
            bg=COLOR_ERROR,
            fg="white",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side="left", padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MajorQuizEngineApp(root)
    root.mainloop()