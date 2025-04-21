from flask import Blueprint, request, jsonify
from logger.logger import Logger

class Routes(Blueprint):

    def __init__(self, ftp_service):
        super().__init__('routes', __name__)
        self.ftp_service = ftp_service
        self.logger = Logger()
        self.register_routes()

    def register_routes(self):
        self.route('/api/upload_file', methods=['POST'])(self.upload_file)
        self.route('/api/get_files', methods=['GET'])(self.get_files)
        self.route('/api/download_file/<filename>', methods=['GET'])(self.download_file)
        self.route('/api/preview_file/<filename>', methods=['GET'])(self.preview_file)

    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        return self.ftp_service.upload_file(file)
    
    def get_files(self):
        return self.ftp_service.get_files()
    
    def download_file(self, filename):
        if not filename:
            self.logger.error("Filename is required for download")
            return jsonify({'error': 'Filename is required'}), 400
        
        self.logger.info(f"Downloading file: {filename}")
        return self.ftp_service.download_file(filename)
    
    def preview_file(self, filename):
        if not filename:
            self.logger.error("Filename is required for preview")
            return jsonify({'error': 'Filename is required'}), 400
        
        self.logger.info(f"Previewing file: {filename}")
        return self.ftp_service.preview_file(filename)