from flask_restful import Resource
import pandas as pd
import os


class RecipeResource(Resource):
    
    def diet_recipe_to_csv(self):
        # csv에서 레시피 정보를 가져옴
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../model/recipe.csv'))
        return df.to_dict(orient='records')
    
    def get(self):
        try:
            return self.diet_recipe_to_csv()
        except Exception as e:
            return {'error': str(e)}, 500
