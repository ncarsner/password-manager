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
│   └── tests
│       ├── test_api.py           # Unit tests for API endpoints
│       └── test_units.py         # Unit tests for services and utilities
├── frontend
│   ├── src
│   │   ├── index.html            # Main HTML file for the frontend
│   │   ├── main.js               # Main JavaScript logic
│   │   └── styles.css            # CSS styles
│   ├── components
│   │   └── vault-view.js         # Component for managing the password vault
│   └── tests
│       └── test_ui.test.jsx      # Unit tests for frontend components
├── scripts
│   └── init_db.sh                # Script for initializing the database
├── .env.sample                    # Sample environment configuration
├── pyproject.toml                 # Project metadata and dependencies
├── uv.lock                        # Locked dependency versions
├── LICENSE                        # Licensing information
└── README.md                     # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd password-manager
   ```

2. Install `uv` if you haven't already:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies and create the virtual environment:
   ```
   uv sync
   ```

4. Configure environment variables:
   ```
   cp .env.sample .env
   ```
   Edit `.env` and set `SECRET_KEY` and `ENCRYPTION_KEY` to secure random values before running in production.
   `DATABASE_PATH` defaults to `database.db` in the project root.

5. Set up the frontend:
   - Open `frontend/src/index.html` in a web browser to view the application.

## Usage

Start the backend server:
```
uv run flask --app backend.src.app run
```

The API will be available at `http://localhost:5000`. Access the frontend by opening `frontend/src/index.html` in a web browser.

### Running tests

```
uv run python3 -m pytest
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
