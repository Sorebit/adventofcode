#!/usr/bin/env bash

set -e

d="day${1}"
if [ -d $d ]; then
  echo "${d} already exists"
  exit 1
fi

mkdir -p $d
cp template.go "${d}/${d}.go"
cd $d/
touch example.in
touch problem.in
go mod init "aoc2024/${1}"
go mod edit -replace helpers/aoc=../aoc
go mod tidy
