import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css'

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [success,setSuccess]=useState()

    const onFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const onFileUpload = async () => {
        if (!file) {
            setMessage('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                mode: 'cors'
            });
            setMessage(response.data.header);
            console.log('Response:', response.data);
            setSuccess(true)
        } catch (error) {
            setMessage('Error uploading file.');
            console.error('Error:', error);
            setSuccess(false)
        }
    };

    const onFileDownload=async()=>{
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await axios.post('http://127.0.0.1:5000/download', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                mode: 'cors'
            });
            setMessage(response.data.header);
            console.log('Response:', response.data);
        } catch (error) {
            setMessage('Error uploading file.');
            console.error('Error:', error);
        }


    }
    const downloadFile = async () => {
        const formData = new FormData();
        formData.append('file', file);
        const filename = 'example.txt'; // Change this to the desired filename
        try {
            const response = await axios.post('http://127.0.0.1:5000/download', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                mode: 'cors'
            });
          
          if (!response.ok) {
            throw new Error('Network response was not ok.');
          }
        
        let blob;
        if (typeof response.blob === 'function') {
          blob = await response.blob();
        } else {
          const arrayBuffer = await response.arrayBuffer();
          blob = new Blob([arrayBuffer]);
        }
  
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link); // Clean up
        } catch (error) {
          console.error('There was an error downloading the file:', error);
        }
      };

      return (
        <div className="container">
            <div className="upload-box">
                <h2>UPLOAD HTML DOCUMENT</h2>
                <input type="file" accept=".html" onChange={onFileChange} />
                <button onClick={onFileUpload}>Upload</button>
                {message && (<>
                    <p className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
                        {message}
                    </p>
                   {success ?  <button onClick={downloadFile}>Download</button> : null}
                    </>
                    
                )}
               
            </div>
        </div>
    );
};

export default FileUpload;









