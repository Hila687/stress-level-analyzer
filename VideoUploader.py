import os
import uuid
from werkzeug.datastructures import FileStorage

class VideoUploader:

    #a path to the directory
    UPLOAD_FOLDER = 'temp_videos'

    #valid extensions
    ALLOWED_EXTENSIONS = {'mpeg', 'wmv', 'mp4', 'qt', 'mpg', 'm1v', 'mov', 'mpe', 'flv', 'avi'}

    #A function to save the video file in a unique name in the directory
    def save_video(self,file:FileStorage)->str:

        #Check if the file has a valid extension
        if not self._allowed_file(file.filename):
            raise ValueError("File type is not suported")
        
        #create a unique file name
        extension = file.filename.rsplit('.', 1)[-1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"

        #create the folder if does not exist
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
        
        save_path = os.path.join(self.UPLOAD_FOLDER, unique_filename)

        #save the file
        file.save(save_path)

        return save_path


    #Check if the file has a valid extension  
    def _allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in self.ALLOWED_EXTENSIONS
    
    #a function to delete the file 
    def delete_video(self, path: str):
        if os.path.exists(path):
            os.remove(path)


