# Password Manager

This project is a password manager application that provides a secure way to store and manage passwords. It consists of a Python backend and a small-footprint UX frontend.

## Project Structure

```
password-manager
├── backend
│   ├── src
│   │   ├── app.py                # Entry point for the backend application
│   │   ├── api
│   │   │   ├── __init__.py       # Initializes the API module
│   │   │   └── v1.py             # API endpoints for version 1
│   │   ├── models
│   │   │   └── vault.py          # Vault model class
│   │   ├── services
│   │   │   ├── crypto.py         # Cryptographic functions
│   │   │   └── storage.py        # Storage operations
│   │   ├── utils
│   │   │   └── helpers.py        # Utility functions
│   │   └── config.py             # Configuration settings
│   ├── tests
│   │   └── test_api.py           # Unit tests for API endpoints
│   ├── requirements.txt           # Python dependencies
│   └── pyproject.toml             # Project metadata and dependencies
├── frontend
│   ├── src
│   │   ├── index.html            # Main HTML file for the frontend
│   │   ├── main.js               # Main JavaScript logic
│   │   └── styles.css            # CSS styles
│   ├── components
│   │   └── vault-view.js         # Component for managing the password vault
│   └── tests
│       └── test_ui.py            # Unit tests for frontend components
├── scripts
│   └── init_db.sh                # Script for initializing the database
├── .env.sample                    # Sample environment configuration
├── LICENSE                        # Licensing information
└── README.md                     # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd password-manager
   ```

2. Set up the backend:
   - Install `uv` if you haven't already:
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - Install the required Python packages and set up the virtual environment:
     ```
     uv sync
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Open `index.html` in a web browser to view the application.

## Usage

- Start the backend server by running:
  ```
  python src/app.py
  ```

- Access the frontend by opening `index.html` in a web browser.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.