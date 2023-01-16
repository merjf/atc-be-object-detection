import { Box, Button, Container, Divider } from "@mui/material";
import { makeStyles } from "@mui/styles";
import { useState } from "react";
import Header from './components/Header'
import { fetchResult, Response } from './services/ai-ml-service'
import CleaningServicesIcon from '@mui/icons-material/CleaningServices';
import UploadIcon from '@mui/icons-material/Upload';

const useStyles = makeStyles({
  main: {
    display: "flex !important",
    marginTop: 200,
    flexDirection: "column",
    alignItems: "center",
    gap: 15
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
    flexDirection: "column",
    alignItems: "center",
  }
});

function App() {
  const classes = useStyles();

  const [result, setResult] = useState<Response>();

  const getResult = () => {
    fetchResult()
      .then((res) => {
        setResult(res);
    })
  }

  const cleanData = () => {
    setResult(undefined);
  }

  return (
    <div className="App">
      <Header />
      <Container className={classes.main} maxWidth={"md"}>
        <h2>Upload Image Form</h2>
        <Box className={classes.formBox}>
          <Button variant="contained" startIcon={<UploadIcon />} onClick={getResult}>
            Upload
          </Button>
          <Button variant="outlined" startIcon={<CleaningServicesIcon />} onClick={cleanData}>
            Clear
          </Button>
        </Box>
        <Divider className={classes.divider}/>
        {result && 
          <Box className={classes.resultBox}>
            <h3>Result:</h3>
            <Box sx={{whiteSpace: "pre"}}>
              <b>Message:</b> {result?.message}
              <b>Value:</b> {result?.value}
            </Box>
          </Box>}
      </Container>
    </div>
  );
}

export default App;
