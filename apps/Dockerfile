# setting up base image
FROM python:3.12-alpine

# prevents python buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# sets up the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions
WORKDIR /app

# copies files and directories from current directory to WORKDIR
COPY . .

# install system dependencies
RUN pip3 install -r requirements.txt --no-cache-dir

# Expose the port your app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
