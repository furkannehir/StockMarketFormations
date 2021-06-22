from StockClass import Label
import argparse
import lstm
import Label
import lstm

#TODO create dataset fucked up now

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', action='store', type=str, help='dataset file path', required=True)
    parser.add_argument('-t', '--train', action='store_true', help='If train or not', required=False)
    parser.add_argument('-e', '--epoch', action='store', type=int, help='epoch count', required=False)
    parser.add_argument('-s', '--split', action='store', type=float, help='train test split ratio', required=False)
    parser.add_argument('-l', '--labeled', action='store_true', help='if data labeled', required=False)
    return parser.parse_args()

def main():
    dataset_dir = 'dataset_CAC40/'
    epoch = 50
    split = 0.8
    args = parse_args()
    filepath = dataset_dir + args.filepath
    labeled = args.labeled 
    cols = ['High', 'Low', 'Label', 'Open', 'Close']
    if args.epoch:
        epoch = args.epoch
    if args.split:
        split = args.split
    if args.train:
        lstm.train(filepath, epoch, split, cols, labeled=labeled)
    else:
        lstm.test()

if __name__ == "__main__":
	main()
    # lst = [1,2,3,4,5,6]
    # print(lst[:-1])