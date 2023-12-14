import tkinter as tk
from tkinter import messagebox
import re

class Survey:
    def __init__(self, master):
        self.master = master
        self.master.title("Опросник")

        self.questions = []
        self.answers = []

        self.current_question = 0

        with open("questions.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                question, options = line.strip().split(":")
                self.questions.append((question, options.split("|")))

        self.entry_labels = [
            "Фамилия:", 
            "Имя:", 
            "Отчество:", 
            "Возраст:", 
            "Пол:", 
            "Электронная почта:", 
            "Номер телефона:"
        ]
        self.entries = []

        self.label = tk.Label(self.master, text="Введите свои данные:")
        self.label.pack(anchor=tk.W)

        self.entry_width = max(len(label_text) for label_text in self.entry_labels)

        for label_text in self.entry_labels:
            frame = tk.Frame(self.master)
            frame.pack(anchor=tk.W)
            label = tk.Label(frame, text=label_text)
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=self.entry_width)
            entry.pack(side=tk.RIGHT)
            self.entries.append(entry)

        self.button = tk.Button(self.master, text="Продолжить", command=self.start_survey)
        self.button.pack()

    def start_survey(self):
        for entry in self.entries:
            value = entry.get().strip()
            if not value:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            self.answers.append(value)
            entry.delete(0, tk.END)

        self.show_question()

    def show_question(self):
        self.label.config(text=self.questions[self.current_question][0])
        self.var_list = []
        for option in self.questions[self.current_question][1]:
            var = tk.IntVar()
            rb = tk.Radiobutton(self.master, text=option, variable=var, value=len(self.var_list))
            rb.pack(anchor=tk.W)
            self.var_list.append(var)

        self.button.configure(text="Далее", command=self.next_question)

    def next_question(self):
        selected_option = None
        for i, var in enumerate(self.var_list):
            if var.get() == 1:
                selected_option = self.questions[self.current_question][1][i]
                break
        if selected_option is None:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите вариант ответа.")
        else:
            self.answers.append(selected_option)
            self.current_question += 1
            for widget in self.master.pack_slaves()[1:]:
                widget.destroy()
            if self.current_question < len(self.questions):
                self.show_question()
            else:
                self.save_answers()

    def save_answers(self):
        # Возраст
        if int(self.answers[3]) < 6:
            messagebox.showerror("Ошибка", "Возраст не может быть меньше 6 лет.")
            return

        # Электронная почта
        email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
        if not email_pattern.match(self.answers[5]):
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректную электронную почту на английском языке.")
            return

        # Номер телефона
        if not self.answers[6].startswith("+7") or not self.answers[6][2:].isdigit():
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный номер телефона, начинающийся с '+7' и состоящий только из цифр.")
            return
        
        with open("survey_results.txt", "w", encoding="utf-8") as file:
            file.write("Данные пользователя:\n")
            file.write("Фамилия: {}\n".format(self.answers[0]))
            file.write("Имя: {}\n".format(self.answers[1]))
            file.write("Отчество: {}\n".format(self.answers[2]))
            file.write("Возраст: {}\n".format(self.answers[3]))
            file.write("Пол: {}\n".format(self.answers[4]))
            file.write("Электронная почта: {}\n".format(self.answers[5]))
            file.write("Номер телефона: {}\n".format(self.answers[6]))

            file.write("\nОтветы на вопросы:\n")
            for i in range(len(self.answers)-7):
                file.write("{}: {}\n".format(self.questions[i][0], self.answers[i+7]))

        messagebox.showinfo("Результаты", "Спасибо за участие в опросе!\n\nРезультаты сохранены в файле 'survey_results.txt'.")
        self.master.destroy()

root = tk.Tk()
survey = Survey(root)
root.mainloop()