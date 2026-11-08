import os
import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['reading_score','writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )


            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("OneHOtEncoder", OneHotEncoder()),
                ]
            )

            preprocessor = ColumnTransformer([
                ("numerical_pipeline", num_pipeline, numerical_columns),
                ("categorical_pipeline", cat_pipeline, categorical_columns),
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)



    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)  

            logging.info("Reading of training and test data completed")

            logging.info("Obtaining preprocessor object")

            preprocessor = self.get_data_transformer_object()

            target_col_name = ['math_score']

            target_feature_train_df = train_data[target_col_name]
            input_feature_train_df = train_data.drop(columns=target_col_name)

            target_feature_test_df = test_data[target_col_name]
            input_feature_test_df = test_data.drop(columns=target_col_name)

            logging.info("Applying preprocessing on train and test dataframes")

            input_feature_train_array = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_array,np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
