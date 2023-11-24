import os
import argparse
import sys
import io


def read_lines(file):
    file_bytes = file.read()
    text = file_bytes.decode()
    lines = text.split(os.linesep)[:-1]
    return lines


def get_file_name(file_path):
    file_name = file_path.split(os.path.sep)[-1]
    return file_name


def count_characters(file):
    file.seek(0)  # seek to the beginning of the files
    text = file.read()
    return len(text)


def count_lines(file):
    file.seek(0)
    lines = read_lines(file)
    return len(lines)


def count_words(file):
    file.seek(0)
    lines = read_lines(file)
    text = " ".join(lines)
    words_count = len(text.split())
    return words_count


def get_size(file):
    file.seek(0, 2)
    file_size = file.tell()
    return file_size


def main(args):
    # if a file path is provided

    if args.filename:
        try:
            file = open(args.filename, "rb")
        except OSError as e:
            print(e)
            sys.exit(1)

    else:
        file = io.BytesIO()
        input_bytes = sys.stdin.read().encode()
        file.write(input_bytes)

    # if no options provided

    no_options_provided = not args.c and not args.l and not args.w and not args.m
    outputs = []

    if args.c:
        file_size_bytes = get_size(file)
        outputs.append((file_size_bytes))
    if args.l or no_options_provided:
        lines_count = count_lines(file)
        outputs.append(lines_count)

    if args.w or no_options_provided:
        word_count = count_words(file)
        outputs.append(word_count)

    if args.m or no_options_provided:
        characters_count = count_characters(file)
        outputs.append(characters_count)

    file_name = "" if not args.filename else get_file_name(args.filename)
    outputs.append(file_name)
    print("    " + "   ".join(map(str, outputs)))
    file.close()


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="wc",
        description="counts bytes, lines, characters, size of a file or a file stream",
    )
    parser.add_argument("filename", nargs="?")
    parser.add_argument("-c", action="store_true", help="shows file size in bytes")
    parser.add_argument("-l", action="store_true", help="shows lines count")
    parser.add_argument("-w", action="store_true", help="shows words count")
    parser.add_argument("-m", action="store_true", help="shows characters count")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
