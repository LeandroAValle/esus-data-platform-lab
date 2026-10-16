FROM python:3.11-slim

COPY docker/streamlit/requirements-streamlit.txt /requirements-streamlit.txt
RUN pip install --no-cache-dir -r /requirements-streamlit.txt

WORKDIR /app
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["src/dashboard/app.py", "--server.address=0.0.0.0"]
