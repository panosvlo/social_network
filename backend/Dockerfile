FROM python:3.9.10

RUN mkdir /src
WORKDIR /src
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD ./ /src/
CMD python manage.py runserver