Advent of Code 
==============

This repository contains my solutions to Advent of Code 2020

# Usage

## Installation

```
pip install git+https://github.com/d1618033/aoc.git
```

## Running

To run the solution for a particular day:

```
aoc solve <day_number> --input <your_file>
```

## Development

To make new files, and download data for the new day:

```
aoc new [--day <day>] [--session <session>]
```

The session is the session cookie - you can find it by going to the website and looking at the network tab.

You can also save your session cookies in a config file called `~/.aoc`:

```json
{
  "session": "<your cookie>"
}
```

To remove a day:

```
aoc rm [--day <day>]
```

Just to download the input data:

```
aoc download [--day <day>] [--session <session>]
```
