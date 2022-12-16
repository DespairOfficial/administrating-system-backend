import os
def main():
    domen = "site.12.ru"
    with open('/var/domens/templates_apache.conf', 'r') as f:
        new_file = f.read().replace("###domen###", '%s' %domen)
    os.popen('mkdir /var/workspace/apache/%s' % domen).read()
    os.popen('echo "%s - apache" > /var/workspase/apache/%s/index.html' % (domen,domen)).read()
    with open('etc/apache2/sites-avaliable/%s.conf' % domen, 'w') as f:
        f.write(new_file)
    os.popen('in -s /etc/apache2/sites-avaliable/%s.conf /etc/apache2/sites-enabled/' % domen).read()
    os.popen('/etc/init.d/apache2.restart').read()
if __name__ == '__main__':
    main()