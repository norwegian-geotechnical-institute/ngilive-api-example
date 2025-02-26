# NGI Live API sample

## Requirements:

- Python

## Set up:

1. Create a virtual environment

   ```sh
   python -m venv .venv
   ```

2. Activate the python virtual environent

   linux/mac:

   ```sh
   source .venv/bin/activate
   ```

   windows:

   ```sh
   .venv\scripts\activate.ps1
   ```

3. Install dependencies from requirements file

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the template and fill the required variables in the .env

   Contact NGI to obtain a client id and secret if you don't have one.

   Linux/mac:

   ```sh
   cp .env.template .env
   ```

   Fill the required parameters, for example:

   ```
   KEYCLOAK_CLIENT_ID=your-client          # your client id
   KEYCLOAK_CLIENT_SECRET=abcsasdkjhadkjjd # your client secret
   PROJECT_ID=20241234                     # Project number
   ```

## Run the sample:

`python demo.py`
