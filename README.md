#### Hexlet tests and linter status:
[![Actions Status](https://github.com/Dobrovera/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/Dobrovera/python-project-50/actions)
#### linter test
[![linter](https://github.com/Dobrovera/python-project-50/actions/workflows/make-lint.yml/badge.svg)](https://github.com/Dobrovera/python-project-50/actions/workflows/make-lint.yml)
#### Codeclimate
<a href="https://codeclimate.com/github/Dobrovera/python-project-50/maintainability"><img src="https://api.codeclimate.com/v1/badges/b781c7194aeb1bbbb189/maintainability" /></a>
#### Test Coverage
<a href="https://codeclimate.com/github/Dobrovera/python-project-50/test_coverage"><img src="https://api.codeclimate.com/v1/badges/b781c7194aeb1bbbb189/test_coverage" /></a>

### About this package
The program compares two configuration files. 

Available output formats:
* stylish - default
* plain
* json

### Install
```bash
git clone https://github.com/Dobrovera/python-project-50
cd python-project-50
make install
```

### Help information
Command ```gendiff -h ```

```bash
usage: gendiff [-h] [-f {stylish,plain}] first_file second_file

Compares two configuration files and shows a difference.

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f {stylish,plain}, --format {stylish,plain}
                        set format of output
```
### Comparing two json files
Command ```gendiff filepath1.json filepath2.json```

[![asciicast](https://asciinema.org/a/540252.svg)](https://asciinema.org/a/540252)


### Comparing two yaml files
Command ```gendiff filepath1.yaml filepath2.yaml```

[![asciicast](https://asciinema.org/a/540253.svg)](https://asciinema.org/a/540253)

### Comparing files with nested structures
Command ```gendiff filepath1.yaml filepath2.yaml``` //
Formatter stylish

[![asciicast](https://asciinema.org/a/560284.svg)](https://asciinema.org/a/560284)


### Flat format
Command ```gendiff --format plain filepath1.yaml filepath2.yaml``` //
Formatter plain

[![asciicast](https://asciinema.org/a/563624.svg)](https://asciinema.org/a/563624)