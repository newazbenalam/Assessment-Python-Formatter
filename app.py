import argparse
import os

from app import formatJsonDoc

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Python formatter')
  parser.add_argument('--input', dest='input', type=str, help='Name of the input file')
  args = parser.parse_args()
  
  out = formatJsonDoc(args.input)

  with open("formatted_"+os.path.basename(args.input), "w") as outfile:
    outfile.write(out)

  print(f"Formatted JSON saved to root folder")