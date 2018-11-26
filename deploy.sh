#!/usr/bin/env bash
git add -f .secrets/
eb deploy --profile eb --staged
git reset HEAD .secrets/