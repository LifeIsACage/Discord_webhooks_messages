import customtkinter
import requests
from json import dumps
from tkinter import messagebox

class WebhookApp:
    def __init__(self):
        self.webhook_name = ""
        self.webhook_token = ""
        self.setup_login_gui()

    def setup_login_gui(self):
        # Set up the login GUI window
        get_webhook_win = customtkinter.CTk()
        get_webhook_win.geometry("400x200")
        get_webhook_win.title("Webhook Login")  # Set window title
        get_webhook_win.resizable(False, False)  # Disable window resizing

        get_input = customtkinter.CTkEntry(get_webhook_win, width=380, height=30)
        get_input.place(x=10, y=50)

        get_button = customtkinter.CTkButton(get_webhook_win, width=105, height=50, text="Login", font=('Bold', 18), command=self.on_login_clicked)
        get_button.place(x=145, y=115)

        self.get_webhook_win = get_webhook_win
        self.get_input = get_input

        get_webhook_win.mainloop()

    def on_login_clicked(self):
        # Handle login button click
        webhook_url = str(self.get_input.get())
        webhook_name, webhook_token = self.get_webhook_data(webhook_url)

        if webhook_name and webhook_token:
            self.webhook_name = webhook_name
            self.webhook_token = webhook_token
            self.get_webhook_win.destroy()

            # Create an instance of WebhookAppGUI and pass the necessary parameters
            webhook_app_gui = WebhookAppGUI(name=self.webhook_name, token=self.webhook_token, webhook_url=webhook_url)
            webhook_app_gui.create_webhook_app()
        else:
            messagebox.showwarning("WRONG WEBHOOK URL", "The entered URL is incorrect, please try again.")

    def get_webhook_data(self, webhook: str):
        # Fetch webhook data from the provided URL
        try:
            req = requests.get(url=webhook, headers={'Content-Type': 'application/json'})
            req.raise_for_status()  # Raise an HTTPError for bad responses

            hook_data = req.json()

            if req.status_code == 200 and hook_data.get('url') == webhook:
                return hook_data['name'], hook_data['token']
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Request Error", f"Failed to fetch webhook data: {error}")

        return None, None


class WebhookAppGUI:
    def __init__(self, name, token, webhook_url):
        self.name = name
        self.token = token
        self.webhook_url = webhook_url

    def create_webhook_app(self):
        # Set up the main webhook app GUI window
        main_win = customtkinter.CTk()
        main_win.geometry("600x400")
        main_win.title("Webhook App")  # Set window title
        main_win.resizable(False, False)  # Disable window resizing

        show_hook_token = customtkinter.CTkLabel(main_win, text=f"Token: {self.token}", font=("bold", 14))
        show_hook_token.place(x=10, y=10)

        show_hook_name = customtkinter.CTkLabel(main_win, text=f"Name: {self.name}", font=("bold", 14))
        show_hook_name.place(x=10, y=40)

        message_history = customtkinter.CTkTextbox(main_win, height=200, width=560)
        message_history.place(x=20, y=80)
        message_history.configure(state='disable')

        message = customtkinter.CTkEntry(main_win, width=560, height=30)
        message.place(y=300, x=20)

        send_btn = customtkinter.CTkButton(main_win, width=560, height=40, command=lambda: self.on_send_message(message, message_history), text="Send Message", font=('Bold', 16))
        send_btn.place(x=20, y=345)

        # Bind the <Return> event to the on_send_message function
        message.bind('<Return>', lambda event=None: self.on_send_message(message, message_history))

        main_win.mainloop()

    def on_send_message(self, message_entry, message_history):
        # Handle sending a message
        msg = str(message_entry.get())

        # Handle empty a message        
        if len(msg) < 1:    return
        
        self.send_message(msg)

        # Append the sent message to the message_history textbox
        message_history.configure(state='normal')
        message_history.insert('end', f"{self.name}: {msg}\n")
        message_history.configure(state='disable')

        message_entry.delete(0, 'end')  # Clear the content of the entry

    def send_message(self, msg):
        # Send a message to the webhook
        headers = {
            'Content-Type': 'application/json',
        }
        req = requests.post(url=self.webhook_url, headers=headers, data=dumps({'content': msg}))

if __name__ == "__main__":
    app = WebhookApp()
