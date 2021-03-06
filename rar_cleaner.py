import os
import glob
import shutil
import subprocess

movies_dir = "/volume1/data/torrents/movies"
tv_dir = "/volume1/data/torrents/tv"
unrar_dir = "/volume1/data/torrents/_unrar"
unrar_flag_file = ".unrar"
hardlink_flag_file = ".hardlink"
unrared_filetypes = ["mkv", "mp4", "avi", "iso"]
unrar_command = ["unrar", "x"]


def main():
    setup_dirs()
    walk_dirs_for_unrar(movies_dir)
    walk_dirs_for_unrar(tv_dir)
    # walk_dirs_for_hardlink(downloads_dir)


def walk_dirs_for_unrar(start_dir):

    for dir_path, sub_dirs, files in os.walk(start_dir):

        print(f"CHECKING FOR UNRAR {dir_path}")

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


def walk_dirs_for_hardlink(start_dir):

    for dir_path, sub_dirs, files in os.walk(start_dir):

        print(f"CHECKING FOR HARDLINK {dir_path}")
        if has_hardlinks_file(dir_path):
            continue

        save_hardlink_file(dir_path)


def setup_dirs():
    try:
        os.makedirs(unrar_dir)
    except FileExistsError:
        pass


def has_unrar_file(dir_path):
    return is_file(os.path.join(dir_path, unrar_flag_file))


def has_hardlinks_file(dir_path):
    return is_file(os.path.join(dir_path, hardlink_flag_file))


def is_file(file):
    return os.path.isfile(file)


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
    save_file(dir_path, unrar_flag_file)


def save_hardlink_file(dir_path):
    save_file(dir_path, hardlink_flag_file)


def save_file(dir_path, file):
    fp = open(os.path.join(dir_path, file), "x")
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
