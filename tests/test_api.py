from fastapi import status
from fastapi.testclient import TestClient
from main import app
from io import BytesIO

client = TestClient(app)

class TestMainAPI:
    def test_upload_audio_missing_file(self):
        """Test upload audio with missing file"""
        response = client.post("/score-audio/", data={"target": "hello"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error
    
    def test_upload_audio_missing_target(self):
        """Test upload audio with missing target"""
        # Create a mock audio file
        audio_content = b"mock audio content"
        files = {"file": ("test.wav", BytesIO(audio_content), "audio/wav")}
        
        response = client.post("/score-audio/", files=files)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_upload_audio_invalid_file_type(self):
        """Test upload audio with invalid file type"""
        files = {"file": ("test.txt", BytesIO(b"not audio"), "text/plain")}
        data = {"target": "hello"}
        
        response = client.post("/score-audio/", files=files, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_upload_audio_invalid_file_size(self):
        """Test upload audio with invalid file size"""
        files = {"file": ("test.wav", BytesIO(b"a" * 11 * 1024 * 1024), "audio/wav")}
        data = {"target": "hello"}
        
        response = client.post("/score-audio/", files=files, data=data)
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_upload_audio_with_real_file(self):
        """Test upload audio with a real audio file"""
        # Open the actual audio file
        with open("tests/audio/rabbit.wav", "rb") as audio_file:
            files = {"file": ("rabbit.wav", audio_file, "audio/wav")}
            data = {"target": "rabbit"}
            
            response = client.post("/score-audio/", files=files, data=data)
            assert response.status_code == status.HTTP_200_OK
            
            # Check the response structure
            result = response.json()
            assert "score" in result
            assert "transcript" in result
            assert "filename" in result
            assert result["filename"] == "rabbit.wav"
    