import { Dialog, DialogTitle, Typography } from "@mui/material";

export default function PreviewFile({open, setOpen, file}) {

    const handleClose = () => {
        setOpen(false); // Close the dialog when the close button is clicked
    }

    return (
        <Dialog onClose={handleClose} open={open}>
            <DialogTitle>{file === null ? "Preview File" : file.name}</DialogTitle>
            <Typography variant="body1" sx={{ padding: 2 }}>
                This is a preview of the file. You can add your preview logic here.
            </Typography>
            <iframe 
                src={file === null ? "" : `http://localhost:5000${file.preview_url}`} // Replace with the actual URL to fetch the file
                width="100%"
                height="500px"
                title="File Preview"
            />
        </Dialog>
    )
}