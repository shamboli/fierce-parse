# fierce DNS recon parse utility
outputs two files containing ip addresses and hostnames when given a fierce result

## requirements
- fping
- fierce dns recon tool https://github.com/mschwager/fierce

## usage
```bash
# generate files based on if host replies to a ping
python ./fierce_parse.py --connect 1 --infile input.txt --outpath /path/to/output

# parse fierce result and dump ip/hostnames
python ./fierce_parse.py --connect 0 --infile input.txt --outpath /path/to/output
```

```bash
user@know:/mnt/e/github/fierce_parse$ python ./fierce_parse.py
usage: fierce_parse.py [-h] --connect [CONNECT] --infile INFILE --outpath
                       OUTPATH
fierce_parse.py: error: argument --connect is required
```

## example
![example of input/outputs](https://i.imgur.com/ZkhE8d6.jpg)
