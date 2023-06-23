Instructions for running the Python script to get package statistics:

#STEP 1:
    Create a virtual Python environment and activate it:

    bash
    Copy code
    python3 -m pip install --user --upgrade pip
    python3 -m pip --version
    python3 -m pip install --user virtualenv
    python3 -m venv env
    source env/bin/activate
    Add the shebang line at the beginning of the Python file to indicate the path to the Python interpreter. (package_statistics.py)

    bash
    Copy code
    .../env/bin/python
#STEP 2:
    Install the required module:

    Copy code
    pip install requests
#STEP 3:
    Run the Python script in the terminal, providing the architecture (one of: all, amd64, arm64, armel, armhf, i386, mips64el, mipsel, ppc64el, s390x, source) as an argument. For example:

    bash
    Copy code
    chmod +x package_statistics.py
    ./package_statistics.py amd64
#Approach and Time to Solve the Exercise:
    The exercise took approximately 5-6 hours to complete.

    The package_statistics.py file includes several methods for obtaining and analyzing package data from a Debian package mirror URL. The __init__ method initializes the mirror URL and gets package details using the req_package_details method. The req_status method validates the architecture parameter and retrieves package data for that architecture using the _get_debian_package_data method. The count_json method counts the packages in the data and returns the top ten packages. The get_package_list method returns the package list, and the get_available_architectures method returns a list of available architectures.
    The __init__ method initializes the mirror URL for the Debian package and gets package details by calling the req_package_details method. The req_status method takes an architecture parameter and validates it. It then gets package data for that architecture using the _get_debian_package_data method and counts the packages in the data using the count_json method. Finally, it returns the top ten packages.
    The get_package_list method returns the package list, while the get_available_architectures method returns a list of available architectures.
    The validate_package method validates the input package and raises a ValueError if the input package is not valid.
    The req_package_details method requests and parses the package details from the mirror URL using the req_package_details_data method and builds JSON data from the filtered package details data using the _build_package_json method.
    The _build_package_json method builds JSON data from the filtered package details data by iterating through the filtered data and extracting architecture and filename information. It then adds the data to a JSON object using the _add_to_data_json method.
    The _add_to_data_json method adds data to a JSON object if the architecture is not already in the object. It also handles .udeb files differently than other files.
    The _get_debian_package_data method gets package data from the mirror URL using the architecture and filename information in the package details JSON object.
    The _get_file_name_package method parses the package filename from the line of data, and the _get_add_value_from_filename method gets to add value from the filename.
    The _package_list_modification method updates the package count for the given architecture.
    The count_json method initializes an empty dictionary to hold the package count, reads each line of data, gets the file name and package name from the current line, gets the value to add to the package count, updates the package count for the given architecture, and sorts the package count by the number of files in descending order.
    Finally, the script checks if it is being run as the main program creates a Debian object, gets a list of available architectures, get the top packages for the architecture specified in the command line argument, and prints the top ten packages with their counts.



