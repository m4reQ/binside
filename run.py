import argparse
import sys

from binside import app as binside_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('app_name', choices=('binside', 'binside_trainer'))

    args = parser.parse_args(sys.argv.copy()[1:])
    match args.app_name:
        case 'binside':
            binside_app.run(sys.argv)
        case 'binside_trainer':
            raise NotImplementedError('Binside trainer app is not implemented yet.')
        case invalid:
            raise ValueError(f'Invalid option: {invalid}')
