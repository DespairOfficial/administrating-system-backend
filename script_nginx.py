import os
def main():
    domen = "site.12.ru"
    with open('/var/domens/templates_nginx.conf', 'r') as f:
        new_file = f.read().replace("###domen###", '%s' %domen)
    os.popen('mkdir /var/workspace/nginx/%s' % domen).read()
    os.popen('echo "%s - nginx" > /var/workspase/nginx/%s/index.html' % (domen,domen)).read()
    with open('etc/nginx/sites-avaliable/%s.conf' % domen, 'w') as f:
        f.write(new_file)
    os.popen('in -s /etc/nginx/sites-avaliable/%s.conf /etc/nginx2/sites-enabled/' % domen).read()
    os.popen('/etc/init.d/nginx.restart').read()
if __name__ == '__main__':
    main()