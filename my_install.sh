pyenv local 3.11
poetry init --python "^3.11" -n
poetry env use $(pyenv which python)

echo '''version: "3"

tasks:
  default:
    - task: help

  help:
    desc: "List all tasks"
    silent: true
    cmds:
      - task --list-all

  generate-pre-commit-config:
    desc: "Generate .pre-commit-config.yaml file from .pre-commit-config.yaml.template"
    silent: true
    preconditions:
      - test -f .pre-commit-config.yaml.template
    generates:
      - .pre-commit-config.yaml
    env:
      PRE_COMMIT_ADDITIONAL_DEPENDENCIES:
        sh: echo "$(poetry export --with dev --without-hashes | while read line; do echo "          - $(echo ${line} | sed "s/^[[:space:]]*//")"; done)"
    cmds:
      - envsubst < .pre-commit-config.yaml.template > .pre-commit-config.yaml
      - echo "The .pre-commit-config.yaml file has been generated."

  install-pre-commit-config:
    desc: "Install pre-commit with generated .pre-commit-config.yaml"
    cmds:
      - pre-commit install
      - poetry update
      - task generate-pre-commit-config
      - pre-commit autoupdate
      - echo "The pre-commit installed and updated."

  update-pre-commit-config:
    desc: "Update versions .pre-commit-config.yaml and poetry update"
    cmds:
      - poetry update
      - task generate-pre-commit-config
      - pre-commit autoupdate
      - echo "The pre-commit updated."

  lint:
    desc: "Run pre-commit run --all-files"
    preconditions:
      - test -f .pre-commit-config.yaml
    cmds:
      - pre-commit run --all-files

  run-local-test-bot:
    desc: Run telegram bot locally
    cmds:
      - python -m src

  build-version:
    desc: "Generate version. Example for generate production version: task build-version -- -p"
    env:
      APP_VERSION:
        sh: python -m src.config.builder {{.CLI_ARGS}}
      APP_NAME:
        sh: python -m src.config.get_name
    cmds:
      - sed -i '.bak' -e "s/^APP_VERSION=.*/APP_VERSION=${APP_VERSION}/; s/^APP_NAME=.*/APP_NAME=${APP_NAME}/" build_version
      - echo "build version set up APP_VERSION=${APP_VERSION} APP_NAME=${APP_NAME}"

  build-docker-bot-without-run:
    desc: "Build docker container telegram bot Example: task build-docker-bot-without-run -- '-p'"
    cmds:
      - task build-version -- {{.CLI_ARGS}}
      - docker compose -f docker-compose-dev.yaml --env-file build_version create --build

  push-docker-container:
    desc: "Push docker container to docker hub"
    cmds:
      - docker image push --all-tags zimkaa/sales_bot

  run-docker-bot:
    desc: Run docker container telegram bot
    cmds:
      - docker compose -f docker-compose-dev.yaml --env-file .dev.env up -d

  stop-docker-bot:
    desc: Stop docker container telegram bot
    cmds:
      - docker compose -f docker-compose-dev.yaml down

  # test:
  #   desc: Run tests
  #   cmds:
  #     - python -m coverage run
  #     - python -m coverage report -m
  #     - python -m coverage html

  file-id-bot:
    desc: Run file_id sender locally
    cmds:
      - python ./get_file_id_for_bot.py

  user-id-bot:
    desc: Run user id sender locally
    cmds:
      - python ./get_user_id.py

  test-deploy:
    desc: Action test locally
    cmds:
      # - act -j 'docker-build-push' --container-architecture linux/amd64 --var-file .vars --secret-file .secrets -e event.json
      - act --container-architecture linux/amd64 --var-file .vars --secret-file .secrets -e event.json

  run-build-container:
    desc: Run locally container
    dotenv: ['build_version']
    cmds:
      - docker run --platform linux/amd64 --env-file .dev.env --name "${APP_NAME}-${APP_VERSION}" -d "zimkaa/${APP_NAME}:${APP_VERSION}"
''' >> Taskfile.yml

echo '''## folders
.venv/
.env/
__pycache__/
.pytest_cache/
.mypy_cache/

## files
*.pyc
*.log
*.log.zip
.python-version
.pre-commit-config.yaml

# dotenv
.env
.dev.env
.secrets
.vars
''' | tee .gitignore .dockerignore

echo '''###########
# BUILDER #
###########
FROM python:3.10 as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev

RUN pip install --no-cache-dir --upgrade -r requirements.txt

###########
## IMAGE ##
###########
FROM python:3.10-slim

WORKDIR /home/appuser/app

COPY . /home/appuser/app

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN chown -R appuser:appgroup /home/appuser/app

USER appuser

ENTRYPOINT ["./entrypoint.sh"]
'''  >> Dockerfile

echo '''[tool.pytest.ini_options]
addopts = "-vvv"
cache_dir = "/tmp/pytest_cache"
testpaths = [
    "tests",
]

[tool.ruff]
cache-dir = "/tmp/ruff_cache"
fix = true
line-length = 120
unsafe-fixes = true
exclude = [
    "alembic/",
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
]

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D1",  # docstring
    "D203",  # docstring
    "D213",  # docstring
    "S101",  # use of assert
    "ANN101",  # self annotation
    "TRY401",  # exeption logging
    # "FA102",  # from __future__ import annotations
    # projec specific
    "TD002",
    "TD003",
    "FIX002",
]
exclude = [
    "get_file_id_for_bot.py",
    "src/telegram/templates/text.py",
    "src/telegram/base/custom_filters/callback_filter.py"
]

[tool.ruff.lint.isort]
no-lines-before = ["standard-library", "local-folder"]
known-third-party = []
known-local-folder = ["whole_app"]
lines-after-imports = 2
force-single-line = true

[tool.ruff.lint.extend-per-file-ignores]
"tests/*.py" = ["ANN101", "S101", "S311"]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.11"
cache_dir = "/tmp/mypy_cache"
ignore_missing_imports = true
strict = false
exclude = ["~/.pyenv/*", ".venv/", "alembic/"]

[tool.pyright]
ignore = ["server"]
''' >> pyproject.toml

echo '''default_language_version:
  python: python3.11

repos:
  - repo: https://github.com/floatingpurr/sync_with_poetry
    rev: "1.1.0"
    hooks:
      - id: sync_with_poetry

  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: "v1.3.1"
    hooks:
      - id: python-safety-dependencies-check
        files: pyproject.toml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [ --fix, --exit-non-zero-on-fix ]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
        exclude: src/fight/example
        exclude_types:
          - markdown
      - id: check-added-large-files
        args:
          - "--maxkb=1024"
      - id: check-yaml
        exclude: \.gitlab-ci.yml
      - id: check-ast
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-symlinks
      - id: check-toml
      - id: debug-statements
      - id: end-of-file-fixer

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: "v1.8.0"
    hooks:
      - id: mypy
        args:
          - "--config-file=pyproject.toml"
          - "--install-types"
          - "--non-interactive"
        exclude: "alembic/"
        additional_dependencies:
$PRE_COMMIT_ADDITIONAL_DEPENDENCIES
''' >> .pre-commit-config.yaml.template

echo '''{
  "act": true
}
''' >> event.json

git init
git add .
git commit -m "initial"

touch start.py README.md example.env .env .dev.env .vars .secrets
