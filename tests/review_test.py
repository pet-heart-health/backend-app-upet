import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from models.review import Review
from models.petOwner import PetOwner
from models.user import User
from schemas.review import ReviewSchemaGet, ReviewSchemaPost
from services.reviewService import ReviewService

class TestReviewService(unittest.TestCase):
    """
    Pruebas unitarias para el servicio de Review (reseñas)
    """
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        """
        self.db = MagicMock()
        self.petowner_id = 5
        self.veterinarian_id = 10
        self.stars = 4
        self.description = "Excelente atención y trato amable"
        self.test_datetime = datetime.utcnow()
        
        self.user = MagicMock(spec=User)
        self.user.id = 15
        self.user.name = "Juan Pérez"
        self.user.image_url = "https://example.com/image.jpg"
        
        self.petowner = MagicMock(spec=PetOwner)
        self.petowner.id = self.petowner_id
        self.petowner.user = self.user
    
    def test_create_new_review_returns_correct_data(self):
        """
        Prueba que al crear una reseña se devuelven los datos correctos
        """
        self.db.query().filter().first.return_value = self.petowner
        
        review_schema = MagicMock(spec=ReviewSchemaPost)
        review_schema.description = self.description
        review_schema.stars = self.stars
        review_schema.veterinarian_id = self.veterinarian_id
        
        expected_response = {
            "id": 1,
            "description": self.description,
            "stars": self.stars,
            "review_time": self.test_datetime,
            "image_url": self.user.image_url,
            "pet_owner_name": self.user.name
        }
        
        with patch.object(ReviewSchemaGet, 'from_orm', return_value=expected_response):
            result = ReviewService.create_new_review(self.petowner_id, review_schema, self.db)
            
            self.assertEqual(result["id"], 1)
            self.assertEqual(result["description"], self.description)
            self.assertEqual(result["stars"], self.stars)
            self.assertEqual(result["review_time"], self.test_datetime)
            self.assertEqual(result["image_url"], self.user.image_url)
            self.assertEqual(result["pet_owner_name"], self.user.name)
            
            self.db.add.assert_called_once()
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
    
    def test_get_all_reviews(self):
        """
        Prueba obtener todas las reseñas
        """
        review1 = MagicMock()
        review1.id = 1
        review1.description = "Reseña 1"
        review1.stars = 5
        
        review2 = MagicMock()
        review2.id = 2
        review2.description = "Reseña 2"
        review2.stars = 4
        
        mock_reviews = [review1, review2]
        
        self.db.query().options().all.return_value = mock_reviews
        
        def mock_from_orm(review):
            if review.id == 1:
                return {
                    "id": 1,
                    "description": "Reseña 1",
                    "stars": 5,
                    "review_time": self.test_datetime,
                    "image_url": "url1",
                    "pet_owner_name": "Owner 1"
                }
            else:
                return {
                    "id": 2,
                    "description": "Reseña 2",
                    "stars": 4,
                    "review_time": self.test_datetime,
                    "image_url": "url2",
                    "pet_owner_name": "Owner 2"
                }
        
        with patch.object(ReviewSchemaGet, 'from_orm', side_effect=mock_from_orm):
            results = ReviewService.get_all_reviews(self.db)
            
            self.assertEqual(len(results), 2)
            
            self.assertEqual(results[0]["id"], 1)
            self.assertEqual(results[0]["description"], "Reseña 1")
            self.assertEqual(results[0]["stars"], 5)
            
            self.assertEqual(results[1]["id"], 2)
            self.assertEqual(results[1]["description"], "Reseña 2")
            self.assertEqual(results[1]["stars"], 4)

if __name__ == '__main__':
    unittest.main()