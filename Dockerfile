FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
WORKDIR /app

# Copy requirements individually to allow for caching
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
RUN black /app --check # Confirm that the code is formatted correctly
RUN pytest -m unit /app # Ensure that unit tests are passing, ignoring integration tests

# Run the application
CMD ["sleep", "infinity"]