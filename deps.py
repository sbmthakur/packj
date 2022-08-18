import re
import subprocess
import json

def __parse_string_for_pkg_info(line):
    try:
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

def get_python_packages(filepath):
    packages=[]
    with open(filepath) as f:
        while True:
            line = f.readline().strip()
            pkg = __parse_string_for_pkg_info(line)
            if not pkg:
                break
            packages.append(pkg)
    return packages

def get_node_packages(filepath):
    packages=[]
    with open(filepath) as f:
        pkg_data = json.load(f)

        for k,v in pkg_data['dependencies'].items():
            pkg = {
                "name": k,
                "version": v.replace('^', '').replace('~', '')
            }
            packages.append(pkg)
    return packages

def get_gems(filepath):
    packages = []
    try:
        o = subprocess.check_output(['ruby', 'parse_gemfile.rb'], stderr=subprocess.STDOUT)
        pkgs = o.decode('utf-8').split('\n')
        breakpoint()

        for pkg in pkgs:
            try:
                name_re = re.search(r".* ", pkg)
                name = name_re.group(0).replace(' ', '')

                version_re = re.search(r"\((.*?)\)", pkg)
                version = version_re.group(0).replace('(', '').replace(')', '')
            except:
                print('Error')
                continue

            pkg_data = {
                "name": name,
                "version": version
            }

            packages.append(pkg_data)

        return packages

    except subprocess.CalledProcessError as e:
        print(f'subprocess failed while parsing rubygems: {e.output}')

def get_packages_from_file(filepath, pm_name):
    packages = []
    try:
        if pm_name == 'pypi':
            packages = get_python_packages(filepath)
        elif pm_name == 'npm':
            packages = get_node_packages(filepath)
        elif pm_name == 'rubygems':
            packages = get_gems(filepath)
            breakpoint()
        
    except Exception as e:
        print("Failed to parse %s for packages" % (tmpfile, str(e)))
        pass
    finally:
        return packages

def create_html(total_risks):

	html = f"<details><summary>{total_risks} issues found with dependencies. Click here for details</summary>"
	html += "<table><tr><th>Package name</th><th>Description</th><th>Dependency file</th></tr>"
	with open('./tempfile') as f:
		for line in f:
			if '==' in line:
				break
			name, summary,file_name = line.split('|')
			html += f'<tr><td>{name}</td><td>{summary}</td><td>{file_name}</td></tr>'
		html += '</table></details>'

	file_name = "deps"
	html_report_name = f'/tmp/{file_name}.htm'

	with open(html_report_name, mode='w') as f:
		f.write(html)

	print(f'View complete report: {html_report_name}')

def main(args):
    file_names = args.file_name.split(',')

    total_risks = 0

    with open('./tempfile', mode='w') as f:
        for file_name in file_names:

            pm_name = None
            if file_name == 'requirements.txt':
                pm_name = 'pypi'
            elif file_name == 'package.json':
                pm_name = 'npm'
            elif file_name == 'Gemfile.lock':
                pm_name = 'rubygems'
            else:
                pm_name = 'pypi'

            packages = get_packages_from_file(file_name, pm_name)
            #breakpoint()

            for pkg_info in packages:
                name, version = pkg_info['name'], pkg_info['version']

                inputs = ['python', 'main.py', 'audit', pm_name, name]

                if version:
                    inputs.append(version)

                try:
                    o = subprocess.check_output(inputs, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                #except Exception as e:
                    print(f'subprocess failed: {e.output}')
                    continue

                index = None

                if pm_name == 'pypi':
                    index = -4
                elif pm_name == 'npm':
                    index = -3

                pkg_result = o.decode('utf-8').split('\n')[index]
                pkg_result = pkg_result.replace('[+] ', '')

                n = None

                try:
                    n = int(pkg_result[0])
                    total_risks += n
                except:
                    print(f'Not a numeric character {pkg_result[0]}')

                print(f'{name}| {pkg_result}| {file_name}')
                f.write(f'{name}| {pkg_result}| {file_name}\n')
        
        f.write('======')

    create_html(total_risks)
