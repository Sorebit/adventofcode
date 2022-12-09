from pathlib import Path
import shutil
import sys


def copy_template_if_new(src: Path, dst: Path):
    if dst.exists():
        print(f'File {dst} already exists, skipping')
        return
    print(f'Copying template to {dst}')
    shutil.copyfile(src, dst)


def scaffold_day(num):
    print(f'Scaffolding day number {num}')

    here = Path(__file__).parent
    template_src = here / 'template.py'

    # Copy template to 2022/{{num}}.py
    aoc_2022_dir = here.parent
    destination = aoc_2022_dir / f'{num}.py'
    copy_template_if_new(template_src, destination)

    # Create input directory 2022/in/{{num}}/
    in_dir = aoc_2022_dir / f'in/{num}'
    print(f'Creating directory {in_dir}')
    in_dir.mkdir(parents=True, exist_ok=True)

    # Touch in/{{num}}/input
    in_file = in_dir / 'input'
    print(f'Touching input file {in_file}')
    in_file.touch()


if __name__ == '__main__':
    num = sys.argv[1]
    scaffold_day(num)
