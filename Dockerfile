# 1. Use an official Python runtime as a parent image
# We use python 3.10 because your pycache files show cpython-310
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
# This uses your existing requirements.txt file
COPY requirements.txt .

# 4. Install the required packages
# This installs openai, tqdm, python-dotenv, pyyaml, etc.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Set environment variable to ensure logs show up immediately
ENV PYTHONUNBUFFERED=1

# 7. Define the command to run your app
CMD ["python", "main.py"]