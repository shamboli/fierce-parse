# fierce parser
import os, re, errno, socket, argparse
import platform, subprocess

parser = argparse.ArgumentParser(description="Fierce result parsing utility to verify if host pings")
parser.add_argument('--connect', nargs='?', const=0, type=int, help="test ping to host", required=True)
parser.add_argument('--infile', type=str, help="input fierce .txt file", required=True)
parser.add_argument('--outpath', type=str, help="export path for ip table and hostname output", required=True)
args = parser.parse_args()

def is_dir(dirname):
    # Checks if a path is an actual directory
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname

def is_valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

def is_valid_hostname(hostname):
    # strip
    hostname = hostname.strip()
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def check_line(line):
    result = []
    if line.startswith("Found:"):
        # parse for hostname and ip 
        ip_value = ''.join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', line))
        host_value = line.split(" ")[1]
        # check and group these values 
        if is_valid_ip(ip_value) and is_valid_hostname(host_value):
            return ip_value, host_value
        else:
            return None
    elif ((re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)) and not line.startswith("Found:")): 
        # try to pull out general values
        values = re.sub('[,}{\"\' ]', '', line).split(":")
        # the ip hopefully
        if re.findall(r'[0-9]+(?:\.[0-9]+){3}', values[0]):
            ip_value = values[0]
        else:
            print "ip false ", values[0]
            ip_value = None
        if is_valid_hostname(values[1]):
            host_value = values[1].strip()
        else:
            print "host invalid ", values[1]
            host_value = None
        # check and group 
        if (ip_value != None) and (host_value != None):
            return ip_value, host_value
    else:
        return None

def ping_host(host):
    response = os.system("fping -t100 -c2 " + host + ">/dev/null 2>/dev/null")
    if response == 0:
        return True

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# validate arguments 
outpath = args.outpath
infile = args.infile
if not os.path.isdir(outpath):
    print "path does not exist: {0}".format(outpath)
    exit 
elif not os.path.isfile(infile):
    print "input file does not exist: {0}".format(infile)
    exit

connect = args.connect
if connect == 1:
    print "operating in connect mode"
    connect = True
elif connect == 0: 
    print "operating in no connect mode"
    connect = False
else:
    print "--connect= accepts 1 or 0 as arguments"
    exit

# its ok 
output_path = os.path.join(outpath, os.path.splitext(os.path.basename(infile))[0])
mkdir_p(output_path)
print "writing to path: ", output_path
fh = open(os.path.join(output_path, "hostname_output.txt"), "a+")
fi = open(os.path.join(output_path, "ip_output.txt"), "a+")
open_file = open(infile, "r")
for line in open_file:
    # check line
    result = check_line(line)
    if (check_line(line) != None):
        ip_value, host_value = result
        if (ip_value != None) and (host_value != None):
            if connect: 
                print "testing: ", ip_value, " | ", host_value
                # test ping and dump
                if ping_host(ip_value):
                    # host up, write out 
                    print "writing: ", ip_value, " | ", host_value
                    fi.write(ip_value)
                    fi.write("\n")
                    fh.write(host_value)
                    fh.write("\n")
            elif not connect: 
                # dump information
                print "writing: ", ip_value, " | ", host_value
                fi.write(ip_value)
                fi.write("\n")
                fh.write(host_value)
                fh.write("\n")