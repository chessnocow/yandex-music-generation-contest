from argparse import ArgumentParser
from Levenshtein import distance
from data_utils import read_abc
from glob import glob
from tqdm import tqdm
from pathlib import Path


def bars_similiarity(bar1, bar2):
    distances = []
    for n1 in bar1:
        distances.append(min([distance(n1, n2) / (len(n1) + len(n2)) for n2 in bar2]))
    
    return sum(distances) / len(distances)


def parse():
    parser = ArgumentParser()

    parser.add_argument("input_dir")
    parser.add_argument("output_dir")

    return parser.parse_args()


def main(args):
    bars = []
    bars_similaruty = []

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    file_index = 0

    print("preprocessing data...")
    for i in tqdm(list(input_dir.glob("*.abc"))):
        abc = read_abc(i)
        if abc is None:
            continue
            
        keys, abc = abc.split(" @ ")
        abc = abc.replace(" ", "").split("|")
        num_bars = len(abc) // 16
        
        if num_bars == 0:
            continue
            
            
        for i in range(num_bars):
            if "x8" in "|\n".join(abc[:i+16]):
                continue

            sim = bars_similiarity(abc[i:i+8], abc[i+8:i+16])
            
            if sim < 0.17:
                continue

            with open(output_dir.joinpath(f"{file_index}.abc"), "w") as f:
                f.write(keys.replace(" ", "\n") + "\n" + "|\n".join(abc[:i+16]))
            
            file_index += 1

if __name__ == "__main__":
    args = parse()
    main(args)