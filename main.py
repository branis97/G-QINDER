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
    _radius = 3
    try:
        opts, args = getopt.getopt(argv, "i:o:w:s:f:a:r:")
    except getopt.GetoptError:
        print(
            '-i <input_file> -o <output_repository> -w <window> -s <score threshold> -f <offset> -a <angle> '
            '-r <radius>\n')
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('To run Qinder use the command line: \n')
            print('-i <input_file> -o <output_repository> -w <window> -s <score threshold> -f <offset>'
                  ' -a <angle> -r <radius>\n')
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
        elif opt in ("-r", "--radius"):
            _radius = arg

    return _input_file, _output_file, int(_window), float(_score), int(_offset), int(_angle), int(_radius)


if __name__ == "__main__":
    try:
        input_file, output_file, window, score, offset, angle, radius = main(sys.argv[1:])
        file_name = input_file.split("/")[-1]
        name = file_name.split(".")
    except Exception as e:
        print('Invalid params ' + '(' + str(e) + ')')
        sys.exit()

    OPF = os.listdir(output_file)
    DIR = "Results_" + str(name[0])
    file_name = input_file.split("/")[-1]
    file_fasta = file_name.split(".")

    _new_result_dir = output_file + "/" + DIR + "/" + file_fasta[0] + "-window:" + str(window) + "-score:" + str(
        score) + "-offset:" + str(offset) + "-angle:" + str(angle) + "-radius:" + str(radius) + ".txt"

    if DIR in OPF:
        print('\nRe-run of Qinder on same input file\n')
    else:
        os.makedirs(output_file + "/" + DIR + "/", mode=0o777)
        print("\nCreating new result file\n")

    plot = []

    file_in = open(input_file, "r")
    print("Input file:", file_fasta[0], "\n")

    result_file = open(_new_result_dir, "w")
    startTime = time.time()

    _qinder = Qinder()
    res = _qinder.qinder_app(file_in, window, score, offset, angle, radius)

    for key, value in res.items():
        result_file.write('%s\t%s\n' % (key, value))
    file_in.close()

    fin = time.time()

    print("\nResults generated in:", round(fin - startTime, 2), "sec")
    print("\nResults stored in:", DIR)

    result_file.close()
