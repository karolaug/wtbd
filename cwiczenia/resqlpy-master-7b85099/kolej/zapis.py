import sys, os
import re
import datetime

UNLOAD = 10

def change(point, minutes):
    try:
        return point.replace(minute=point.minute+minutes)
    except ValueError:
        minutes2 = (point.minute + minutes) % 60
        hour2 = point.hour + (-1 if minutes < 0 else +1)
        return point.replace(hour=max(min(hour2, 0), 23), minute=minutes2)

train_re = re.compile(r'([A-Z]{2,3}) \s* (\d+)', re.X)
time_re = re.compile(r'(\d\d) : (\d\d)', re.X)
station_re = re.compile(r'([\D ()-]+?)', re.X)

start_re = re.compile(r'^\s* %s \s+ %s \s+ %s \s*$' %
                      (station_re.pattern,
                       time_re.pattern, train_re.pattern),
                      re.X)
inter_re = re.compile(r'^\s* %s \s+ %s \s+ %s \s*$' %
                      (station_re.pattern,
                       time_re.pattern, time_re.pattern),
                      re.X)
end_re = re.compile(r'^\s* %s \s+ %s \s*$' %
                    (station_re.pattern, time_re.pattern),
                    re.X)

def parse(input):
    line = input.readline()
    m = start_re.match(line)
    if not m:
        raise ValueError('failed', line)
    station = m.group(1)
    train = m.group(4) + m.group(5)
    start = datetime.time(int(m.group(2)), int(m.group(3)))
    yield train, station, None, start

    lines = input.readlines()
    for line in lines[:-1]:
        m = inter_re.match(line)
        if not m:
            sys.stderr.write("warning: failed for '%r'\n" % line)
            continue
        station = m.group(1)
        start = datetime.time(int(m.group(2)), int(m.group(3)))
        end = datetime.time(int(m.group(4)), int(m.group(5)))
        yield train, station, start, end

    m = end_re.match(lines[-1])
    if not m:
        raise ValueError('failed', line)
    station = m.group(1)
    start = datetime.time(int(m.group(2)), int(m.group(3)))
    yield train, station, start, None

def normalize(rows):
    for train, station, start, end in rows:
        if start is None:
            start = change(end, -UNLOAD)
        if end is None:
            end = change(start, +UNLOAD)
        yield train, station, start, end

def output(rows, **args):
    for train, station, start, end in rows:
        print('%02d:%02d %02d:%02d %s' % (
                start.hour, start.minute,
                end.hour, end.minute, station), **args)

def convert(input):
    lines = list(normalize(parse(input)))
    train = lines[0][0]
    filename = train + '.info'
    if os.path.exists(filename):
        raise ValueError('exits ' +  filename)
    print('writing ', filename)
    with open(filename, 'w') as out:
        output(lines, file=out)
    with open(filename) as inp:
        sys.stdout.write(inp.read())

if __name__ == '__main__':
    convert(sys.stdin)
