#!/Users/yakkshit/Desktop/DebianMirror/env/bin/python
import sys
import gzip
import requests
from io import BytesIO

class Debian:
    def __init__(self) -> None:
        # initialize the mirror URL for the Debian package and get package details
       self.mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
       self.package_details = self.req_package_details()
       self.package_list = None
    def req_status(self, architecture):
        # validate the architectureitecture package and get package count data
        self.validate_package(architecture)
        data = self._get_debian_package_data(architecture)
        package_list = self.count_json(data, architecture)
        data.close()
        return package_list[:10]
    def get_package_list(self):
        # return package list
        return self.package_list
    def get_available_architectures(self):
        # return list of available architectureitectures
        return list(self.package_details.keys())
    def validate_package(self, package):
        # validate the input package
        if package not in self.get_available_architectures():
            raise ValueError(f"{package} not a valid Debian package")
    def req_package_details(self):
        # request and parse the package details from the mirror URL
        data = self.req_package_details_data()
        return self._build_package_json(data)
    def req_package_details_data(self):
        # request the package details data from the mirror URL
        res = requests.get(self.mirror_url)
        return res.text.splitlines()
    def _build_package_json(self, data):
        # build JSON data from the filtered package details data
        filtered_data = []
        for row in data:
            if "Contents-" in row and ".gz" in row:
                filtered_data.append(row)
        return self._build_json_data_with_filtered_data(filtered_data)
    @staticmethod
    def _build_json_data_with_filtered_data(filtered_data):
        # build JSON data from the filtered data
        data_info = {}
        for row in filtered_data:
            info = row[row.rfind("Contents-") : row.rfind(".gz")]
            architecture = info[info.rfind("-") + 1 :]
            data_info = Debian._add_to_data_json(architecture, info, data_info)
        return data_info
    @staticmethod
    def _add_to_data_json(architectu, info, data_info):
        # add data to JSON object
        if architectu not in data_info:
            data_info[architectu] = {}
        if "Contents-udeb" in info:
            data_info[architectu]["udeb_filename"] = f"{info}.gz"
        else:
            data_info[architectu]["fileName"] = f"{info}.gz"
        return data_info
    def _get_debian_package_data(self, package):
        # get package data from the mirror URL
        url = self.mirror_url + self.package_details[package]["fileName"]
        content = BytesIO(requests.get(url).content)
        return gzip.open(content, "rt")
    @staticmethod
    def _get_file_name_package(line):
        # parse package filename from line of data
        info = line.split()
        if len(info) > 2:
            return info[:-1], info[-1].split("/")[-1]
        if len(info) == 2:
            return info[0],  info[1].split("/")[-1]
        return False, False
    def _get_add_value_from_filename(self, file_name):
        # get add value from filename
        add = 1
        if file_name == "EMPTY_PACKAGE":
            add = 0
        return add
    def _package_list_modification(self, add, architectu, package_list):
        # check if the given architecture is not in the package list
        if architectu not in package_list:
            # add the architecture with the given value to the package list
            package_list[architectu] = add
        else:
            # update the value of the architecture in the package list
            package_list[architectu] += add
        # return the updated package list
        return package_list
    def count_json(self, data, package):
       # initialize an empty dictionary to hold the package count
        package_list = {}
       # read each line of data
        for line in data.readlines():
           # get the file name and package name from the current line
            file_name, package = self._get_file_name_package(line)
           # get the value to add to the package count
            add = self._get_add_value_from_filename(file_name)
           # if file_name is not False and add is not 0
            if file_name and add:
               # update the package count for the given architecture
                package_list = self._package_list_modification(add, package, package_list)
             # sort the package count by the number of files in descending order
        sorted_package_list = sorted(package_list.items(), key=lambda x: x[1], reverse=True)
                # return the sorted package count
        return sorted_package_list


if __name__ == "__main__":
     debian_package = Debian()
     available_architectures = debian_package.get_available_architectures()
     top_packages = debian_package.req_status(sys.argv[1]) #for listing of the top packages
     for i, (package, count) in enumerate(top_packages):
          print(f"{i+1:<10}{package:<50}{count:>10}")