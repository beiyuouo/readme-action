FROM python:3.8-slim

# Install dependencies.
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copy code.
ADD main.py /main.py
ADD social.py /social.py

CMD ["python", "/main.py"]
