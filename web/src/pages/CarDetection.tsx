import { useState } from "react";
import { makeStyles } from "@mui/styles";
import { Box, Button, Container, Divider } from "@mui/material";
import { fetchCarModelTesting, fetchCarDatasetInfo } from '../services/APIService'
import { Response, Image } from '../models/responses'
import CleaningServicesIcon from '@mui/icons-material/CleaningServices';
import UploadIcon from '@mui/icons-material/Upload';
import ImageIcon from '@mui/icons-material/Image';

const useStyles = makeStyles({
    main: {
      display: "flex !important",
      flexDirection: "column",
      alignItems: "center",
      gap: 15,
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
      gap: 0,
      "& > pre": {
        margin: 0
      },
      "& > img":{
        maxWidth: 400,
      }
    },
    dataResultBox: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 5
    }
});

const CarDetection = () => {
    const classes = useStyles();

    const [result, setResult] = useState<Response>();
    const [image, setImage] = useState<Image>();
  
    const getImage = (event : any) => {
      var file = event.target.files[0];
      setImage({
        src: URL.createObjectURL(file),
        value: file,
        name: file.name,
        type: file.type,
        size: file.size
      });
    }

    const getCarDatasetInfo = () => {
      if(image){
        fetchCarModelTesting(image)
          .then((res) => {
            setResult(res);
          })
      }
    }
  
    const cleanData = () => {
      setResult(undefined);
      setImage(undefined);
    }

    return (
        <Container className={classes.main} maxWidth={"md"}>
            <h2>Car Detection</h2>
            <Box className={classes.formBox}>
              {!image &&
                  <Button variant="contained" startIcon={<UploadIcon />} component="label"> 
                  Chose Picture
                  <input type="file" hidden onChange={getImage}/>
                  </Button>
              }
              {image &&
                  <Button variant="contained" startIcon={<ImageIcon />} component="label" onClick={getCarDatasetInfo}> 
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
                    <img src={image.src} />
                  </Box>
              }
              {result &&
                  <Box className={classes.dataResultBox}>
                    <h3>Data Result:</h3>
                    <b>Class:</b> {result?.class}
                    <b>Accuracy:</b> {result?.accuracy}
                  </Box>
              }
            </Box>
        </Container>
    )
}

export default CarDetection;