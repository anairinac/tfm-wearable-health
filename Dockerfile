FROM public.ecr.aws/lambda/python:3.12
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
COPY requirements-lambda.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt
COPY scripts/data_cleanup.py scripts/risk_scoring.py ${LAMBDA_TASK_ROOT}/
COPY scripts/models/ ${LAMBDA_TASK_ROOT}/models/
COPY scripts/lambda_function.py ${LAMBDA_TASK_ROOT}/
CMD ["lambda_function.handler"]