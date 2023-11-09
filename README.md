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

```bash
pip install requests
