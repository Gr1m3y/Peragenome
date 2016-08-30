
"""
Peragenome
"""

import csv

def main():
    logging.basicConfig(filename='test/debug.log', level=logging.INFO)
    logging.info('STARTED')

    #TODO: main code goes here

    print csv.get_nth_field(1, 'hello,world')

    logging.info('FINISED')

if __name__ == '__main__':
    main()
