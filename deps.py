import re
import subprocess

def __parse_string_for_pkg_info(line):
    try:
        #breakpoint()
        if line == '':
            return None
        version_search_outcome = re.search(r'(.*)(==|>=|<=)(.*)', line)
        if version_search_outcome is not None:
            pkg = {
                "name": version_search_outcome.group(1),
                "version": version_search_outcome.group(3)
            }
        else:
            pkg = {
                "name": line
            }
        return pkg
    except Exception as e:
        raise Exception("Failed to parse %s: %s" % (line, str(e)))

def get_packages_from_file(filepath):
    packages=[]
    try:
        with open(filepath) as f:
            while True:
                line = f.readline().strip()
                pkg = __parse_string_for_pkg_info(line)
                if not pkg:
                    break
                packages.append(pkg)
        #breakpoint()
        return packages
    except Exception as e:
        print("Failed to parse %s for packages" % (tmpfile, str(e)))
        pass
    finally:
        return packages

def create_html(total_risks):

	html = f"<details><summary>{total_risks} riks found</summary>"
	html += "<table>"
	with open('./tempfile') as f:
		for line in f:
			if '==' in line:
				break
			name, summary = line.split('|')
			html += f'<tr><td>{name}</td><td>{summary}</td></tr>'
		html += '</table></details>'

	file_name = "deps"
	html_report_name = f'/tmp/{file_name}.htm'

	with open(html_report_name, mode='w') as f:
		f.write(html)

	print(f'View complete report: {html_report_name}')

def main(args):
    file_name = args.file_name
    packages = get_packages_from_file(file_name)

    pm_name = None
    if file_name == 'requirements.txt':
        pm_name = 'pypi'
    elif file_name == 'package.json':
        pm_name = 'npm'
    elif file_name == 'Gemfile.lock':
        pm_name = 'rubygems'
    else:
        pm_name = 'pypi'


    total_risks = 0

    with open('./tempfile', mode='w') as f:
        for pkg_info in packages:
            name, version = pkg_info['name'], pkg_info['version']

            inputs = ['python', 'main.py', 'audit', pm_name, name]

            if version:
                inputs.append(version)

            o = subprocess.check_output(inputs, stderr=subprocess.STDOUT)
            pkg_result = o.decode('utf-8').split('\n')[-4]
            pkg_result = pkg_result.replace('[+] ', '')

            n = None

            try:
                n = int(pkg_result[0])
                total_risks += n
            except e:
                print(n)


            f.write(f'{name}| {pkg_result}\n')

            #print(name, pkg_result)

        f.write('======')
    
    create_html(total_risks)




    
