#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

import getopt
import random
import sys
import unittest


class StockException(Exception):
    """
    General Exception for the Stock Class
    """
    pass

class Stock(object):
    """
    Loads a Memory loadable CSV File to the program, which contains stock data of multiple companies over a periode
    The methods in this class helps to find the highest stock value for the company over the periode
    """

    def __init__(self, fp):
        self.read_file(fp)
    
    def read_file(self, fp = None):
        if fp:
            try:
                self.fp = open(fp,'rb')
                self.reader = csv.reader(self.fp)
                self.header = self.reader.next()
                self.check_format(header = self.header)
                self.companies = {}
            except IOError:
                raise StockException ("Error Opening File")
    
    def close_fp(self):
        if self.fp:
            self.fp.close()

    def check_format(self, line = None, header = None):
        try:
            if header and isinstance(header, list):
                if header[0].lower == 'year' and header[1].lower == 'month':
                    return True

            #print isinstance(line,list)
            if line and isinstance(line, list):
                for index, item in enumerate(line):
                    if index >= 2:
                        y = float(line[index])

                    elif len(line[0]) == 4 and len(line[1]) == 3:
                        pass    
                
                return True
        except Exception:
            raise StockException ("CSV File contain Errors") 
    
    def find_highest(self):
        if self.fp and self.reader and self.header:
            for row in self.reader:
                self.check_format(line = row)
                for index, company in enumerate(self.header):
                    if index >=2:
                        if self.companies.get(company) and self.companies.get(company).get('price') and self.companies.get(company).get('year_month'):
                            if float(row[index]) > self.companies.get(company).get('price'):
                                self.companies[company]['price'] = float(row[index])
                                self.companies[company]['year_month'] = ["%s, %s" %(row[0], row[1])]
                            elif float(row[index]) == self.companies.get(company).get('price'):
                                self.companies[company]['year_month'].append("%s, %s" %(row[0], row[1]))
                        elif not self.companies.get(company):
                                self.companies[company] = {'price':float(row[index]), 'year_month':["%s, %s" %(row[0], row[1])]}
            return True

    def print_highest(self):

        self.find_highest()
        print "\n"
        print "{0:=^60}".format("=")
        print "%-15s %10s %20s" %("Company","Highest Price","Year and Month")
        print "{0:=^60}".format("=")
        for company, data in self.companies.iteritems():
            c_flag = True 
            if data.get('price') and data.get('year_month'):
                for year_month_item in data['year_month']:
                    if c_flag:
                        print "%-15s %10.2f %20s" %(company, data['price'], year_month_item)
                        c_flag = False
                    else:
                        print "%-15s %10s %20s" %(' ',' ',year_month_item)

            print "{0:=^60}".format("=")
        return True


if __name__ == '__main__':
    
    from unittesthighstock import TestStock    
    
    try:
        fnopt, args = getopt.getopt(sys.argv[1:], "f:t")
        for o, value in fnopt:
            if o == '-f':
                try:
                    sa = Stock(value)
                    sa.print_highest()
                    sa.close_fp

                except (StockException), e:
                    print e

                finally:
                    sys.exit()
            elif o == '-t':
                suite = unittest.TestLoader().loadTestsFromTestCase(TestStock)
                unittest.TextTestRunner(verbosity=2).run(suite)            
                sys.exit() 

        sys.exit("Usage: %s -f <csvfile>\n %s -t for test" % (sys.argv[0], sys.argv[0]))

    except getopt.GetoptError:
        sys.exit("Usage: %s -f <csvfile>\n %s -t for test" % (sys.argv[0],sys.argv[0]))  



