from subprocess import call
import os

startpath = os.path.dirname(__file__)
inkscape_path = "C:/Program Files/Inkscape/inkscape.exe"

def iteration(subpath='', overwrite=False):
    path = startpath + subpath
    for f in os.listdir(path):
        if f.startswith('.'):
            continue
        fname = f'{path}/{f}'
        if f.endswith('.png'):
            if overwrite or not os.path.isfile(f'{path}/{f[:-4]}.svg'):
                print(f)
                call([inkscape_path, '-z', fname, '-l',
                      f'{fname[:-4]}.svg', '--without-gui'])
        if os.path.isdir(fname):
            iteration(f'{subpath}/{f}', overwrite)


if __name__ == '__main__':
    iteration()
