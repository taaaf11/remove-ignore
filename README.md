# remove-ignore
A small installable package that, when run, deletes the paths (files and directories) matching ignore patterns given in git ignore file(s).


### Usage
When run without any cli option, it checks for `.gitignore` file in current directory, and gets patterns from it. It then starts deleting matching files and directories recursively.
If `.gitignore` is not present, an error message is shown and the process exits.
There are cli options to customize program's behaviour.

- To specify custom ignore file(s), you can specify space-separated list of paths. For example, if you want to tell the program to use `.gitignore` and `ignore` files present in pwd, you can use:
```bash
remign -f ignore .gitignore
```

- If you want to change top directory i.e. from where deletion starts, you can use:
```bash
remign -t /path/to/top/directory
```


### Installation
1. Clone repository or download zip and extract it.
2. `cd` into project root.
3. Run `pip install .` or `pipx install .` .
