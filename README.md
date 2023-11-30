# EnergyUsageDataWorkflow
Energy Usage Data Workflow

This repository contains a two-step Python workflow for processing energy usage data. The first script, process_delivery_dates.py, pre-processes delivery dates from Excel files, setting up a framework for further analysis. The second script, process_energy_usage.py, takes these pre-processed files and analyzes the energy usage data, converting various energy units to kilo British Thermal Units (kBTU) and aggregating usage on a monthly basis.

Installation

Before running the scripts, ensure you have Python installed on your system. Additionally, the Pandas library is required for data manipulation. You can install Pandas using the following command:

bash
Copy code
pip install pandas
Structure

The repository consists of two main scripts:

process_delivery_dates.py: Processes initial delivery date data from Excel files.
process_energy_usage.py: Processes energy usage data, converting to kBTU and aggregating it monthly.
Usage

Place your raw Excel files in the input_files directory.
Run process_delivery_dates.py to generate intermediate files in the intermediate_files directory.
Run process_energy_usage.py to process these intermediate files and generate the final output in the output_files directory.
Contributing

Contributions to this project are welcome. To contribute:

Fork the repository.
Create a new branch for your feature (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.
License

This project is licensed under the MIT License - see the LICENSE.md file for details.

Contact

For any queries regarding this project, please open an issue in the GitHub repository.
