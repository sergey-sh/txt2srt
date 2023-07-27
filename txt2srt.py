#!/usr/bin/env python
import sys


LAST_MESSAGE_TIME = 5*60


def str2seconds(value):
    values = value.split(':')

    if not values[-1].isdigit():
        return None

    s = int(values[-1]) if len(values) > 0 and values[-1].isdigit() else 0
    m = int(values[-2]) if len(values) > 1 and values[-2].isdigit() else 0
    h = int(values[-3]) if len(values) > 2 and values[-3].isdigit() else 0

    return (h * 60 + m) * 60 + s


def seconds2str(value):
    s = value % 60
    mm = int(value / 60)
    m = mm % 60
    h = int(mm / 60)
    return '{:02d}:{:02d}:{:02d},000'.format(h, m, s)


def transcribe_txt_file_to_structured_iter(file_input):
    in_block = False
    time_start = None
    lines = None
    for line in file_input:
        line = line.rstrip()
        if in_block:
            if line == '':
                in_block = False
            else:
                lines.append(line)
            continue

        time_current = str2seconds(line)
        if time_current is None:
            continue

        if time_start is not None:
            yield time_start, time_current, lines
        time_start = time_current
        lines = []
        in_block = True

    if time_start is not None and lines:
        yield time_start, time_start + LAST_MESSAGE_TIME, lines


def string_extract_first_part_delimited_whitespace(line, max_length_text):
    if max_length_text <= 0 or len(line) <= max_length_text:
        return line, ''
    i = max_length_text - 1
    # find first not space char after max_length_text
    while i < len(line) and line[i:i + 1] not in (' ', ',', '.', ':', ';'):
        i += 1
    return line[:i], line[i:]


def split_message_by_max_length_iter(lines, max_length_text):
    if max_length_text is None or max_length_text <= 0:
        yield from lines
        return

    for line in lines:
        while len(line) > 0:
            first_part, line = string_extract_first_part_delimited_whitespace(line, max_length_text)
            if len(first_part.strip()) > 0:
                yield first_part


def transcribe_txt2srt(file_input, file_output, max_length_text):
    n = 1
    for time_start, time_end, lines in transcribe_txt_file_to_structured_iter(file_input):
        print(n, file=file_output)
        print(seconds2str(time_start), ' --> ', seconds2str(time_end), file=file_output)
        for line in split_message_by_max_length_iter(lines, max_length_text):
            line_stripped = line.strip()
            if line_stripped:
                print(line_stripped, file=file_output)
        print('', file=file_output)
        n += 1


def usage_help():
    print('Utility for  convert text file to srt file', file=sys.stderr)
    print('Text file format:', file=sys.stderr)
    print('MM:SS', file=sys.stderr)
    print('text ... text', file=sys.stderr)
    print('... text', file=sys.stderr)
    print('empty line is delimiter', file=sys.stderr)
    print('', file=sys.stderr)
    print('Usage: python txt2srt.py file_input file_output [max length text]', file=sys.stderr)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '/h', '--help', '/help'):
        usage_help()
        quit()

    if len(sys.argv) < 2:
        file_input = sys.stdin
        file_output = sys.stdout
    elif len(sys.argv) < 3:
        file_input = open(sys.argv[1], 'r')
        file_output = sys.stdout
    else:
        file_input = open(sys.argv[1], 'r')
        file_output = open(sys.argv[2], 'w')

    max_length_text = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    transcribe_txt2srt(file_input, file_output, max_length_text)

    if file_input != sys.stdin:
        file_input.close()

    if file_output != sys.stdout:
        file_output.close()


if __name__ == '__main__':
    main()
