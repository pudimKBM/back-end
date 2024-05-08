# DESAFIO Hyperativa

This project is a [brief description of what the project does or its purpose].
- [@antoniovvl](https://www.linkedin.com/in/avvl/)
## Stack utilizada

- **Back-end:** Flask, pydantic,  SQLAlquemy
- **Database:** sqlite

## Cosiderations
- The sqlite makes it easier to create project and test fast so is the database tha we are using in the project today and it will be created in the start of the app in the backend folder
- The log file will be created in the backend folder and wil log the requests and the user that is making the requests if they are already logged in
- I also modified the example text file to take out the comments so use the DESAFIO-HYPERATIVA.txt since is the updated one
- the encription was kind of hard to decide soo i have 2 columns 1 encripted with a simple hash sha256 for the selects on the database and for the validation and retival of the cards and a simple Fernet (symmetric encryption) for the encryption of the cards aswell the keys are in the .env.dev file
- There is also a postman collection(v2.1) in the backend folder 

## Installation

### Prerequisites

Before you begin, make sure you have Conda installed on your system. If you don't have Conda installed, you can download it from [here](https://docs.conda.io/en/latest/miniconda.html).

### Setup

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/pudimKBM/back-end.git
    cd back-end/backend
    ```

2. Create a new Conda environment:

    ```bash
    conda create --name <env name> -c conda-forge python=3.11
    ```

3. Activate the Conda environment:

    ```bash
    conda activate <env name>
    ```

4. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Rund the following command in the command prompt

```bash
python main.py
```

## Api docs
# Authentication API

## Register Endpoint

### Method
- `POST`

### URL
- `/register`

### Description
- Registers a new user by providing their email and password.

### Request Body Parameters
- `mail` (string, required): User's email address.
- `password` (string, required): User's password.

### Responses
- `201 Created`: User registered successfully.
  - Response Body: `{ "message": "User registered successfully" }`
- `400 Bad Request`: Missing username or password or user already exists.
  - Response Body: `{ "message": "Missing username or password" }` or `{ "message": "User already exists" }`

## Login Endpoint

### Method
- `POST`

### URL
- `/login`

### Description
- Logs in a user by providing their email and password. It also updates the `date_modified` column in the database to record the last login date and time.

### Request Body Parameters
- `mail` (string, required): User's email address.
- `password` (string, required): User's password.

### Responses
- `200 OK`: Successful login.
  - Response Body: `{ "access_token": "<JWT access token>" }`
- `401 Unauthorized`: Invalid username or password.
  - Response Body: `{ "message": "Invalid username or password" }`


# Batch Upload API

## Upload Endpoint

### Method
- `POST`

### URL
- `/upload`

### Description
- Uploads a batch file containing card information. It processes the file, encrypts card numbers, and stores them in the database.

### Request Headers
- `Authorization` (string, required): JWT access token for authentication.

### Request Body Parameters
- `file` (file, required): Batch file containing card information.

### Responses
- `200 OK`: File processed successfully.
  - Response Body: `{ "message": "File processed successfully." }`
- `400 Bad Request`: No file part or no selected file or invalid file type.
  - Response Body: `{ "error": "No file part" }` or `{ "error": "No selected file" }` or `{ "error": "Invalid file type" }`
- `500 Internal Server Error`: Error occurred during file processing.
  - Response Body: `{ "error": "<error message>" }`


# Card Management API

## Insert Card Endpoint

### Method
- `POST`

### URL
- `/card`

### Description
- Inserts a new card into the database.

### Request Headers
- `Authorization` (string, required): JWT access token for authentication.

### Request Body Parameters
- `card_number` (string, required): Card number to be inserted.

### Responses
- `201 Created`: Card data inserted successfully.
  - Response Body: `{ "message": "Card data inserted successfully." }`
- `400 Bad Request`: Card number might already exist.
  - Response Body: `{ "error": "Card number might already exist." }`

## Get Card Endpoint

### Method
- `GET`

### URL
- `/card/<card_number>`

### Description
- Retrieves card information based on the card number.

### Request Headers
- `Authorization` (string, required): JWT access token for authentication.

### URL Parameters
- `card_number` (string, required): Card number to retrieve information for.

### Responses
- `200 OK`: Card information retrieved successfully.
  - Response Body:
    ```json
    {
        "card_number": "<decrypted_card_number>",
        "date_created": "<date_created>",
        "user_added": "<user_added>",
        "metadata": <metadata>
    }
    ```
- `404 Not Found`: Card number not found.
  - Response Body: `{ "error": "Card number not found." }`
