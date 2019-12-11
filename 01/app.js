// https://adventofcode.com/2019/day/1

const fs = require('fs');
const path = require('path');
const filePath = path.join(__dirname, 'input.txt');

// Sum helper
const s = (a, c) => a + c;

// Rocket fuel equation
const c = (e) => Math.max(Math.floor(e / 3) - 2, 0);
// Fuel for fuel
const d = (e) => {
  let sum = 0;
  while (e > 0) {
    sum += c(e);
    e = c(e);
  }
  return sum;
};

fs.readFile(filePath, 'utf8', (err, contents) => {
  if (err) {
    console.error(err);
    return;
  }

  const data = contents.split('\n').map(l => Number(l));

  const part1 = data.map(e => c(e)).reduce(s);
  const part2 = data.map(e => d(e)).reduce(s);

  console.log('Advent of Code 2019 - Day 1');
  console.log('Part 1:', part1);
  console.log('Part 2:', part2);
});
