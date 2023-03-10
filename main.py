import getopt
import os
import sys
import time

from qinder import Qinder


def main(argv):
    if not argv:
        sys.stdout.write("Sorry: you must specify at least an argument\n")
        sys.stdout.write("More help available with -h or --help option\n")
        sys.exit(1)

    _input_file = ''
    _output_file = ''
    _window = 25
    _score = 1.2
    _offset = 5
    _angle = 15
    _all_score = False
    _is_multiplication_enabled = False
    try:
        opts, args = getopt.getopt(argv, "i:o:w:s:x:f:a:m:")
    except getopt.GetoptError:
        print(
            '-i <input_file> -o <output_repository> -w <window> -s/x <score threshold/negatives included> '
            '-f <offset> -a <angle> -m <multiplication show if "true">\n')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('To run Qinder use the command line: \n')
            print('-i <input_file> -o <output_repository> -w <window> -s/x <score threshold/negatives included> '
                  '-f <offset> -a <angle> -m <multiplication show if "true">\n')
            sys.exit()
        elif opt in ("-i", "--input"):
            _input_file = arg
        elif opt in ("-o", "--output"):
            _output_file = arg
        elif opt in ("-w", "--window"):
            _window = arg
        elif opt in ("-s", "--score"):
            _score = arg
        elif opt in ("-f", "--offset"):
            _offset = arg
        elif opt in ("-a", "--angle"):
            _angle = arg
        elif opt in ("-x", "--all-score"):
            _score = arg
            _all_score = True
        elif opt in ("-m", "--multiplication"):
            _is_multiplication_enabled = True

    return _input_file, _output_file, int(_window), float(_score), int(_offset), int(_angle), bool(
        _all_score), bool(_is_multiplication_enabled)


def file_write(results, file, _is_multiplication_enabled):
    _header = "G-QINDER Beta\nViglasky V., Osif B., Trizna L.\n2023\n\nRESULTS\n\ncolumn 1 = position, column 2 = " \
              "sequence, column 3 = score\n\n"
    file.write(_header)
    for key, value in results.items():
        (position, found_value, g4_found_value) = value
        file.write('%s\t%s\t\t\t%s\t\t\t%s\n' % (
            position, key, found_value, g4_found_value)) if _is_multiplication_enabled else file.write(
            '%s\t%s\t\t\t%s\n' % (position, key, found_value))


if __name__ == "__main__":
    try:
        input_file, output_file, window, score, offset, angle, is_all_score, is_multiplication_enabled = main(
            sys.argv[1:])
        file_name = os.path.split(input_file)[-1]
        name = file_name.split(".")
    except Exception as e:
        print('Invalid params ' + '(' + str(e) + ')')
        sys.exit()

    OPF = os.listdir(output_file)
    DIR = "Results_" + str(name[0])
    file_name = os.path.split(input_file)[-1]
    file_fasta = file_name.split(".")

    score_file_names = ["-score(G)-", "-score(C)-"] if is_all_score else ["-score-"]

    _new_result_dirs = []

    for _dir_name in score_file_names:
        _new_result_dirs.append(
            os.path.join(output_file, DIR, file_fasta[0] + "-window-" + str(window) + _dir_name + str(
                score) + "-offset-" + str(offset) + "-angle-" + str(angle) + ".txt"))

    if DIR in OPF:
        print('\nRe-run of Qinder on same input file\n')
    else:
        os.makedirs(os.path.join(output_file, DIR), mode=0o777)
        print("\nCreating new result file\n")

    plot = []

    file_in = open(input_file, "r")
    print("Input file:", file_fasta[0], "\n")

    result_file_g = open(_new_result_dirs[0], "w")

    result_file_c = is_all_score and open(_new_result_dirs[1], "w")

    startTime = time.time()

    _qinder = Qinder()
    res_g, res_c = _qinder.qinder_app(file_in, window, score, offset, angle, is_all_score)

    file_write(res_g, result_file_g, is_multiplication_enabled)
    is_all_score and file_write(res_c, result_file_c, is_multiplication_enabled)

    file_in.close()

    fin = time.time()

    print("\nResults generated in:", round(fin - startTime, 2), "sec")
    print("\nResults stored in:", DIR)

    result_file_g.close()
    is_all_score and result_file_c.close()
