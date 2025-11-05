class DataManager:
    def process_and_save_user(self, user_data):
        """
        Processes and saves user data, but also does validation and logging.
        """
        # (Justice) - Validation
        if not user_data.get("name"):
            print("Error: User name is missing.")
            return None

        # (Power) - Core data processing and saving
        user_data["status"] = "processed"
        print(f"Saving user: {user_data['name']}")
        # self.db.save(user_data)

        # (Wisdom) - Logging
        with open("activity.log", "a") as f:
            f.write(f"Processed user {user_data['name']}\n")

        # (Love) - Communication
        # self.email_client.send_confirmation(user_data['email'])
        print("Sent confirmation to user.")

        return user_data
