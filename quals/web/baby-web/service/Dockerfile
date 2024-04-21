FROM ubuntu:latest
# Add Env Args for tzdata package
ARG DEBIAN_FRONTEND=noninteractive

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy files
COPY . .

# Install requirements
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

CMD ["gunicorn", "-w", "8", "--bind", "0.0.0.0:5000", "--log-level", "debug", "app:app"]
