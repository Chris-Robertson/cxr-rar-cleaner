import os
import glob
import shutil
import subprocess

torrent_dir = "/volume1/downloads/complete"
unrar_dir = "/volume1/downloads/complete/_unrar"
unrar_flag_file = ".unrar"
unrared_filetypes = ["mkv", "mp4", "avi", "iso"]
unrar_command = ["unrar", "x"]


def main():
    setup_dirs()
    walk_dirs()


def walk_dirs():

    for dir_path, sub_dirs, files in os.walk(torrent_dir):

        print(f"CHECKING {dir_path}")

        if has_unrar_file(dir_path):
            continue

        rar_files = get_rar_files(dir_path)

        if len(rar_files) == 0:
            save_unrar_file(dir_path)
            continue

        moved_files = move_unrared_files(dir_path)

        if len(moved_files) > 0:
            save_unrar_file(dir_path)
            continue

        unrar_to_unrar_dir(rar_files)
        save_unrar_file(dir_path)


def setup_dirs():
    try:
        os.makedirs(unrar_dir)
    except FileExistsError:
        pass


def has_unrar_file(dir_path):
    unrar_file = os.path.join(dir_path, unrar_flag_file)
    return os.path.isfile(unrar_file)


def get_rar_files(dir_path):
    return get_files_with_extension(dir_path, "rar")


def move_unrared_files(dir_path):
    unrared_files = get_unrared_files(dir_path)
    for unrared_file in unrared_files:
        move_to_unrar_dir(unrared_file)
    return unrared_files


def get_unrared_files(dir_path):
    unrared_files = []
    for filetype in unrared_filetypes:
        unrared_files.extend(get_files_with_extension(dir_path, filetype))
    return unrared_files


def get_files_with_extension(dir_path, extension):
    return glob.glob(f"{dir_path}/*.{extension}")


def save_unrar_file(dir_path):
    fp = open(os.path.join(dir_path, unrar_flag_file), "x")
    fp.close()


def move_to_unrar_dir(file):
    move(file, new_file_path(file, unrar_dir))


def move(file, destination):
    moved_file = shutil.move(file, destination)
    print(f"MOVED {file} TO {moved_file}")


def unrar_to_unrar_dir(rar_files):
    for rar_file in rar_files:
        unrar(rar_file, unrar_dir)


def unrar(file, destination=None):
    subprocess.run(
        unrar_command + [file, destination],
        text=True,
        stderr=subprocess.STDOUT
    )
    print(f"UNRARED {file} TO {destination}")


def new_file_path(file, new_path):
    return os.path.join(new_path, os.path.basename(file))


if __name__ == '__main__':
    main()
