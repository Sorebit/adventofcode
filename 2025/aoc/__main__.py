from pathlib import Path
import shutil
import sys


def touch_inputs(in_dir: Path, inputs: list[str]):
    for in_file in inputs:
        in_path = in_dir / in_file
        print(f"Touching input file {in_path}")
        in_path.touch()


def copy_template_if_new(src: Path, dst: Path):
    if dst.exists():
        print(f"File {dst} already exists, skipping")
        return
    print(f"Copying template to {dst}")
    shutil.copyfile(src, dst)


def scaffold_day(num):
    print(f"Scaffolding day number {num}")

    here = Path(__file__).parent
    year_solutions_dir = here.parent

    # Copy template to 20XX/{{num}}.py
    template_src = here / "template.py"
    destination = year_solutions_dir / f"{num}.py"
    copy_template_if_new(template_src, destination)

    # Create input directory 2022/in/{{num}}/
    in_dir = year_solutions_dir / f"in/{num}"
    print(f"Creating directory {in_dir}")
    in_dir.mkdir(parents=True, exist_ok=True)

    touch_inputs(in_dir, ["input", "test_example"])

def usage():
    print(f"Usage: {sys.argv[0]} [arg]")
    print("Arguments")
    print("num\t: day number such as 09, or 24")
    exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()        
    num = sys.argv[1]
    scaffold_day(num)
