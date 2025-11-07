# aws-controller
A AI based controller to manage AWS 



{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red214\green85\blue98;\red155\green162\blue177;}
{\*\expandedcolortbl;;\cssrgb\c87843\c42353\c45882;\cssrgb\c67059\c69804\c74902;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs26 \cf2 # aws-fastapi-starter\cf3 \
\
\cf2 ## Overview\cf3 \
Brief purpose, key features, and target SLOs.\
\
\cf2 ## Architecture\cf3 \
```mermaid\
flowchart LR\
  Client --> API[FastAPI]\
  API --> Auth[OIDC/JWT]\
  API --> DB[(Postgres)]\
  API --> Cache[(Redis)]\
  API --> MQ[(SQS/EventBridge)]\
  API --> Obs[OTel/CloudWatch]}
## Overview
Production-grade FastAPI microservice starter tailored for AWS (ECS/Fargate or Lambda via container), Python 3.13+, and modern security/observability defaults.

## Architecture
```mermaid
flowchart LR
  Client --> API[FastAPI]
  API --> Auth[OIDC/JWT]
  API --> DB[(Postgres/SQLite)]
  API --> Cache[(Redis optional)]
  API --> MQ[(SQS/EventBridge optional)]
  API --> Obs[OpenTelemetry/CloudWatch]
```

## Local Development
- Python 3.13 (or nearest available). Create venv and install deps with `make dev`.
- Copy `.env.example` to `.env` and adjust values.
- Run `make up` (optional Redis), then `make run` to start the API at http://127.0.0.1:8000
- OpenAPI docs: http://127.0.0.1:8000/docs and /redoc

## Deploy (AWS)
- Containerized app (Dockerfile) deployable to ECS/Fargate behind an ALB (Terraform scaffolding in `infra/terraform/`).
- Secrets via AWS Secrets Manager or SSM Parameter Store.
- Observability via CloudWatch logs + (optional) AWS Distro for OpenTelemetry.

## Security Checklist
See `SECURITY_CHECKLIST.md`.

## Make targets

```
{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 .AppleSystemUIFontMonospaced-Regular;}
{\colortbl;\red255\green255\blue255;\red155\green162\blue177;\red197\green136\blue83;}
{\*\expandedcolortbl;;\cssrgb\c67059\c69804\c74902;\cssrgb\c81961\c60392\c40000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs26 \cf2 ## Local Development\
- Python \cf3 3.13\cf2  (or nearest available), UV/venv, `make dev`\
- Env via `.env` (never commit secrets). Example vars in `.env.example`.\
\
## Run\
```bash\
make up        # start services\
make run       # uvicorn app.main:app --reload}
{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 make test\
make lint\
make typecheck}
```
## Troubleshooting
- Set `AUTH_DISABLED=true` in `.env` for local development to bypass JWT (never in prod).
- If SQLite is used, ensure the `data/` directory is writable.

## License
See `LICENSE`.
