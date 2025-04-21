import io
from flask import jsonify, send_file
from ftplib import FTP, error_perm
from logger.logger import Logger

class FTPService:

    def __init__(self):
        # FTP server config
        self.FTP_HOST = "192.168.1.70"  # FTP server address
        self.FTP_USER = 'ftpuser'  # FTP username
        self.FTP_PASS = 'ftpuser'  # FTP password
        self.FTP_PORT = 21  # FTP port
        self.FTP_DIR = '/'  # Directory to upload files to
        self.logger = Logger()  # Initialize logger
        
    def upload_file(self, file):
        try:
            # Upload to FTP server
            with FTP(self.FTP_HOST) as ftp:
                ftp.login(user=self.FTP_USER, passwd=self.FTP_PASS)

                # Verify that directory exists
                try:
                    ftp.cwd(self.FTP_DIR)
                except error_perm:
                    # Create directory if it doesn't exist
                    ftp.mkd(self.FTP_DIR)
                    ftp.cwd(self.FTP_DIR)
                
                # Stream the file directly to FTP without local save
                file.seek(0)  # Rewind the file pointer
                ftp.storbinary(f'STOR {file.filename}', file.stream)
                
                # Verify file was uploaded
                size = ftp.size(file.filename)
                print(f"Uploaded {file.filename}, size: {size} bytes")
            
            return jsonify({'message': f'File {file.filename} uploaded successfully'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def get_files(self):
        try:
            with FTP(self.FTP_HOST) as ftp:
                ftp.login(user=self.FTP_USER, passwd=self.FTP_PASS)
                ftp.cwd(self.FTP_DIR)

                files = []

                # Parse LIST output correctly (handles spaces in filenames)
                def parse_line(line):
                    parts = line.split()
                    # Join all parts after the 8th element (filename may contain spaces)
                    filename = ' '.join(parts[8:]) if len(parts) > 8 else ''
                    if filename:  # Skip empty lines/directories
                        content = {
                            'name': filename,
                            'size': int(parts[4]), # Size in bytes
                            'type': 'directory' if parts[0][0] == 'd' else 'file',
                            'modified': ' '.join(parts[5:8]), # Date of last modification
                            'preview_url': f'/api/preview_file/{filename}'
                        }
                        files.append(content)

                ftp.retrlines('LIST', parse_line)

                self.logger.info(f"Files in {self.FTP_DIR}: {files}")
                return jsonify({'files': files}), 200
            
        except error_perm as e:
            self.logger.error(f"FTP error: {str(e)}")
            return jsonify({'error': f'FTP error :{str(e)}'}), 500
        except Exception as e:
            self.logger.error(f"Error fetching files: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
    def download_file(self, filename):
        self.logger.info(f"Downloading file: {filename}")
        try:
            with FTP(self.FTP_HOST) as ftp:
                ftp.login(user=self.FTP_USER, passwd=self.FTP_PASS)
                ftp.cwd(self.FTP_DIR)

                # Create a local file to save the downloaded file
                file_data = io.BytesIO()
                ftp.retrbinary(f'RETR {filename}', file_data.write)
                file_data.seek(0)

                return send_file(
                    file_data,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='/application/octet-stream'
                )
            
        except error_perm:
            self.logger.error(f"File {filename} not found on FTP server")
            return jsonify({'error': f'File {filename} not found'}), 404
        except Exception as e:
            self.logger.error(f"Error downloading file {filename}: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
    def preview_file(self, filename):
        self.logger.info(f"Previewing file: {filename}")
        try:
            with FTP(self.FTP_HOST) as ftp:
                ftp.login(user=self.FTP_USER, passwd=self.FTP_PASS)
                ftp.cwd(self.FTP_DIR)

                # Create a local file to save the downloaded file
                file_data = io.BytesIO()
                ftp.retrbinary(f'RETR {filename}', file_data.write)
                file_data.seek(0)

                mimetype = 'application/octet-stream'
                if filename.lower().endswith('.txt'):
                    mimetype = 'text/plain'
                elif filename.lower().endswith('.pdf'):
                    mimetype = 'application/pdf'
                elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    mimetype = f'image/{filename.split(".")[-1].lower()}'

                return send_file(
                    file_data,
                    mimetype=mimetype
                )
            
        except error_perm:
            self.logger.error(f"File {filename} not found on FTP server")
            return jsonify({'error': f'File {filename} not found'}), 404
        except Exception as e:
            self.logger.error(f"Error downloading file {filename}: {str(e)}")
            return jsonify({'error': str(e)}), 500
