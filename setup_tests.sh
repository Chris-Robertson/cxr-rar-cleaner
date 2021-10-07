#!/bin/zsh

rm -rf ./test

mkdir ./test ./test/subdir1 ./test/subdir2 ./test/subdir3 ./test/subdir4

touch ./test/subdir1/movie1.rar
touch ./test/subdir1/movie1.mkv

touch ./test/subdir2/movie2.rar

touch ./test/subdir3/movie3.mkv

touch ./test/subdir4/movie4.rar
touch ./test/subdir4/.unrar
