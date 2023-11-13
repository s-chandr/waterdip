# Flask Task Manager API

## Requirements
- Python
- Flask
- MongoDB

## Installation
1. Clone the repository
2. Set MongoDB URI in `app.py`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Run the server: `python app.py`
2. Endpoints:
   - Create a task: `POST /v1/tasks`
   - List tasks: `GET /v1/tasks`
   - Get a task: `GET /v1/tasks/{id}`
   - Delete a task: `DELETE /v1/tasks/{id}`
   - Edit a task: `PUT /v1/tasks/{id}`
   - Bulk add tasks: `POST /v1/tasks/bulk`
   - Bulk delete tasks: `DELETE /v1/tasks/bulk`

## Testing
Run tests with `pytest test_endpoints.py`

## Contributing
Feel free to contribute! Fork the repo and submit a pull request.

## License
This project is licensed under the MIT License.
