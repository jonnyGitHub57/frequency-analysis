# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 06:20:44 2020

@author: jonny
"""
import subprocess

class ReportGenerator(object):
    """"
    Contains methods to create a *.pdf report using LaTeX as application.
    A template file is added with wanted information
    """
    def __init__(self, mainClassRef, Debug=False):
        self.person_name = mainClassRef.name
        self.template = 'weight_template.tex'
        self.report_file = self.person_name + '_weight_report.tex'
        self.debug = Debug
        
    def SimpleReport(self):
        print(self.person_name, 'has a reportfile: ' + self.report_file)
        
    def setLaTeXfileName(self, report_file='weight_report.tex'):
        self.report_file = self.person_name + '_' + report_file
        
    def BasicDataToLaTeX(self, basic_data):
        """
        Add basic data such as name, target weight, target BMI etc
        to the report header section. the insertion point in the
        LaTeX template file is identified by the string:
        '% Insert header data here...'
        """
        template_file = open(self.template,"r")
        result_file = open(self.report_file, "w")
        count = 0
        for line in template_file:
            result_file.write(line)
            if line.strip().startswith('% Insert header data here'):
                result_file.write('Found the place to insert data')
        
    def DataToLaTeX(self, basic_data, physio_data):
        """"
        Fill in the template with data from the calculations
        """
        template_file = open(self.template,"r")
        result_file = open(self.report_file, "w")
        count = 0
        """
        Calculate how many rows to skip in order to fit
        the table into one page 'Max_nr_table_rows' + header (2 rows)
        is the total size of the table
        """
        Max_nr_table_rows = 20
        if len(physio_data) > Max_nr_table_rows:
            skip_to_row = len(physio_data) -Max_nr_table_rows + 1
        else:
            skip_to_row = 1
        for line in template_file:
            result_file.write(line)
            if line.strip().startswith('% Insert header data here'):
                for x in basic_data:
                    result_file.write('\t\t' + x + r'\\' + '\r\n')
            elif line.strip().startswith('% Weight data'):
                result_file.write('\t\t' + str(physio_data[0][0]) + '& ' +
                                    str(physio_data[0][1]) + '& ' +
                                    str(physio_data[0][2]) + '& ' +
                                    str(physio_data[0][3]) + '& ' +
                                    str(physio_data[0][4]) + '& ' +
                                    str(physio_data[0][5]) + r'\\' + '\r\n')                    
                for x in range (skip_to_row, len(physio_data)):
                    result_file.write('\t\t' + str(physio_data[x][0]) + '& ' +
                                    str(physio_data[x][1]) + '& ' +
                                    str(physio_data[x][2]) + '& ' +
                                    str(physio_data[x][3]) + '& ' +
                                    str(physio_data[x][4]) + '& ' +
                                    str(physio_data[x][5]) + r'\\' + '\r\n')
                result_file.write(r'\hline')
            count= count+ 1
        template_file.close()
        result_file.close()        
        print('Number of lines in report = ' + str(count))
        subprocess.run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", 
                        self.report_file])