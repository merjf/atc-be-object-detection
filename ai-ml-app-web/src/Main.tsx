import { Box, Button, Container, Divider } from "@mui/material";
import { makeStyles } from "@mui/styles";
import { useState } from "react";
import Header from './components/Header'
import Footer from './components/Footer'
import { fetchResult } from './services/ai-ml-service'
import { Response, Image } from './types/responses'
import CleaningServicesIcon from '@mui/icons-material/CleaningServices';
import UploadIcon from '@mui/icons-material/Upload';
import ImageIcon from '@mui/icons-material/Image';

const useStyles = makeStyles({
  main: {
    display: "flex !important",
    marginTop: 100,
    flexDirection: "column",
    alignItems: "center",
    gap: 15,
    marginBottom: 100
  },
  formBox: {
    display: "flex",
    gap: 20
  },
  divider: {
    borderWidth: "3px !important",
    width: "50%",
    borderRadius: "50px !important",
  },
  resultBox: {
    display: "flex",
    gap: 40
  },
  previewImageBox: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 5
  },
  dataResultBox: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 5
  }
});

function App() {
  const classes = useStyles();

  const [result, setResult] = useState<Response>();
  const [image, setImage] = useState<Image>();

  const getImage = (event : any) => {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function (event: any) {
      var url = URL.createObjectURL(file);
      setImage({src: url, value: reader.result, name: file.name});
    }.bind(reader);
  }

  const uploadImage = () => {
    fetchResult()
      .then((res) => {
        setResult(res);
    })
  }

  const cleanData = () => {
    setResult(undefined);
    setImage(undefined);
  }

  return (
    <div className="App">
      <Header />
      <Container className={classes.main} maxWidth={"md"}>
        <h2>Upload Image Form</h2>
        <Box className={classes.formBox}>
          {!image &&
            <Button variant="contained" startIcon={<UploadIcon />} component="label"> 
              Chose Picture
              <input type="file" hidden onChange={getImage}/>
            </Button>
          }
          {image &&
            <Button variant="contained" startIcon={<ImageIcon />} component="label" onClick={uploadImage}> 
              Upload
            </Button>
          }
          <Button variant="outlined" startIcon={<CleaningServicesIcon />} onClick={cleanData}>
            Clear Data
          </Button>
        </Box>
        <Divider className={classes.divider}/>
        <Box className={classes.resultBox} sx={{flexDirection: { xs: "column", sm: "row"}}}>
          {image &&
            <Box className={classes.previewImageBox}>
              <h3>Preview image:</h3>
              <span>{image.name}</span>
              <img src={image.src} />
            </Box>
          }
          {result && 
            <Box className={classes.dataResultBox}>
              <h3>Data Result:</h3>
              <b>Message:</b> {result?.message}
              <b>Value:</b> {result?.value}
            </Box>
          }
        </Box>
      </Container>
      <Footer />
    </div>
  );
}

export default App;
