#!/usr/bin/env bash
git add -f .secrets/ .media/
eb deploy --profile eb --staged
git reset HEAD .secrets/ .media/