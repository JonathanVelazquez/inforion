# Import the code to be tested
import os
import unittest
import pandas as pd
import pandas.testing as pdt
import numpy as np

from inforion.transformation.transform import *
from inforion.helper.filehandling import *

class TestTransformationMethods(unittest.TestCase):

    valid_mappingfile = "data/TestMapping.xlsx"
    invalid_mappingfile = "data/TestMappingError.xlsx"
    sample_otputfile = "data/SampleOutput.xlsx"
    sample_wc_file = "data/SampleWcOutput.xlsx"
    staging_file = "data/StagingData.xlsx"
    staging_wc_file = "data/StagingWcData.xlsx"
    
    staging_data = pd.DataFrame()
    sample_output = pd.DataFrame()
    sample_wc_output = pd.DataFrame()
    staging_wc_data = pd.DataFrame()
    

    def test_validate_dbfields(self):
        field = 'No'
        #change db field for testing
        staged_data = self.staging_data
        staged_data.rename(columns={field: 'No_1'}, inplace=True)
        print(staged_data)
        with self.assertRaises(TransformationError) as context:
            parallelize_tranformation(self.valid_mappingfile, "Artikel", staged_data, None, 1)
            
        self.assertEqual(context.exception.message, "Field '"+field+"' mentioned in mapping sheet is not found.")
    
    def test_validate_tabs(self):
        tab = 'STAT'
        with self.assertRaises(TransformationError) as context:
            parallelize_tranformation(self.invalid_mappingfile, "Artikel", self.staging_data, None, 1)
            
        self.assertEqual(context.exception.message, "Tab '"+tab+"' mentioned in mapping sheet is not found.")
    
    def test_validate_transformation(self):
        df_return = parallelize_tranformation(self.valid_mappingfile, "Artikel", self.staging_data, None, 1)
        df_return = df_return.applymap(str)
        
        pdt.assert_frame_equal(self.sample_output, df_return)
    
    def test_validate_wildcard(self):
        df_return = parallelize_tranformation(self.valid_mappingfile, "Artikel-Lagerort", self.staging_wc_data, None, 1)
        df_return = df_return.applymap(str)
        
        pdt.assert_frame_equal(self.sample_wc_output, df_return)

    def setUp(self):
        self.staging_wc_data = pd.read_excel(self.staging_wc_file)
        self.staging_data = pd.read_excel(self.staging_file, dtype=str)
        self.sample_output = pd.read_excel(self.sample_otputfile, dtype=str).replace(np.nan, "", regex=True)
        self.sample_wc_output = pd.read_excel(self.sample_wc_file, dtype=str).replace(np.nan, "", regex=True)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
