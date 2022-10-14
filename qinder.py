import math

from Bio import SeqIO


def read_file(file_in):
    list_seq, l_header = [], []
    for record in SeqIO.parse(file_in, "fasta"):
        l_header.append(record.id)
        list_seq.append(record.seq)
    return l_header, list_seq


def sequence_score(line, angle, radius):
    g_c_sum_value, a_t_sum_value = 0, 0
    r = radius

    sample_len = len(line)

    for i, gene in enumerate(line):
        if gene in ('G', 'g'):
            if i + 1 < len(line):
                if line[i + 1] in ('G', 'g'):
                    g_c_sum_value += r
                if line[i + 1] in ('A', 'a', 'T', 't'):
                    g_c_sum_value += r / 2
                if line[i + 1] in ('A', 'a'):
                    a_t_sum_value += r / 2
                if line[i + 1] in ('T', 't'):
                    a_t_sum_value -= r / 2
        if gene in ('C', 'c'):
            if i + 1 < len(line):
                if line[i + 1] in ('C', 'c'):
                    g_c_sum_value -= r
                if line[i + 1] in ('A', 'a', 'T', 't'):
                    g_c_sum_value -= r / 2
                if line[i + 1] in ('A', 'a'):
                    a_t_sum_value += r / 2
                if line[i + 1] in ('T', 't'):
                    a_t_sum_value -= r / 2
        if gene in ('A', 'a'):
            if i + 1 < len(line):
                if line[i + 1] in ('A', 'a'):
                    a_t_sum_value += r
                if line[i + 1] in ('G', 'g', 'C', 'c'):
                    a_t_sum_value += r / 2
                if line[i + 1] in ('G', 'g'):
                    g_c_sum_value += r / 2
                if line[i + 1] in ('C', 'c'):
                    g_c_sum_value -= r / 2
        if gene in ('T', 't'):
            if i + 1 < len(line):
                if line[i + 1] in ('T', 't'):
                    a_t_sum_value -= r
                if line[i + 1] in ('G', 'g', 'C', 'c'):
                    a_t_sum_value -= r / 2
                if line[i + 1] in ('G', 'g'):
                    g_c_sum_value += r / 2
                if line[i + 1] in ('C', 'c'):
                    g_c_sum_value -= r / 2

    g_c_value = g_c_sum_value / sample_len
    a_t_value = a_t_sum_value / sample_len

    sin_of_a_t = math.sin(math.radians(angle)) * a_t_value
    final_score = g_c_value - sin_of_a_t
    return line, final_score


class Qinder:

    @staticmethod
    def qinder_app(input_file, window, score, offset, angle, radius, is_all_score):

        limit = window
        offset = offset

        l_header, list_seq = read_file(input_file)

        result_dict = dict()

        whole_sequence = list_seq[0]
        for _offset in range(0, int(len(whole_sequence)), offset):
            _sequence, _score = sequence_score(whole_sequence[_offset:(limit + _offset)], angle, radius)
            if is_all_score:
                if _score > score or -score > _score:
                    result_dict[str(_sequence)] = _score
            else:
                if _score > score:
                    result_dict[str(_sequence)] = _score

        return result_dict
