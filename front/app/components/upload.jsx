import { Button, Container, FormControl, Grid, Typography } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import PreviewFile from "./preview";

export default function Upload() {

    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [files, setFiles] = useState([]);

    const [currentFile, setCurrentFile] = useState(null); // State to manage the current file for preview
    const [open, setOpen] = useState(false); // State to manage the dialog open/close

    useEffect(() => {
        fetchAllFiles(); // Fetches all files when the component mounts
    }, []);

    const handleCloseDialog = () => {
        setOpen(true); // Toggle the open state of the dialog
    }

    const handlePreview = (file) => {
        setCurrentFile(file); // Set the current file for preview
        setOpen(true); // Open the preview dialog
    }

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    }

    // Function that fetches all files from the FTP server
    const fetchAllFiles = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/get_files'); // Fetches the list of files from the server
            console.info('Files fetched successfully:', response.data.files); // Log the response to the console
            setFiles(response.data.files); // Sets the files state with the fetched data
            setMessage('Files fetched successfully'); // Update message state
        }
        catch (error) {
            setMessage('Error fetching files: ' + error); // Update message state with error
            console.error('Error fetching files:', error); // Log the error to the console
        }
    }

    // Function that handles the file upload to the FTP server
    // It uses FormData to send the file in a multipart/form-data format
    const handleUpload = async (e) => {
        e.preventDefault();

        console.info('File to upload:', file); // Log the file to the console

        if (!file) {
            setMessage('Please select a file to upload');
            return;
        }

        const formData = new FormData(); // It's used to send files in a form
        formData.append('file', file); // Adds the file to the form data

        try {
            const response = axios.post('http://localhost:5000/api/upload_file', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setMessage(response.data);
            console.info('File uploaded successfully:', response.data);

            setFile(null); // Reset the file state after upload
            fetchAllFiles(); // Fetches all files after uploading a new one
        }
        catch (error) {
            setMessage('Error uploading file: ' + error);
            console.error('Error uploading file: '+ error); // Log the error to the console
        }
    }

    const downloadFile = async (file_name) => {
        console.info('File to download:', file_name); // Log the file name to the console
        try {
            const response = await axios.get(`http://localhost:5000/api/download_file/${file_name}`, {
                responseType: 'blob' // Set the response type to blob for file download
            });

            const url = window.URL.createObjectURL(new Blob([response.data])); // Create a URL for the downloaded file
            const link = document.createElement('a'); // Create a link element
            link.href = url; // Set the href to the URL created above
            link.setAttribute('download', file_name); // Set the download attribute with the file name
            link.click(); 
            link.remove(); // Remove the link element after clicking
            window.URL.revokeObjectURL(url); // Revoke the URL to free up memory

            console.info('File downloaded successfully:', response); // Log the response to the console
        }
        catch(error){
            setMessage('Error downloading file: ' + error); // Update message state with error
            console.error('Error downloading file:', error); // Log the error to the console
        }
    }

    return (
        <Container sx={{ marginTop: 5 }} maxWidth="xl">
            <Typography variant="h3" component="h1" gutterBottom>
                Home Page
            </Typography>

            <form onSubmit={handleUpload}>
                <FormControl fullWidth sx={{ marginBottom: 2 }}>
                    <Typography variant="h5" component="h2" gutterBottom>
                        Upload your files here
                    </Typography>
                    <input type="file" multiple onChange={handleFileChange} />
                    <Button variant="contained" color="primary" type="submit" sx={{ marginTop: 2 }}>
                        Upload File
                    </Button>
                </FormControl>
            </form>

            <Typography variant="h5" component="h3" gutterBottom>
                Files Available:
            </Typography>
            <Grid container>
                {files.map((file) => {
                    return (
                        <Grid size={12} key={file.name}>
                            <Typography variant="subtitle" gutterBottom>
                                {file.name}
                            </Typography>
                            <Button onClick={() => downloadFile(file)} variant="contained" color="primary" sx={{ marginRight: 2, marginTop: 2 }}>
                                Download
                            </Button>
                            {file.type === 'file' && (
                                <Button onClick={() => handlePreview(file)} variant="contained" color="primary" sx={{ marginRight: 2, marginTop: 2 }}>
                                    Preview
                                </Button>
                            )}
                        </Grid>
                    )
                })}
            </Grid>

            <Button onClick={handleCloseDialog} variant="contained" color="primary" sx={{ marginTop: 2 }}>
                Open Preview Dialog
            </Button>
            <PreviewFile open={open} setOpen={setOpen} file={currentFile} />
            
            
        </Container>
    );
}