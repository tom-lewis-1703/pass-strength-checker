# Password Strength Checker

The Password Strength Checker is a Python application with a graphical user interface (GUI) built using Tkinter. It allows users to enter a password and assess its strength based on various security criteria such as length, use of numbers, use of upper and lowercase letters, inclusion of special characters, and checks against known compromised passwords.

## Features

- **Strength Assessment**: Evaluates password strength on a scale from "Very Weak" to "Very Strong".
- **Compromised Password Check**: Verifies if the password has appeared in known data breaches (requires internet connection).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system.
- `requests` library installed to check for compromised passwords using the "Have I Been Pwned" API.

You can install the required packages using `pip`:

`
pip install requests
`

## Running the Application
To run the Password Strength Checker, use the following command:
`
python password_strength_checker.py
`

Replace password_strength_checker.py with the path to the script file if you have placed it in a different directory.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments
* [Have I Been Pwned](https://haveibeenpwned.com/)
