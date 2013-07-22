import zipfile
import tempfile

def unzip(zipped_file):
    temp_zip = tempfile.SpooledTemporaryFile(1024*10000)
    temp_zip.write(zipped_file)
    if not zipfile.is_zipfile(temp_zip):
        return False
    
    zip = zipfile.ZipFile(temp_zip)
    
    temp_dir = tempfile.mkdtemp()
    zip.extractall(temp_dir)
    return temp_dir