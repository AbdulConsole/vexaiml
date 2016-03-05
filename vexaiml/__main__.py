import argparse


def main(text_address=None, aiml_address=None):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_address', action='store', default='')
    parser.add_argument('--aiml_address', action='store', default='')

    args = parser.parse_args()
    main(args.text_address, args.aiml_address)
