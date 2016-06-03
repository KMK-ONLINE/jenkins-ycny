import os


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def install_desktop():
    target = os.path.expanduser('~/.local/share/applications/')
    return copy_desktop(target)


def install_autostart():
    target = os.path.expanduser('~/.config/autostart/')
    return copy_desktop(target)


def copy_desktop(target):
    if not os.path.exists(target):
        os.makedirs(target)

    s = open(ROOT_PATH + '/' + 'jenkins.desktop.in', 'r').read()
    s = s.replace('{ROOT_PATH}', ROOT_PATH)

    target_file = target + '/' + 'jenkins.desktop'
    if not os.path.exists(target_file):
        open(target_file, 'w').write(s)
        return True


def main():
    install_desktop()
    install_autostart()


if __name__ == '__main__':
    main()
