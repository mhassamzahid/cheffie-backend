docker run --rm -v "D:\Repositories\cheffie-backend:/var/task" --entrypoint /bin/sh public.ecr.aws/lambda/python:3.12 -c "pip install -r requirements.txt -t package/"
