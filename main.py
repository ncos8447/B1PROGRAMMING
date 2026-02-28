#user authentification
import logging

logging.basicConfig(level=logging.INFO)

class User:
    MAX_FAILED_ATTEMPTS = 3

    def __init__(self, username, password, privilege="user"):
        self.set_username(username)
        self.__password_hash = self.hash_password(password)
        self.set_privilege(privilege)
        self.__failed_attempts = 0
        self.__is_locked = False

    def hash_password(self, password):
        return f"hashed_{password}"

    def set_username(self, username):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        self.username = username

    def get_username(self):
        return self.username

    # privilege setter
    def set_privilege(self, privilege):
        allowed_roles = ["user", "admin"]
        if privilege not in allowed_roles:
            raise ValueError("Invalid privilege level.")
        self.privilege = privilege

    def get_privilege(self):
        return self.privilege

    # authenticate user
    def authenticate(self, password):
        if self.__is_locked:
            logging.warning(f"Locked account login attempt: {self.username}")
            return False

        if self.__password_hash == self.hash_password(password):
            self.__failed_attempts = 0
            logging.info(f"Successful login: {self.username}")
            return True
        else:
            self.__failed_attempts += 1
            logging.warning(f"Failed login attempt {self.__failed_attempts} for {self.username}")

            if self.__failed_attempts >= User.MAX_FAILED_ATTEMPTS:
                self.__is_locked = True
                logging.critical(f"Account locked: {self.username}")

            return False

    # safe user info display
    def display_info(self):
        return {
            "username": self.username,
            "privilege": self.privilege,
            "account_locked": self.__is_locked
        }

    # prevent direct password access
    @property
    def password(self):
        raise AttributeError("Password is private and cannot be accessed directly.")

    # unlock account
    def unlock_account(self, admin_user):
        if admin_user.get_privilege() == "admin":
            self.__failed_attempts = 0
            self.__is_locked = False
            logging.info(f"Account unlocked by admin: {admin_user.get_username()}")
        else:
            logging.warning(f"Unauthorized unlock attempt by: {admin_user.get_username()}")
            raise PermissionError("Only admin users can unlock accounts.")


# demo section
if __name__ == "__main__":

    # create users
    admin = User("adminUser", "AdminPass123", "admin")
    user1 = User("johnDoe", "UserPass123", "user")

    print("=== authentication demo ===")

    # correct login
    print("correct password:", user1.authenticate("UserPass123"))

    # incorrect login attempts
    print("wrong password:", user1.authenticate("wrong1"))
    print("wrong password:", user1.authenticate("wrong2"))
    print("wrong password (locks account):", user1.authenticate("wrong3"))

    # attempt login after lock
    print("attempt after lock:", user1.authenticate("UserPass123"))

    # unlock account
    admin.authenticate("AdminPass123")
    user1.unlock_account(admin)

    print("login after unlock:", user1.authenticate("UserPass123"))

    # safe display
    print("safe user info:", user1.display_info())

    # attempt privilege escalation
    try:
        user1.set_privilege("admin")
    except ValueError as e:
        print("privilege escalation prevented:", e)