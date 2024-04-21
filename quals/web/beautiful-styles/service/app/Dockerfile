FROM python:3.8-slim
# Copy files
COPY . .

# Install requirements
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

RUN mkdir uploads

CMD ["gunicorn", "-w", "8", "--bind", "0.0.0.0:5000", "--log-level", "debug", "app:app"]
