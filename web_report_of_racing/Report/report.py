"""
This module read data from 2 files(start.log, end.log),
order racers by time and print report that shows the top 15 racers
and the rest after underline.
"""

from datetime import datetime
import argparse

class Racer:
    """
    Create a new object 'Racer'.
    Constructors:
    __init__()
    Operators:
    __lt__
    """

    def __init__(self, name, team, result):
        """
        Constructor.
        Arguments required:
        name: str, team: str, result: timedelta
        """
        self.name = name
        self.team = team
        self.result = result

    def __lt__(self, other):
        """This method is needed to compare odjects(Racer) using sort() method"""
        return self.result < other.result


def get_time_data(path: str) -> dict:
    """
    This func prepares data to get result.
    It takes a path(str), opens the file for reading and
    return data from file(for each racer) in dict like {"racer abbreviation" : data(datetime type)}
    """
    data = dict()
    with open(path, 'r') as f:
        for line in f.read().split('\n'):
            if line:  # if line isn't empty
                data[line[:3]] = datetime.strptime(
                    line[3:], '%Y-%m-%d_%H:%M:%S.%f')
    return data


def get_result(start: dict, end: dict) -> dict:
    """
    This func calculates the result.
    It takes 2 dicts (with the start data and the end data) and subtracts
    the difference between the end time and the start time for each racer.
    The func return dict like {"racer abbreviation" : result(timedelta type)}
    """
    result = dict()
    for key in end.keys():
        result[key] = end[key] - start[key]
    return result


def build_report(folder_path: str) -> list:
    """
    This func generates a race report.
    It takes the path to the data folder and
    return an array of race data (the array is sorted by time [timedelta]).
    """
    start_path = f'{folder_path}/start.log'
    end_path = f'{folder_path}/end.log'

    start_data = get_time_data(start_path)
    end_data = get_time_data(end_path)

    results = get_result(start_data, end_data)

    abbs = dict()
    with open("./abbreviations.txt", 'r') as f:
        for line in f.read().split('\n'):
            abbs[line[:3]] = line[4:].split('_')

    report_out = [Racer(abbs[racer][0], abbs[racer][1], results[racer]) for racer in results.keys()]
    report_out.sort()
    return report_out


def print_report(report: list, asc=None, driver=None, desc=None):
    """
    This func takes report and prints it based on several params.
    """
    if driver:
        for racer in report:
            if racer.name == driver:
                print(f'{racer.name} | {racer.team} | {str(racer.result)}')
                break
        else:
            raise NameError('Name of driver not found')
    elif desc:
        position = len(report)
        for racer in report[::-1]:
            print(f'{position}. {racer.name} | {racer.team} | {str(racer.result)}')
            position -= 1
            if position == 15:
                print(75*'-')
    elif asc:
        position = 0
        for racer in report:
            position += 1
            print(f'{position}. {racer.name} | {racer.team} | {str(racer.result)}')
            if position == 15:
                print(75*'-')


def main():
    parser = argparse.ArgumentParser(
        description='Process files with data on race results')

    parser.add_argument(
        '--files',
        help='folder path',
        type=str)

    parser.add_argument(
        '--driver',
        help="racer's name")

    parser.add_argument(
        '--asc',
        action='store_true',
        default=True)

    parser.add_argument(
        '--desc',
        action='store_true')

    args = parser.parse_args()
    result = build_report(args.files)
    print_report(result, args.asc, args.driver, args.desc)


if __name__ == '__main__':
    main()
